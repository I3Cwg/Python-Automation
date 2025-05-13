#!/usr/bin/env python3
"""
IP Reputation Checker using VirusTotal API

This script allows users to check the reputation of IP addresses using the VirusTotal API.
It provides detailed information about an IP's reputation across multiple security vendors.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
import requests
import ipaddress
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

class VirusTotalIPChecker:
    """Class to handle VirusTotal API interactions for IP reputation checking."""
    
    def __init__(self, api_key=None):
        """Initialize the IP checker with an API key."""
        self.api_key = api_key or os.environ.get("VT_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set it as parameter or as VT_API_KEY environment variable.")
        
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {
            "x-apikey": self.api_key,
            "Accept": "application/json"
        }
        self.console = Console()
        
    def is_valid_ip(self, ip_address):
        """Validate if the given string is a valid IP address."""
        try:
            ipaddress.ip_address(ip_address)
            return True
        except ValueError:
            return False
        
    def check_ip(self, ip_address):
        """Query VirusTotal for information about an IP address."""
        # Validate IP address
        if not self.is_valid_ip(ip_address):
            self.console.print(f"[red]Invalid IP address: {ip_address}[/red]")
            return None
            
        url = f"{self.base_url}/ip_addresses/{ip_address}"
        
        try:
            with Progress() as progress:
                task = progress.add_task(f"[cyan]Querying VirusTotal for {ip_address}...", total=1)
                
                response = requests.get(url, headers=self.headers)
                progress.update(task, advance=1)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    self.console.print(f"[yellow]IP address {ip_address} not found in VirusTotal database.[/yellow]")
                    return None
                elif response.status_code == 429:
                    self.console.print("[red]API request quota exceeded. Please try again later.[/red]")
                    return None
                else:
                    self.console.print(f"[red]Error: {response.status_code} - {response.text}[/red]")
                    return None
        except requests.exceptions.RequestException as e:
            self.console.print(f"[red]Connection error: {str(e)}[/red]")
            return None

    def display_results(self, data, ip_address):
        """Display the IP reputation results in a formatted table."""
        if not data:
            return
            
        attributes = data.get("data", {}).get("attributes", {})
        
        # Basic information panel
        basic_info = [
            f"IP Address: {ip_address}",
            f"Country: {attributes.get('country', 'Unknown')}",
            f"ASN: {attributes.get('asn', 'Unknown')}",
            f"ASN Owner: {attributes.get('as_owner', 'Unknown')}",
            f"Last Analysis Date: {datetime.fromtimestamp(attributes.get('last_analysis_date', 0)).strftime('%Y-%m-%d %H:%M:%S')}",
        ]
        
        self.console.print(Panel("\n".join(basic_info), title="[bold blue]Basic Information[/bold blue]"))
        
        # Reputation stats
        stats = attributes.get("last_analysis_stats", {})
        if stats:
            stats_table = Table(title="[bold blue]Detection Statistics[/bold blue]")
            stats_table.add_column("Category", style="cyan")
            stats_table.add_column("Count", style="green")
            
            for category, count in stats.items():
                stats_table.add_row(category.replace("_", " ").title(), str(count))
                
            self.console.print(stats_table)
        
        # Detailed vendor results
        vendor_results = attributes.get("last_analysis_results", {})
        if vendor_results:
            results_table = Table(title="[bold blue]Vendor Analysis Results[/bold blue]")
            results_table.add_column("Vendor", style="cyan")
            results_table.add_column("Category", style="yellow")
            results_table.add_column("Result", style="green")
            
            for vendor, result in vendor_results.items():
                category = result.get("category", "unknown")
                method = result.get("method", "unknown")
                result_text = result.get("result", "N/A")
                
                # Color-code by category
                category_style = "green"
                if category in ["malicious", "suspicious"]:
                    category_style = "red"
                
                results_table.add_row(
                    vendor, 
                    f"[{category_style}]{category}[/{category_style}]", 
                    result_text
                )
                
            self.console.print(results_table)
            
        # Whois information if available
        whois_data = attributes.get("whois", "")
        if whois_data:
            self.console.print(Panel(whois_data, title="[bold blue]WHOIS Information[/bold blue]", 
                                    expand=False, width=100))

    def save_report(self, data, ip_address, output_file=None):
        """Save the results to a JSON or text file."""
        if not data:
            return False
            
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"vt_report_{ip_address}_{timestamp}.json"
            
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=4)
            self.console.print(f"[green]Report saved to {output_file}[/green]")
            return True
        except Exception as e:
            self.console.print(f"[red]Error saving report: {str(e)}[/red]")
            return False


def main():
    """Main function to run the IP reputation checker."""
    parser = argparse.ArgumentParser(description="Check IP reputation using VirusTotal API")
    parser.add_argument("ip", help="IP address to check")
    parser.add_argument("-k", "--api-key", help="VirusTotal API key (can also be set as VT_API_KEY environment variable)")
    parser.add_argument("-o", "--output", help="Output file for the report (JSON format)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode - only save report without displaying results")
    parser.add_argument("-b", "--batch", action="store_true", help="Switch to batch mode (use batch_ip_checker.py instead)")
    
    args = parser.parse_args()
    
    # If batch mode is requested, suggest using the batch script
    if args.batch:
        print("For batch processing of multiple IP addresses, please use the batch_ip_checker.py script:")
        print("  python batch_ip_checker.py -f <ip_list_file> -o <output_directory>")
        print("  python batch_ip_checker.py -i <ip1> <ip2> <ip3> ... -o <output_directory>")
        return 0
    
    try:
        # Initialize the checker
        checker = VirusTotalIPChecker(api_key=args.api_key)
        
        # Get IP reputation data
        result = checker.check_ip(args.ip)
        
        if result:
            # Display results if not in quiet mode
            if not args.quiet:
                checker.display_results(result, args.ip)
                
            # Save report if output is specified
            if args.output:
                checker.save_report(result, args.ip, args.output)
            else:
                # Ask if user wants to save the report
                save_report = input("\nDo you want to save the report? (y/n): ").lower() == 'y'
                if save_report:
                    checker.save_report(result, args.ip)
                    
        return 0
    except ValueError as e:
        print(f"Error: {str(e)}")
        return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
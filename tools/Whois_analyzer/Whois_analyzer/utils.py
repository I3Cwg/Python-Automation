"""
extension and utility functions
"""
import os
import re
import json
import csv
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

def validate_domain(domain: str) -> bool:
    """
    Validate the domain name using a regex pattern.
    :param domain: The domain name to validate.
    :return: True if the domain is valid, False otherwise.
    """
    domain_regex = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    )
    return bool(domain_regex.match(domain))

def parse_domain_list(input_file: str) -> List[str]:
    """
    Parse a list of domains from a file.
    :param input_file: The path to the input file.
    :return: A list of domain names.
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"File {input_file} does not exist.")
    
    with open(input_file, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
    
    return [domain for domain in domains if validate_domain(domain)]

def save_to_json(data: Dict[str, Any], output_file: str) -> None:
    """
    Save data to a JSON file.
    :param data: The data to save.
    :param output_file: The path to the output file.
    """
    output_data = {
        "generated_at": datetime.now().isoformat(),
        "count": len(data),
        "results": data
    }
    with open(output_file, 'w') as file:
        json.dump(output_data, file, indent=2)
    

def save_to_csv(data: List[Dict[str, Any]], output_file: str) -> None:
    """
    Save data to a CSV file.
    :param data: The data to save.
    :param output_file: The path to the output file.
    """
    if not data:
        raise ValueError("No data to save.")
    
    fieldnames = [
        'domain', 'status', 'registrar', 'creation_date', 'expiration_date',
        'updated_date', 'days_to_expiration', 'name_servers', 'emails'
    ]

    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            writer.writerow({
                'domain': item.get('domain'),
                'status': item.get('status'),
                'registrar': item.get('registrar'),
                'creation_date': item.get('creation_date'),
                'expiration_date': item.get('expiration_date'),
                'updated_date': item.get('updated_date'),
                'days_to_expiration': item.get('days_to_expiration'),
                'name_servers': ", ".join(item.get('name_servers', [])),
                'emails': ", ".join(item.get('emails', []))
            })

def format_whois_result(result: Dict[str, Any]) -> str:
    """
    Format the WHOIS result for better readability in terminal.
    :param result: The WHOIS result to format.
    :return: A formatted string representation of the result.
    """
    if result.get("status") == "error":
        return f"Name: {result.get('domain')}\nStatus: {result.get('status')}\nError: {result.get('error')}"

    output = []
    output.append(f"Domain: {result.get('domain')}")
    output.append(f"Registrar: {result.get('registrar', 'N/A')}")
    output.append(f"Creation Date: {result.get('creation_date', 'N/A')}")
    output.append(f"Expiration Date: {result.get('expiration_date', 'N/A')}")

    if result.get('days_to_expiration') is not None:
        output.append(f"Days to Expiration: {result.get('days_to_expiration')}")

    # DNS servers
    name_servers = result.get('name_servers', [])
    if isinstance(name_servers, list) and name_servers:
        output.append("Name Servers:")
        for ns in name_servers:
            output.append(f"  - {ns}")
    elif isinstance(name_servers, str):
        output.append("Name Servers:")
        for ns in name_servers.split(","):
            ns = ns.strip()
            if ns:
                output.append(f"  - {ns}")
    else:
        output.append("Name Servers: N/A")


    # Registrant
    registrant = result.get('registrant', {})
    if registrant.get('name') or registrant.get('organization'):
        output.append("Information of Registrant:")
        if registrant.get('name'):
            output.append(f"  Name: {registrant.get('name')}")
        if registrant.get('organization'):
            output.append(f"  Organization: {registrant.get('organization')}")
        if registrant.get('country'):
            output.append(f"  Country: {registrant.get('country')}")
     
    return "\n".join(output)





#!/usr/bin/env python

import whois
import concurrent.futures
import logging
from datetime import datetime
from typing import Dict, List, Optional

# set up logging configuration to log to a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WhoisAnalyzer:
    """
    Class chính để phân tích thông tin WHOIS của tên miền"""            
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def query_domain(self, domain: str) -> Dict:
        """ 
        This function queries the WHOIS information for a given domain.
        :param domain: The domain name to query.
        :return: A dictionary containing the WHOIS information.
        """
        try:
            whois_info = whois.whois(domain)  # Thay đổi cách gọi đây
            return self._process_whois_data(domain, whois_info)
        except Exception as e:
            return {
                "domain_name": domain,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    def batch_query(self, domains: List[str], max_worker: int = 5) -> List[Dict]:
        """
        This function queries the WHOIS information for a list of domains.
        :param domains: A list of domain names to query.
        :param max_worker: The maximum number of concurrent workers.
        :return: A list of dictionaries containing the WHOIS information for each domain.
        """
        from concurrent.futures import ThreadPoolExecutor

        results = []
        logger.info(f"Starting batch WHOIS query for {len(domains)} domains.")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_worker) as executor:
            future_to_domain = {executor.submit(self.query_domain, domain): domain for domain in domains}
            for future in concurrent.futures.as_completed(future_to_domain):
                domain = future_to_domain[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error querying domain {domain}: {str(e)}")
                    results.append({
                        "domain_name": domain,
                        "status": "error",
                        "error": str(e),
                        "timestamp": datetime.now().isoformat()
                    })
        
        return results
        

    def _process_whois_data(self, domain: str, whois_info) -> Dict:
        """
        Xử lý và chuẩn hóa dữ liệu WHOIS
        
        Args:
            domain: Tên miền đã truy vấn
            whois_info: Đối tượng WHOIS từ thư viện python-whois
            
        Returns:
            Dict: Dữ liệu WHOIS đã được chuẩn hóa
        """
        result = {
            "domain": domain,
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "registrar": getattr(whois_info, "registrar", None),
            "creation_date": self._format_date(whois_info.creation_date),
            "expiration_date": self._format_date(whois_info.expiration_date),
            "updated_date": self._format_date(whois_info.updated_date),
            "name_servers": self._format_list(whois_info.name_servers),
            "status": self._format_list(whois_info.status),
            "emails": self._format_list(whois_info.emails),
            "dnssec": getattr(whois_info, "dnssec", None),
            "registrant": {
                "name": getattr(whois_info, "registrant_name", None),
                "organization": getattr(whois_info, "org", None),
                "country": getattr(whois_info, "country", None),
            }
        }
        
        # caculate days to expiration
        if result["expiration_date"]:
            try:
                exp_date = self._parse_date(result["expiration_date"])
                if exp_date:
                    days_remaining = (exp_date - datetime.now()).days
                    result["days_to_expiration"] = days_remaining
            except Exception:
                result["days_to_expiration"] = None
        
        return result

    def _format_date(self, date):
        """
        Format the date to ISO format.
        :param date: The date to format.
        :return: A formatted ISO date string or None.
        """
        if isinstance(date, list):
            return [d.isoformat() if isinstance(d, datetime) else str(d) for d in date]
        elif isinstance(date, datetime):
            return date.isoformat()
        return str(date)

    def _format_list(self, data):
        """
        Format a list of data to a string.
        :param data: The data to format.
        :return: A formatted string or None.
        """
        if isinstance(data, list):
            return ", ".join(data)
        return str(data) if data else None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse a date string to a datetime object.
        :param date_str: The date string to parse.
        :return: A datetime object or None if parsing fails.
        """
        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            return None

# if __name__ == "__main__":
#     whois_analyzer = WhoisAnalyzer()
#     # domain = "example.com"
#     # result = whois_analyzer.query_domain(domain)
#     # print(result)

#         # Test batch query
#     domains = ["example.com", "google.com", "microsoft.com", "github.com", "nonexistent-domain.com"]
#     batch_results = whois_analyzer.batch_query(domains, max_worker=3)
#     print("\nBatch Domain Query:")
#     for res in batch_results:
#         print(res)
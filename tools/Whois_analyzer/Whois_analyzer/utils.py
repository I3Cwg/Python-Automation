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

def parse_domain_list(input_file: str) -> List[str]:
    """
    Parse a list of domains from a file.
    :param input_file: The path to the input file.
    :return: A list of domain names.
    """

def save_to_json(data: Dict[str, Any], output_file: str) -> None:
    """
    Save data to a JSON file.
    :param data: The data to save.
    :param output_file: The path to the output file.
    """

def save_to_csv(data: List[Dict[str, Any]], output_file: str) -> None:
    """
    Save data to a CSV file.
    :param data: The data to save.
    :param output_file: The path to the output file.
    """

def format_whois_result(result: Dict[str, Any]) -> str:
    """
    Format the WHOIS result for better readability.
    :param result: The WHOIS result to format.
    :return: A formatted string representation of the result.
    """



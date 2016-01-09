#!/usr/bin/env python3

__author__ = 'Jay Shepherd'

import ipaddress
import re
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

import bs4


def interactive_url_input():
    """
    Interactive component of soliciting a url. Uses helper function to ensure url is valid.
    :return: Valid URL
    """
    url_input = ''
    while not validate_url(url_input):
        url_input = input("Please enter a url to scrape for IPs. The URL must include http:// or https://: ")
        print('')
    return url_input


def validate_url(url_arg):
    """
    Takes string input and validates url refers to a valid webpage for passing into other functions
    :param url_arg: URL to check for validation
    :return: Boolean result of validation check
    """
    parse = urlparse(url_arg)
    if parse.scheme not in ['http', 'https']:
        return False
    if '.' not in parse.netloc:
        return False
    return True


def get_webpage_text(url_input):
    """
    Extracts text of webpage and returns
    :param url_input: Fully-qualified webpage url to get contents of
    :return: Text of webpage
    """
    data = bs4.BeautifulSoup(urlopen(url_input), 'html.parser')
    return str(data.get_text)


def validate_ip(ip):
    """
    Validates if passed string is an ipv4 or ipv6 address or network.
    :param ip: IP Address as string
    :return: Boolean Result
    """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        try:
            ipaddress.ip_network(ip)
            return True
        except ValueError:
            return False


def ip_from_string(string):
    """
    Takes a string and extracts all valid IP Addresses as a SET of Strings
    Uses the validate_ip helper function to achieve.
    :param string: Any string of data
    :return: IP Addresses as a SET of Strings or Empty Set if none found
    """
    ip_regex = re.compile('(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:\/[0-9]{1,2})?')
    potential_ips = ip_regex.findall(string)
    valid_ips = set()
    for ip in potential_ips:
        if validate_ip(ip) is True:
            valid_ips.add(ip)
    return valid_ips


def main():
    if len(sys.argv) == 1:
        try:
            url_input = interactive_url_input()
        except KeyboardInterrupt:
            print("\nGoodbye")
    else:
        url_input = sys.argv[1]

    webpage_text = get_webpage_text(url_input)
    address_list = ip_from_string(webpage_text)
    if address_list:
        print("\n".join(address_list))
    else:
        print("No ips found when scraping {}".format(url_input))


if __name__ == '__main__':
    main()

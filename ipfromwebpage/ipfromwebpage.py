#!/usr/bin/env python3

__author__ = 'Jay Shepherd'

import argparse
import re
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

import bs4
import netaddr


def check_args(args=None):
    parser = argparse.ArgumentParser(description="IP Webpage Scraper")
    parser.add_argument('url',
                        type=argparse_url_type,
                        help="URL to scrape, must be FQDN ie https://example.com")
    return parser.parse_args(args)


def argparse_url_type(url_to_check):
    """
    This is a helper function that wires check_args to validate_url
    :param url_to_check: The URL positional argument passed from argparse
    :return: Value if okay, otherwise raises argparse exception
    """
    result = validate_url(url_to_check)
    if result:
        return url_to_check
    else:
        raise argparse.ArgumentTypeError(
            "{} is an invalid URL, must specify fqdn, ex. https://www.example.com".format(url_to_check))


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
    data = bs4.BeautifulSoup(urlopen(url_input), 'html.parser').get_text()
    return data


def validate_ip(ip):
    """
    Validates if passed string is an ipv4 or ipv6 address or network.
    :param ip: IP Address as string
    :return: Boolean Result
    """
    try:
        if '/' in ip:
            netaddr.IPNetwork(ip)
        else:
            netaddr.IPAddress(ip)
        return True
    except netaddr.AddrFormatError:
        return False


def ip_from_string(string):
    """
    Takes a string and extracts all valid IP Addresses as a SET of Strings
    Uses the validate_ip helper function to achieve.
    :param string: Any string of data
    :return: IP Addresses as a netaddr.IPSet or empty netaddr.IPSet if none found
    """
    ip_regex = re.compile('(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:\/[0-9]{1,2})?')
    potential_ips = ip_regex.findall(string)
    valid_ips = []
    for ip in potential_ips:
        if validate_ip(ip) is True:
            valid_ips.append(ip)
    return netaddr.IPSet(valid_ips)


def main(url):
    webpage_text = get_webpage_text(url)
    address_list = ip_from_string(webpage_text)
    if address_list:
        for cidr in address_list.iter_cidrs():
            print(cidr)
    else:
        print("No ips found when scraping {}".format(url))


def entrypoint():
    url = check_args(sys.argv[1:]).url
    main(url)


if __name__ == '__main__':
    entrypoint()

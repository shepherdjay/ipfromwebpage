#!/usr/bin/env python3

import argparse
import re
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

import bs4
import netaddr

IPv4_EXCLUSIONS = netaddr.IPSet([
        '0.0.0.0/8',
        '224.0.0.0/3'
])


def check_args(args=None):
    parser = argparse.ArgumentParser(description="IP Webpage Scraper")
    parser.add_argument('url',
                        type=argparse_url_type,
                        help="URL to scrape, must be FQDN ie https://example.com")
    return parser.parse_args(args)


def argparse_url_type(url_to_check: str) -> str:
    """This is a helper function that wires check_args to validate_url"""
    result = validate_url(url_to_check)
    if result:
        return url_to_check
    else:
        raise argparse.ArgumentTypeError(
            "{} is an invalid URL, must specify fqdn, ex. https://www.example.com".format(url_to_check))


def validate_url(url_arg: str) -> bool:
    """Takes string input and validates url refers to a valid webpage for passing into other functions"""
    parse = urlparse(url_arg)
    if parse.scheme not in ['http', 'https']:
        return False
    if '.' not in parse.netloc:
        return False
    return True


def get_webpage_text(url_input: str) -> str:
    """Extracts text of webpage and returns"""
    data = bs4.BeautifulSoup(urlopen(url_input), 'html.parser').get_text()
    return data


def validate_ip(ip: str) -> bool:
    """Validates if passed string is an ipv4 or ipv6 address or network."""
    try:
        if '/' in ip:
            netaddr.IPNetwork(ip)
        else:
            netaddr.IPAddress(ip)
        return True
    except netaddr.AddrFormatError:
        return False


def ip_from_string(string: str) -> netaddr.IPSet:
    """
    Takes a string and extracts all valid IP Addresses as a SET of Strings
    Uses the validate_ip helper function to achieve.
    """
    ip_regex = re.compile(r'(?<!\.)(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?!\.)(?:\/[0-9]{1,2})?')
    potential_ips = ip_regex.findall(string)
    valid_ips = []
    for ip in potential_ips:
        if validate_ip(ip) is True:
            valid_ips.append(ip)
    return netaddr.IPSet(valid_ips) - IPv4_EXCLUSIONS


def ipv6_from_string(string: str) -> netaddr.IPSet:
    """
    Takes a string and extracts all valid IPv6 Addresses as a SET of Strings
    Uses the validate_ip helper function to achieve.
    """

    ipv6_regex = re.compile(
        r'(?<![a-zA-Z\d\.])((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?(\/[\d][\d]?[\d]?|1([01][0-9]|2[0-8]))?|(\.(\d{1,3}))(?<![a-zA-Z\d])')

    potential_ipv6s = re.findall(ipv6_regex, string)
    valid_ipv6s = []

    for ipv6 in potential_ipv6s:
        ipv6 = ipv6[0] + ipv6[75]
        if validate_ip(ipv6) is True:
            valid_ipv6s.append(ipv6)
    return netaddr.IPSet(valid_ipv6s)


def print_address(address_set: netaddr.IPSet, url: str) -> None:
    """
    Takes a set of IPv4/IPv6 Addresses as a netaddr.IPSet and prints out
    each address. If no addresses are in the list then an empty address
    warning is printed for the url that was scraped.
    """
    if address_set:
        for cidr in address_set.iter_cidrs():
            print(cidr)
    else:
        print("No addresses found when scraping {}".format(url))


def main(url: str) -> None:
    webpage_text = get_webpage_text(url)
    address_list = ip_from_string(webpage_text)
    addressv6_list = ipv6_from_string(webpage_text)
    print('================\nIPv4 addresses:')
    print_address(address_list, url)
    print('================\nIPv6 addresses:')
    print_address(addressv6_list, url)


def entrypoint() -> None:
    url = check_args(sys.argv[1:]).url
    main(url)


if __name__ == '__main__':
    entrypoint()

#!/usr/bin/env python3

__author__ = 'Jay Shepherd'

from urllib.request import urlopen
from urllib.parse import urlparse
import re

import bs4


def ip_from_webpage(url_input):
    """Scrapes text of a URL page for IP addresses and returns as set.
    :param url_input: Fully-qualified URL to scrape for IP Addresses
    :return: set
    """
    ip_address = re.compile('(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?:\/[0-9]{1,2})?')
    data = bs4.BeautifulSoup(urlopen(url_input), 'html.parser')
    data = str(data.get_text)
    return set(ip_address.findall(data))


def input_url():
    """
    :return: Printed result of URL scrape
    """
    url_input = ''
    while not validate_url(url_input):
        url_input = input("Please enter a url to scrape for IPs. The URL must include http:// or https://: ")
        print('')
    address_list = ip_from_webpage(url_input)
    if address_list:
        print("\n".join(address_list))
    else:
        print("No ips found when scraping {}".format(url_input))


def validate_url(url_arg):
    """ Takes string input and validates if it is fully qualified url for passing into urlopen
    :param url_arg: URL to check for validation
    :return: Boolean result of validation check
    """
    return urlparse(url_arg).scheme is not ''


if __name__ == '__main__':
    try:
        input_url()
    except KeyboardInterrupt:
        print("\nGoodbye")

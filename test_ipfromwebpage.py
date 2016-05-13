import argparse
from unittest import TestCase

import netaddr

from ipfromwebpage import check_args, argparse_url_type, validate_url, validate_ip, ip_from_string


class TestArgumentParsing(TestCase):
    """
    Why are we testing standard library functions?
    Because you need practice Jay, that is what dharmab would say
    So should I test sys as well?
    """

    def setUp(self):
        self.good_url = 'http://example.com'
        self.bad_url = 'example.com'

    def test_no_arguments(self):
        with self.assertRaises(SystemExit):
            check_args()

    def test_good_return(self):
        result = check_args(self.good_url.split())
        self.assertEqual(result.url, self.good_url)

    def test_error(self):
        with self.assertRaises(SystemExit):
            check_args(self.bad_url)

    def test_appropriate_exception_from_helper(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            argparse_url_type(self.bad_url)


class TestValidate_url(TestCase):
    def test_valid_url(self):
        self.assertTrue(validate_url('http://www.example.com'))

    def test_no_protocol(self):
        self.assertFalse(validate_url('www.example.com'))

    def test_not_http_protocol(self):
        self.assertFalse(validate_url('ftp://www.example.com'))

    def test_custom_tld(self):
        self.assertTrue(validate_url('http://www.example.anything'))

    def test_malformed_url(self):
        self.assertFalse(validate_url('http://example'))


class TestValidate_Ip(TestCase):
    def test_valid_ipv4(self):
        self.assertTrue(validate_ip('192.168.0.1'))

    def test_valid_ipv4network(self):
        self.assertTrue(validate_ip('192.0.0.0/24'))

    def test_valid_ipv6(self):
        self.assertTrue(validate_ip('::1'))

    def test_word(self):
        self.assertFalse(validate_ip('word'))

    def test_invalid(self):
        self.assertFalse(validate_ip('999.999.999.999'))

    def test_close(self):
        self.assertFalse(validate_ip('1234.12341.12.3.3.4'))


class TestIp_from_string(TestCase):
    def test_empty(self):
        self.assertEqual(ip_from_string(''), netaddr.IPSet())

    def test_invalid_multiple(self):
        self.assertEquals(ip_from_string('260.1.3.4 260.1.5.5'),
                          netaddr.IPSet([]))

    def test_valid_multiple(self):
        self.assertEquals(ip_from_string('192.168.0.1 192.168.5.5'),
                          netaddr.IPSet(['192.168.0.1', '192.168.5.5']))

    def test_duplicates(self):
        self.assertEquals(ip_from_string('192.168.0.4 10.2.3.4 192.168.0.4 10.2.3.4'),
                          netaddr.IPSet(['192.168.0.4', '10.2.3.4']))

    def test_newline(self):
        self.assertEqual(ip_from_string('\n192.168.0.1\n10.0.0.1\n'),
                         netaddr.IPSet(['192.168.0.1', '10.0.0.1']))

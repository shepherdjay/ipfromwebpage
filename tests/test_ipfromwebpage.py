import argparse
import io
import os
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import patch

import netaddr

from ipfromwebpage import ipfromwebpage


def get_path(file):
    path = os.path.join(os.path.dirname(__file__), file)
    return path


@patch('ipfromwebpage.ipfromwebpage.urlopen')
class TestExtractWebPageData(TestCase):
    """
    Test case tests bs4 and performs a functional test using mock data from testfiles
    """

    def setUp(self):
        with open(get_path('testfiles/test_html.html'), mode='r') as file:
            self.test_html_doc = file.read()
        with open(get_path('testfiles/test_html_expected.txt'), mode='r') as file:
            self.expected_text = file.read()
        with open(get_path('testfiles/test_functional_expected.txt'), mode='r') as file:
            self.expected_print = file.read()
        with open(get_path('testfiles/test_html_empty.html'), mode='r') as file:
            self.empty_html = file.read()

        self.test_url = 'http://test_html.html'

    def test_extracts_text(self, mock_open):
        """
        Tests the beautifulsoup function to ensure we are getting back the text we expect from its function.
        :param mock_open: A mocked version of built-in urlopen so that we pass the test_html data
        :return:
        """
        mock_open.return_value = self.test_html_doc

        data = ipfromwebpage.get_webpage_text(self.test_url)

        self.assertEqual(data, self.expected_text)
        self.assertEqual(mock_open.call_count, 1)
        mock_open.assert_called_once_with(self.test_url)

    def test_functional_list(self, mock_open):
        with io.StringIO() as buffer, redirect_stdout(buffer):
            mock_open.return_value = self.test_html_doc

            ipfromwebpage.main(self.test_url)

            out = buffer.getvalue()

        self.assertEqual(out, self.expected_print)

    def test_functional_empty(self, mock_open):
        with io.StringIO() as buffer, redirect_stdout(buffer):
            mock_open.return_value = self.empty_html
            test_url = 'http://test_html_empty.html'

            ipfromwebpage.main(test_url)

            out = buffer.getvalue()

            expected = "No ipv4s found when scraping {0}\nNo ipv6s found when scraping {0}\n".format(test_url)

        self.assertEqual(expected, out)


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
            ipfromwebpage.check_args()

    def test_good_return(self):
        result = ipfromwebpage.check_args(self.good_url.split())
        self.assertEqual(result.url, self.good_url)

    def test_error(self):
        with self.assertRaises(SystemExit):
            ipfromwebpage.check_args(self.bad_url)

    def test_appropriate_exception_from_helper(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            ipfromwebpage.argparse_url_type(self.bad_url)


class TestValidateUrl(TestCase):
    def test_valid_url(self):
        self.assertTrue(ipfromwebpage.validate_url('http://www.example.com'))

    def test_no_protocol(self):
        self.assertFalse(ipfromwebpage.validate_url('www.example.com'))

    def test_not_http_protocol(self):
        self.assertFalse(ipfromwebpage.validate_url('ftp://www.example.com'))

    def test_custom_tld(self):
        self.assertTrue(ipfromwebpage.validate_url('http://www.example.anything'))

    def test_malformed_url(self):
        self.assertFalse(ipfromwebpage.validate_url('http://example'))


class TestValidateIp(TestCase):
    def test_valid_ipv4(self):
        self.assertTrue(ipfromwebpage.validate_ip('192.168.0.1'))

    def test_valid_ipv4network(self):
        self.assertTrue(ipfromwebpage.validate_ip('192.0.0.0/24'))

    def test_valid_ipv6(self):
        self.assertTrue(ipfromwebpage.validate_ip('::1'))

    def test_valid_ipv6network(self):
        self.assertTrue(ipfromwebpage.validate_ip('2a03:2880:2130:cf05::/64'))

    def test_word(self):
        self.assertFalse(ipfromwebpage.validate_ip('word'))

    def test_invalid(self):
        self.assertFalse(ipfromwebpage.validate_ip('999.999.999.999'))

    def test_close(self):
        self.assertFalse(ipfromwebpage.validate_ip('1234.12341.12.3.3.4'))


class TestIpFromString(TestCase):
    def test_empty(self):
        self.assertEqual(ipfromwebpage.ip_from_string(''), netaddr.IPSet())

    def test_invalid_multiple(self):
        self.assertEquals(ipfromwebpage.ip_from_string('260.1.3.4 260.1.5.5'),
                          netaddr.IPSet([]))

    def test_valid_multiple(self):
        self.assertEquals(ipfromwebpage.ip_from_string('192.168.0.1 192.168.5.5'),
                          netaddr.IPSet(['192.168.0.1', '192.168.5.5']))

    def test_duplicates(self):
        self.assertEquals(ipfromwebpage.ip_from_string('192.168.0.4 10.2.3.4 192.168.0.4 10.2.3.4'),
                          netaddr.IPSet(['192.168.0.4', '10.2.3.4']))

    def test_newline(self):
        self.assertEqual(ipfromwebpage.ip_from_string('\n192.168.0.1\n10.0.0.1\n'),
                         netaddr.IPSet(['192.168.0.1', '10.0.0.1']))

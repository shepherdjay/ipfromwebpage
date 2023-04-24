import argparse
import io
import os
from contextlib import redirect_stdout
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock, MagicMock

import netaddr
import pytest

import ipfromwebpage


def get_path(file):
    path = os.path.join(os.path.dirname(__file__), file)
    return path


@patch('ipfromwebpage.ipfromwebpage.urlopen')
class TestExtractWebPageData:
    """
    Test case tests bs4 and performs a functional test using mock data from testfiles
    """
    test_url = 'http://test_html.html'
    test_html_doc = ''
    expected_text = ''
    expected_print = ''
    empty_html = ''

    @pytest.fixture(autouse=True)
    def set_up(self):
        with open(get_path('testfiles/test_html.html'), mode='r') as file:
            self.test_html_doc = file.read()
        with open(get_path('testfiles/test_html_expected.txt'), mode='r') as file:
            self.expected_text = file.read()
        with open(get_path('testfiles/test_functional_expected.txt'), mode='r') as file:
            self.expected_print = file.read()
        with open(get_path('testfiles/test_html_empty.html'), mode='r') as file:
            self.empty_html = file.read()

    def test_extracts_text(self, mock_open):
        """
        Tests the beautifulsoup function to ensure we are getting back the text we expect from its function.
        :param mock_open: A mocked version of built-in urlopen so that we pass the test_html data
        :return:
        """
        mock_open.return_value = self.test_html_doc

        data = ipfromwebpage.get_webpage_text(self.test_url)

        assert data == self.expected_text
        assert mock_open.call_count == 1
        mock_open.assert_called_once_with(self.test_url)

    def test_functional_list(self, mock_open):
        with io.StringIO() as buffer, redirect_stdout(buffer):
            mock_open.return_value = self.test_html_doc

            ipfromwebpage.main(self.test_url)

            out = buffer.getvalue()

        assert out == self.expected_print

    def test_functional_empty(self, mock_open):
        with io.StringIO() as buffer, redirect_stdout(buffer):
            mock_open.return_value = self.empty_html
            test_url = 'http://test_html_empty.html'

            ipfromwebpage.main(test_url)

            out = buffer.getvalue()

            expected = "================\nIPv4 addresses:\nNo addresses found when scraping {0}\n================\nIPv6 addresses:\nNo addresses found when scraping {0}\n".format(test_url)

        assert expected == out


class TestArgumentParsing:
    """
    Why are we testing standard library functions?
    Because you need practice Jay, that is what dharmab would say
    So should I test sys as well?
    """
    good_url = 'http://example.com'
    bad_url = 'example.com'

    def test_no_arguments(self):
        with pytest.raises(SystemExit):
            ipfromwebpage.check_args()

    def test_good_return(self):
        result = ipfromwebpage.check_args(self.good_url.split())
        assert result.url == self.good_url

    def test_error(self):
        with pytest.raises(SystemExit):
            ipfromwebpage.check_args(self.bad_url)

    def test_appropriate_exception_from_helper(self):
        with pytest.raises(argparse.ArgumentTypeError):
            ipfromwebpage.argparse_url_type(self.bad_url)

@patch('ipfromwebpage.ipfromwebpage.sys')
@patch('ipfromwebpage.ipfromwebpage.main')
class TestEntryPoint:
    def test_entrypoint(self, mock_main: MagicMock, mock_sys: MagicMock):
        mock_sys.argv = ['ipfromwebpage','http://example.com']
        ipfromwebpage.entrypoint()
        mock_main.assert_called_once_with('http://example.com')


class TestValidateUrl:
    def test_valid_url(self):
        assert ipfromwebpage.validate_url('http://www.example.com')
        assert ipfromwebpage.validate_url('https://www.example.com')

    def test_no_protocol(self):
        assert not ipfromwebpage.validate_url('www.example.com')

    def test_not_http_protocol(self):
        assert not ipfromwebpage.validate_url('ftp://www.example.com')

    def test_custom_tld(self):
        assert ipfromwebpage.validate_url('http://www.example.anything')

    def test_malformed_url(self):
        assert not ipfromwebpage.validate_url('http://example')


class TestValidateIp:
    def test_valid_ipv4(self):
        assert ipfromwebpage.validate_ip('192.168.0.1')

    def test_valid_ipv4network(self):
        assert ipfromwebpage.validate_ip('192.0.0.0/24')

    def test_valid_ipv6(self):
        assert ipfromwebpage.validate_ip('::1')

    def test_valid_ipv6network(self):
        assert ipfromwebpage.validate_ip('2a03:2880:2130:cf05::/64')

    def test_word(self):
        assert not ipfromwebpage.validate_ip('word')

    def test_invalid(self):
        assert not ipfromwebpage.validate_ip('999.999.999.999')

    def test_close(self):
        assert not ipfromwebpage.validate_ip('1234.12341.12.3.3.4')


class TestIpFromString:
    def test_empty(self):
        assert ipfromwebpage.ip_from_string('') == netaddr.IPSet()

    def test_invalid_multiple(self):
        assert ipfromwebpage.ip_from_string('260.1.3.4 260.1.5.5') == netaddr.IPSet([])

    def test_valid_multiple(self):
        assert (ipfromwebpage.ip_from_string('192.168.0.1 192.168.5.5')
                == netaddr.IPSet(['192.168.0.1', '192.168.5.5']))

    def test_duplicates(self):
        assert (ipfromwebpage.ip_from_string('192.168.0.4 10.2.3.4 192.168.0.4 10.2.3.4')
                == netaddr.IPSet(['192.168.0.4', '10.2.3.4']))

    def test_newline(self):
        assert (ipfromwebpage.ip_from_string('\n192.168.0.1\n10.0.0.1\n')
                == netaddr.IPSet(['192.168.0.1', '10.0.0.1']))

    def test_exclusions(self):
        assert (ipfromwebpage.ip_from_string('0.0.3.255 255.255.192.0')
                == netaddr.IPSet())

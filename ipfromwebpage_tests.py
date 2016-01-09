from unittest import TestCase

from ipfromwebpage import *


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
        self.assertEqual(ip_from_string(''), set())

    def test_valid_multiple(self):
        self.assertEquals(ip_from_string('192.168.0.1 192.168.5.5'), {'192.168.0.1', '192.168.5.5'})

    def test_duplicates(self):
        self.assertEquals(ip_from_string('192.168.0.4 10.2.3.4 192.168.0.4 10.2.3.4'), {'192.168.0.4', '10.2.3.4'})

    def test_newline(self):
        self.assertEqual(ip_from_string('\n192.168.0.1\n10.0.0.1\n'), {'192.168.0.1', '10.0.0.1'})

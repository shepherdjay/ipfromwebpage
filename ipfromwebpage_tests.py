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

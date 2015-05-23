#!/usr/bin/env python3

import unittest
from selenium import webdriver

class FooTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.base_url = "http://example.com"

    def is_text_present(self, text):
        return str(text) in self.driver.page_source

    def test_example(self):
        self.driver.get(self.base_url + "/")
        self.assertTrue(self.is_text_present("Example"))

if __name__ == '__main__':

    suite = unittest.TestLoader().loadTestsFromTestCase(FooTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

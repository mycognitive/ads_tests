#!/usr/bin/env python3

import sys, os
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from AdsTest import AdsTest

class AdsTestPagesBasic(AdsTest):

    def test_homepage(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        self.log.debug("Home page loaded.")

        try: self.is_text_present("Browse By Category")
        except AssertionError as e: self.verificationErrors.append(str(e))
        try: self.is_text_present("Browse By Location")
        except AssertionError as e: self.verificationErrors.append(str(e))

        link = driver.find_element_by_xpath(u'//a[contains(text(), "Site map")]')
        self.log.debug("Sitemap link present.")


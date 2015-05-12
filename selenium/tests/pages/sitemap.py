#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from AdsTest import AdsTest

class AdsTestPagesBasic(AdsTest):

    def test_sitemap(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        link = driver.find_element_by_xpath(u'//a[text()="Site map"]')
        link.click()
        self.log.info("Sitemap page loaded successfully.")
        driver.find_element_by_xpath('//div[@id="main"]//a[text()="Register"]')
        self.log.info("Register link present.")


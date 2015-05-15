#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from AdsTest import AdsTest

import time

class AdsTestRegistration(AdsTest):

    def test_registration(self):
        driver = self.driver
        self.log.info("Registering new account.")
        driver.get(self.base_url + "/user/register")
        self.is_error_not_present()
        ymd = time.strftime("%Y%m%d")
        username = "test_" + self.random_word() + "_" + ymd
        email = self.random_word() + "_" + ymd +  "@example.com"
        driver.find_element_by_id("edit-name--2").clear()
        driver.find_element_by_id("edit-name--2").send_keys(username)
        driver.find_element_by_id("edit-mail").clear()
        driver.find_element_by_id("edit-mail").send_keys(email)
        driver.find_element_by_id("edit-conf-mail").clear()
        driver.find_element_by_id("edit-conf-mail").send_keys(email)
        driver.find_element_by_id("edit-submit--2").click()
        self.assertTrue(self.is_text_present("Thank you for applying for an account."))
        self.assertTrue(driver.find_element_by_xpath(u'//a[text()="Site map"]'))
        self.is_error_not_present()

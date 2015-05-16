#!/usr/bin/env python3

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from BaseTest import BaseTest

import time

class AdsTestRegistration(BaseTest):

    def test_registration(self):
        driver = self.driver
        self.log.info("Registering new account.")
        driver.get(self.base_url + "/user/register")
        self.is_error_not_present()
        ymd = time.strftime("%Y%m%d")
        username = "test_" + self.random_word() + "_" + ymd
        password = "pass4" + username
        email = self.random_word() + "_" + ymd +  "@example.com"
        driver.find_element_by_id("edit-name--2").send_keys(username)
        driver.find_element_by_id("edit-mail").send_keys(email)
        driver.find_element_by_id("edit-conf-mail").send_keys(email)
        driver.find_element_by_id("edit-pass-pass1").send_keys(password)
        driver.find_element_by_id("edit-pass-pass2").send_keys(password)
        driver.find_element_by_id("edit-submit--2").click()
        self.assertRegex(self.driver.page_source, "Thank you for applying for an account|Log in successful")
        self.assertTrue(driver.find_element_by_xpath(u'//a[text()="Site map"]'))
        self.is_error_not_present()

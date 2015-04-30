# -*- coding: utf-8 -*-

import os
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from xvfbwrapper import Xvfb

import unittest
import logging
import time
import re
from base64 import b64encode

class AdsTest(unittest.TestCase):
    def __init__(self, *args, cargs=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.vdisplay = Xvfb(width=1280, height=720)
        self.vdisplay.start()
        self.args=cargs
        self.log=logging

    def setUp(self):
        # Set up browser profile.
        # @todo: http://selenium-python.readthedocs.org/en/latest/faq.html
        #fp = webdriver.FirefoxProfile()
        #fp.set_preference("browser.download.dir", os.getcwd())
        #fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")

        # Set up the browser driver.
        browsers = {
            'Firefox':  webdriver.Firefox,
            'Chrome':   webdriver.Chrome,
            'IE':       webdriver.Ie,
            'Opera':    webdriver.Opera,
        }
        # Assign the driver in order: Environment variable, argument value, otherwise Firefox as default.
        self.site = browsers.get(os.environ.get('SELENIUM_BROWSER', self.args.browser), webdriver.Firefox)()

        # Set-up testing URL.
        self.base_url = os.environ.get('SELENIUM_HOST', self.args.host)

        # Set-up credentials (@todo: http://sqa.stackexchange.com/q/12892/2840)
        #if self.args.user or self.args.password:
            #self.headers = { 'Authorization': 'Basic %s' % b64encode(bytes(self.args.user + ':' + self.args.password, "utf-8")).decode("ascii") }

        # Set-up other settings.
        self.site.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.site.maximize_window()

    def is_element_present(self, how, what):
        try: self.site.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.site.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.site.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def wait_for(self, condition_function):
        start_time = time.time()
        while time.time() < start_time + 5:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception('Timeout waiting for {}'.format(condition_function.__name__))

        def tearDown(self):
            self.site.quit()
        self.assertEqual([], self.verificationErrors)

    def page_has_loaded(self):
        page_state = self.site.execute_script('return document.readyState;')
        return page_state == 'complete'

    def is_verbose(self):
        return bool(os.environ.get('VERBOSE', self.args.verbose))

    def log(self, msg=None, level='info', **kwargs):
        levels = {
            'debug':   logging.debug,
            'info':    logging.info,
            'warning': logging.warning,
            'error':   logging.error
        }
        levels.get(level, logging.info)(msg)

    def echo(self, msg, **kwargs):
        print("INFO: ", msg) if self.is_verbose else ''

    def make_screenshot(self, filename='screenshot'):
        self.site.save_screenshot(filename)
        log.debug('Screenshot saved.')

    def kill(self):
        self.vdisplay.stop()


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
import string
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
            'Firefox':      webdriver.Firefox,
            'Chrome':       webdriver.Chrome,
            'IE':           webdriver.Ie,
            'Opera':        webdriver.Opera,
            'PhantomJS':    webdriver.PhantomJS,
        }
        # Assign the driver in order: Environment variable, argument value, otherwise Firefox as default.
        self.driver = browsers.get(os.environ.get('SELENIUM_BROWSER', self.args.browser), webdriver.Firefox)()

        # Set-up testing URL.
        self.base_url = os.environ.get('SELENIUM_HOST', self.args.host)

        # Set-up credentials (@todo: http://sqa.stackexchange.com/q/12892/2840)
        #if self.args.user or self.args.password:
            #self.headers = { 'Authorization': 'Basic %s' % b64encode(bytes(self.args.user + ':' + self.args.password, "utf-8")).decode("ascii") }

        # Set-up other settings.
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.maximize_window()

    def is_text_present(self, text):
        self.log.info("Checking if text '{0}' is present on the page.".format(text))
        return str(text) in self.driver.page_source

    def is_element_present(self, how, what):
        self.log.info("Checking if '{0}' element is present in '{1}' on the page.".format(what, how))
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        self.log.info("Checking if alert is present.")
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def random_word(length=6, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for i in range(length))

    def random_number(length=3):
        return ''.join(random.choice(string.digits) for i in range(length))

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def wait_for(self, condition_function):
        self.log.info("Waiting for {0}".format(condition_function))
        start_time = time.time()
        while time.time() < start_time + 5:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception('Timeout waiting for {}'.format(condition_function.__name__))

        def tearDown(self):
            self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def page_has_loaded(self):
        self.log.info("Checking if page is loaded.")
        page_state = self.driver.execute_script('return document.readyState;')
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
        self.driver.save_screenshot(filename)
        self.log.debug("Screenshot saved as {0}.".format(filename))

    def tearDown(self):
        self.log.debug('Finishing up.')
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def kill(self):
        self.log.debug('Closing display.')
        self.vdisplay.stop()


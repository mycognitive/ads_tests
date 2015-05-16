# -*- coding: utf-8 -*-

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
import random
import time
import re
from base64 import b64encode

class BaseTest(unittest.TestCase):
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
        if not self.base_url:
            self.log.error("Selenium host is required.")
            self.driver.quit()

        # Set-up other settings.
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True
        self.driver.maximize_window()

    def is_text_present(self, text):
        self.log.info("Checking if text '{}' is present at {}.".format(text, self.driver.current_url))
        return str(text) in self.driver.page_source

    def is_element_present(self, how, what):
        self.log.info("Checking if '{}' element is present in '{}' at {}.".format(what, how, self.driver.current_url))
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        self.log.info("Checking if alert is present at {}.".format(self.driver.current_url))
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def is_error_not_present(self, error = "(?i)Example|Lorem|ipsum|on line|MySQL|error"):
        self.log.info("Checking if page has not any errors shown at {}.".format(self.driver.current_url))
        return self.assertNotRegex(self.driver.page_source, error)

    def random_word(self, length=6, chars=string.ascii_lowercase):
        word = ''.join(random.choice(chars) for i in range(length))
        self.log.debug("Generating random word: {}.".format(word))
        return word

    def random_number(self, length=3):
        number = ''.join(random.choice(string.digits) for i in range(length))
        self.log.debug("Generating random number: {}.".format(number))
        return number

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

    def page_has_loaded(self):
        self.log.info("Checking if {} page is loaded.".format(self.driver.current_url))
        page_state = self.driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    #def log(self, msg=None, level='info', **kwargs):
    #    levels = {
    #        'debug':   logging.debug,
    #        'info':    logging.info,
    #        'warning': logging.warning,
    #        'error':   logging.error
    #    }
    #    levels.get(level, logging.info)(msg)

    def make_screenshot(self, filename='screenshot'):
        self.driver.save_screenshot(filename)
        self.log.debug("Screenshot saved as {} at {}.".format(filename, self.driver.current_url))

    def tearDown(self):
        self.log.debug('Finishing up.')
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

    def kill(self):
        self.log.debug('Closing display.')
        self.vdisplay.stop()

    @property
    def failureException(self):
        class MyFailureException(AssertionError):
            def __init__(self_, *args, **kwargs):
                screenshot_dir = os.environ.get('REPORTS_DIR', self.args.dir) + '/screenshots'
                if not os.path.exists(screenshot_dir):
                    os.makedirs(screenshot_dir)
                self.driver.save_screenshot('{0}/{1}.png'.format(screenshot_dir, self.id()))
                return super(MyFailureException, self_).__init__(*args, **kwargs)
        MyFailureException.__name__ = AssertionError.__name__
        return MyFailureException


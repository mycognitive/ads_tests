from BaseTest import BaseTest
import time

class AdsTestRegistration(BaseTest):

    def register_user(self):
        driver = self.driver
        self.log.info("Creating new account.")
        driver.get(self.base_url + "/user/register")
        self.is_error_not_present()
        ymd = time.strftime("%Y%m%d")
        self.username = "test_" + self.random_word() + "_" + ymd
        self.password = "pass4" + self.username
        self.email = self.random_word() + "_" + ymd +  "@example.com"
        driver.find_element_by_id("edit-name--2").send_keys(self.username)
        driver.find_element_by_id("edit-mail").send_keys(self.email)
        driver.find_element_by_id("edit-conf-mail").send_keys(self.email)
        driver.find_element_by_id("edit-pass-pass1").send_keys(self.password)
        driver.find_element_by_id("edit-pass-pass2").send_keys(self.password)
        driver.find_element_by_id("edit-submit--2").click()
        self.assertRegex(self.driver.page_source, "Thank you for applying for an account|Log in successful")
        self.assertTrue(driver.find_element_by_xpath(u'//a[text()="Site map"]'))
        self.is_error_not_present()
        self.log.info("User {} ({}) created successfully.".format(self.username, self.email))
        return True

    def test_registration(self):
        driver = self.driver
        self.register_user()

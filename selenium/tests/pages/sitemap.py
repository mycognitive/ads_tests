from BaseTest import BaseTest

class AdsTestSitemap(BaseTest):

    def test_sitemap(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        self.is_error_not_present()

        driver.find_element_by_link_text("Site map").click()
        self.log.info("Sitemap page loaded successfully.")
        driver.find_element_by_xpath('//div[@id="main"]//a[text()="Register"]')
        self.log.info("Register link present.")
        self.is_error_not_present()


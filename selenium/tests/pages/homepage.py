from BaseTest import BaseTest

class AdsTestPagesBasic(BaseTest):

    def test_homepage(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        self.log.debug("Home page loaded.")

        self.assertTrue(self.is_text_present("Browse by category"))
        self.assertTrue(self.is_text_present("Browse by category"))
        self.is_error_not_present()

        link = driver.find_element_by_xpath(u'//a[contains(text(), "Site map")]')
        self.log.debug("Sitemap link present.")


from BaseTest import BaseTest

import time
from selenium.webdriver.support.ui import Select
import pdb

class AdsTestAnonPostAnAd(BaseTest):

    def post_an_ad(self, driver):
        title = "Lorem Ipsum"
        body = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus pharetra efficitur dui vitae interdum. " * 20
        verrors = "(?i)Error message|not a valid|You need to select"
        phone = "0200 123 1234"
        email = "foo@example.com"

        # Step 1
        Select(driver.find_element_by_css_selector("select.form-select.simpler-select")).select_by_visible_text("Art")
        Select(driver.find_element_by_xpath("//div[@id='field-ad-category-add-more-wrapper']/div/div[2]/select")).select_by_visible_text("General")
        image_path = self.cwd + "/assets/1x1px.svg"
        driver.find_element_by_id("edit-field-ad-image-und-0-upload").send_keys(image_path)
        driver.find_element_by_id("edit-next").click()
        self.is_error_not_present()
        self.is_error_not_present(verrors)

        # Step 2
        Select(driver.find_element_by_css_selector("select.form-select.simpler-select")).select_by_visible_text("UK")
        Select(driver.find_element_by_xpath("//div[@id='field-ad-location-add-more-wrapper']/div/div[2]/select")).select_by_visible_text("England")
        Select(driver.find_element_by_xpath("//div[@id='field-ad-location-add-more-wrapper']/div/div[3]/select")).select_by_visible_text("Greater London")
        Select(driver.find_element_by_xpath("//div[@id='field-ad-location-add-more-wrapper']/div/div[4]/select")).select_by_visible_text("Central London")
        Select(driver.find_element_by_xpath("//div[@id='field-ad-location-add-more-wrapper']/div/div[5]/select")).select_by_visible_text("Camden")
        Select(driver.find_element_by_xpath("//div[@id='field-ad-location-add-more-wrapper']/div/div[6]/select")).select_by_visible_text("Covent Garden")
        driver.find_element_by_id("edit-next").click()
        self.is_error_not_present()
        self.is_error_not_present(verrors)

        # Step 3
        driver.find_element_by_id("edit-title").send_keys(title)
        driver.find_element_by_id("edit-body-und-0-value").send_keys(body)
        driver.find_element_by_id("edit-field-ad-address-und-0-name-line").send_keys("Name")
        driver.find_element_by_id("edit-field-ad-address-und-0-organisation-name").send_keys("Company")
        driver.find_element_by_id("edit-field-ad-address-und-0-thoroughfare").send_keys("Address 1")
        driver.find_element_by_id("edit-field-ad-address-und-0-premise").send_keys("Address 2")
        driver.find_element_by_id("edit-field-ad-address-und-0-locality").send_keys("London")
        driver.find_element_by_id("edit-field-ad-address-und-0-administrative-area").send_keys("County")
        driver.find_element_by_id("edit-field-ad-address-und-0-postal-code").send_keys("NW1 6RH")
        driver.find_element_by_id("edit-field-ad-contact-method-und-phone").click()
        driver.find_element_by_id("edit-field-ad-phone-und-0-value").send_keys(phone)
        driver.find_element_by_id("edit-field-ad-contact-method-und-email").click()
        driver.find_element_by_id("edit-field-ad-email-und-0-email").send_keys(email)
        driver.find_element_by_id("edit-field-ad-contact-method-und-website").click()
        driver.find_element_by_id("edit-field-ad-link-und-0-title").send_keys("Example")
        driver.find_element_by_id("edit-field-ad-link-und-0-url").send_keys("http://example.com/")
        # @fixme: https://github.com/mycognitive/ads_features/issues/113
        #driver.find_element_by_id("edit-field-ad-link-und-add-more").click()
        #driver.find_element_by_id("edit-field-ad-link-und-1-title").send_keys("Example 2")
        #driver.find_element_by_id("edit-field-ad-link-und-1-url").send_keys("http://example.com/")
        #driver.find_element_by_id("edit-field-ad-link-und-add-more--2").click()
        #driver.find_element_by_id("edit-field-ad-link-und-2-title").send_keys("Example 3")
        #driver.find_element_by_id("edit-field-ad-link-und-2-url").send_keys("http://example.com/")

        driver.find_element_by_id("edit-next").click()
        self.is_error_not_present()
        self.is_error_not_present(verrors)
        
        # Preview
        for text in [title, "Example"]:
            self.assertTrue(self.is_text_present(text))
        driver.find_element_by_id("edit-return").click()

        # Advert page
        for text in [title, "Posted", "View"]:
            self.assertTrue(self.is_text_present(text))


    def test_post_an_ad(self):
        driver = self.driver
        driver.get(self.base_url + "/")
        self.is_error_not_present()

        driver.find_element_by_xpath(u'//a[text()="Post an ad"]').click()
        self.post_an_ad(driver)

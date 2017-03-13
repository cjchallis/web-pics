from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
import unittest
import requests
import shutil
import os

cur_path = os.path.realpath(__file__)
func = os.path.split(cur_path)[0]
web_pics = os.path.split(func)[0]
STATIC_ROOT = os.path.join(web_pics, "review", "static")

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)
        self.imgVerificationErrors = []
        # populate /testing from /staging
        self.testing = os.path.join(STATIC_ROOT, "review", "testing")
        self.staging = os.path.join(self.testing, "staging")
        for item in os.listdir(self.staging):
            full_path = os.path.join(self.staging, item)
            if os.path.isdir(full_path):
                shutil.copytree(full_path, os.path.join(self.testing, item))
            else:
                shutil.copy(full_path, self.testing)


    def tearDown(self):
        for item in os.listdir(self.testing):
            full_path = os.path.join(self.testing, item)
            if os.path.isdir(full_path):
                shutil.rmtree(full_path)
            else:
                os.remove(full_path)
            
        self.browser.quit()
        self.assertEqual([], self.imgVerificationErrors)


    def find_img(self, img):
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(img, header_text)
        images = self.browser.find_elements(By.TAG_NAME, 'img')
        self.assertIsNotNone(images)
        for image in images:
            current_link = image.get_attribute("src")
            r = requests.get(current_link)
            try: self.assertEqual(r.status_code, 200)
            except AssertionError as e: 
                self.imgVerificationErrors.append(
                    current_link + ' response code of ' + r.status_code) 



    def test_can_load_review_and_delete_pictures(self):
 
        # Hank heard about a new site to manage your pictures and goes to check it out
        self.browser.get(self.live_server_url)

        # He notices the page title and mentions picture review
        self.assertIn('Picture Management', self.browser.title)

        # The page header indicates a list of directories follows
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Picture Management', header_text)

        # There are options to review pictures and delete pictures
        review = self.browser.find_element_by_link_text('Review Pictures')
        delete = self.browser.find_element_by_link_text('Delete Selected Pictures')

        # He clicks on Review Pictures
        review.click()

        # He clicks on the 'testing' folder
        self.browser.find_element_by_link_text('testing/').click()

        # There is a list of folders and files to click on
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('/..', [row.text for row in rows])
        self.assertIn('dir0/', [row.text for row in rows])
        self.assertIn('pic0.png', [row.text for row in rows])

        # He clicks on a picture link, and the picture appears 
        self.browser.find_element_by_link_text('pic0.png').click()
        self.find_img('review/testing/pic0.png')

        # With the picture, there are options to keep, delete, previous, next
        keep = self.browser.find_element_by_link_text('keep')
        delete = self.browser.find_element_by_link_text('delete')
        previous = self.browser.find_element_by_link_text('previous')
        nxt = self.browser.find_element_by_link_text('next')

        # He clicks on next, a new picture appears
        nxt.click()
        self.find_img('review/testing/pic1.png')

        # He deletes the next picture, its status changes to 'To Delete'
        delete = self.browser.find_element_by_link_text('delete')
        delete.click()
        status = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual(status, 'To Delete')
        nxt = self.browser.find_element_by_link_text('next')
        nxt.click()

        # He keeps the last picture
        keep = self.browser.find_element_by_link_text('keep')
        keep.click()
        status = self.browser.find_element_by_tag_name('h2').text
        self.assertEqual(status, 'Saved')
        nxt = self.browser.find_element_by_link_text('next')
        nxt.click()

        # The first picture reappears - he keeps this one as well

        # A message appears that all pictures in this folder have been reviewed, and
        # he is taken to the home page

if __name__ == '__main__':
    unittest.main(warnings='ignore')


from review.models import PicFile

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)
        self.imgVerificationErrors = []

    def tearDown(self):
        self.browser.quit()
        self.assertEqual([], self.imgVerificationErrors)


    def find_img(self, img):
        self.browser.find_element_by_link_text(img).click()
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertEqual('review/pic0.png', header_text)
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
        self.browser.get('http://localhost:8000')

        # He notices the page title and mentions picture review
        self.assertIn('Review Pictures', self.browser.title)

        # The page header indicates a list of directories follows
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Picture Directories', header_text)

        # There is a list of folders to click on
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('review/', [row.text for row in rows])

        # When he clicks a folder, a list of filenames appears
        self.browser.find_element_by_link_text('review/').click()
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('pic0.png', [row.text for row in rows])

        # He clicks on a picture link, and the picture appears 
        self.find_img('pic0.png')

        # With the picture, there are options to keep, delete, previous, next
        keep = self.browser.find_element_by_link_text('keep')
        delete = self.browser.find_element_by_link_text('delete')
        previous = self.browser.find_element_by_link_text('previous')
        nxt = self.browser.find_element_by_link_text('next')

        # He clicks on next, a new picture appears
        nxt.click()
        self.find_img('pic1.png')

        # He deletes the next picture, a new picture appears
        nxt = self.browser.find_element_by_link_text('next')
        delete = self.browser.find_element_by_link_text('delete')
        delete.click()
        pic = PicFile.objects.filter(path = 'review/pic1.png')
        assertEqual(pic.status, 'to_delete')
        nxt.click()

        # He keeps the last picture
        nxt = self.browser.find_element_by_link_text('next')
        keep = self.browser.find_element_by_link_text('keep')
        keep.click()
        pic = PicFile.objects.filter(path = 'review/pic2.png')
        assertEqual(pic.status, 'keep')
        nxt.click()

        # The first picture reappears - he keeps this one as well

        # A message appears that all pictures in this folder have been reviewed, and
        # he is taken to the home page

if __name__ == '__main__':
    unittest.main(warnings='ignore')


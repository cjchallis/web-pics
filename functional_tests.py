from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

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
        self.assertIn('dir0', [row.text for row in rows])

        # When he clicks a folder, a list of filenames appears
        self.browser.find_element_by_link_text('dir0').click()
        self.fail('Finish the test!')

        # With the picture, there are options to keep, delete, or pass

        # He passes on the picture, a new picture appears

        # He deletes the next picture, a new picture appears

        # He keeps the last picture

        # The first picture reappears - he keeps this one as well

        # A message appears that all pictures in this folder have been reviewed, and
        # he is taken to the home page

if __name__ == '__main__':
    unittest.main(warnings='ignore')


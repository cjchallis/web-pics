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

        # He notices the page title and header mention picture review
        self.assertIn('Review Pictures', self.browser.title)

        # There is a list of folders to click on
        self.assertIn('<a href="link1">link1</a>', self.browser.page_source)
        self.assertIn('<a href="link2">link2</a>', self.browser.page_source)

        # When he clicks a folder, a list of filenames appears
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


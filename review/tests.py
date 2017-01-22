from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from review.views import home_page

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertIn('dir1', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'entries': ['<a href="dir0">dir0</a>',
                         '<a href="dir1">dir1</a>'],
            }
        )
        self.assertEqual(response.content.decode(), expected_html)


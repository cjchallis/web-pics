from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from review.views import view_dir 

class HomePageTest(TestCase):

    def test_root_url_resolves_to_view_dir(self):
        found = resolve('/')
        self.assertEqual(found.func, view_dir)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = view_dir(request, "", "")
        self.assertIn('dir1', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'entries': ['<a href="dir0/">dir0/</a>',
                         '<a href="dir1/">dir1/</a>'],
            }
        )
        self.assertEqual(response.content.decode(), expected_html)


    def test_dir_url_resolves_to_view_dir(self):
        found = resolve('/dir0/')
        self.assertEqual(found.func, view_dir)


    def test_dir_page_returns_correct_html(self):
        request = HttpRequest()
        response = view_dir(request, "", "dir0/")
        expected_html = render_to_string(
            'home.html',
            {'entries': ['<a href="dir00/">dir00/</a>',
                         '<a href="dir01/">dir01/</a>',
                         '<a href="pic0.jpg">pic0.jpg</a>',
                         '<a href="pic1.jpg">pic1.jpg</a>',
                        ],
            }
        )
        self.assertEqual(response.content.decode(), expected_html)


from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from review.views import view_dir 


class HomePageTest(TestCase):

    def test_home_uses_dir_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_dir_uses_dir_template(self):
        response = self.client.get('/review/')
        self.assertTemplateUsed(response, 'home.html')


    def test_file_uses_img_template(self):
        response = self.client.get('/review/pic0.jpg')
        self.assertTemplateUsed(response, 'img.html')


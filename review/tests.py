from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from review.models import PicFile
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

class StatusModelTest(TestCase):

    def test_saving_and_retrieving_files(self):
        first_file = PicFile()
        first_file.path = '/review/pic0.png'
        first_file.status = 'Unreviewed'
        first_file.save()

        second_file = PicFile()
        second_file.path = '/review/pic1.png'
        second_file.status = 'Unreviewed'
        second_file.save()

        saved_files = PicFile.objects.all()
        self.assertEqual(saved_files.count(), 2)

        first_saved_file = saved_files[0]
        second_saved_file = saved_files[1]
        self.assertEqual(first_saved_file.status, 'Unreviewed')
        self.assertEqual(second_saved_file.path, '/review/pic1.png')


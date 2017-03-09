from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from review.models import PicFile
from review.views import view_dir 


class PageTest(TestCase):

    def test_home_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


    def test_dir_uses_dir_template(self):
        response = self.client.get('/review/')
        self.assertTemplateUsed(response, 'dir.html')


    def test_file_uses_img_template(self):
        response = self.client.get('/review/pic0.jpg')
        self.assertTemplateUsed(response, 'img.html')


    def test_del_list_uses_del_template(self):
        response = self.client.get('/deletion_list')
        self.assertTemplateUsed(response, 'del_list.html')


class DeletionTest(TestCase):

    def test_delete_list(self):
        first_file = PicFile()
        first_file.path = 'review/pic0.png'
        first_file.status = "delete"
        first_file.save()

        sec_file = PicFile()
        sec_file.path = 'review/pic1.png'
        sec_file.status = "delete"
        sec_file.save()

        thr_file = PicFile()
        thr_file.path = 'review/pic2.png'
        thr_file.path = 'Saved'
        thr_file.save()

        response = self.client.get('/deletion_list')
        self.assertContains(response, 'review/pic0.png')
        self.assertContains(response, 'review/pic1.png')
        self.assertNotContains(response, 'review/pic2.png')


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


from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
import os

from review.models import PicFile
from review.views import view_dir 

STATIC_PATH = os.path.join("/", "home", "pi", "tdd", "web_pics", "review",
                           "static")

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

        path0 = 'review/pic0.png'
        path1 = 'review/pic5.png'
        path2 = 'review/pic6.png'
        full_path0 = os.path.join(STATIC_PATH, path0)
        full_path1 = os.path.join(STATIC_PATH, path1)
        full_path2 = os.path.join(STATIC_PATH, path2)
        if not os.path.exists(full_path1):
            os.mknod(full_path1)
        if not os.path.exists(full_path2):
            os.mknod(full_path2)

        first_file = PicFile()
        first_file.path = path0 
        first_file.status = "keep"
        first_file.save()

        sec_file = PicFile()
        sec_file.path = path1 
        sec_file.status = "delete"
        sec_file.save()

        thr_file = PicFile()
        thr_file.path = path2 
        thr_file.status = 'delete' 
        thr_file.save()

        response = self.client.get('/deletion_list')
        print(response.content)
        self.assertNotContains(response, path0)
        self.assertContains(response, path1)
        self.assertContains(response, path2)

        response = self.client.get('/run_deletion')
        self.assertTrue(os.path.exists(full_path0))
        self.assertFalse(os.path.exists(full_path1))
        self.assertFalse(os.path.exists(full_path2))


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


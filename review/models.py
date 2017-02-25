from django.db import models

class PicFile(models.Model):
    path = models.TextField(default='')
    status = models.TextField(default='')


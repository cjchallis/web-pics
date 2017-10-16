from django.db import models

class PicFile(models.Model):
    UNREVIEWED = 'UN'
    KEEP = 'KP'
    CHATBOOKS = 'CH'
    DELETE = 'DL'
    STATUS_CHOICES = (
        (UNREVIEWED, 'minus'),
        (KEEP, 'floppy-disk'),
        (CHATBOOKS, 'heart'),
        (DELETE, 'trash'),
    )
    IMAGE = 'PIC'
    VIDEO = 'VID'
    TYPE_CHOICES = (
        (IMAGE, 'image'),
        (VIDEO, 'video'),
    )
    path = models.TextField(default='')
    name = models.TextField(default='')
    thumbnail = models.TextField(default='')
    filetype = models.CharField(
        max_length=3,
        choices=TYPE_CHOICES,
        default=IMAGE,
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=UNREVIEWED,
    )


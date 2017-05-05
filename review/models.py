from django.db import models

class PicFile(models.Model):
    UNREVIEWED = 'UN'
    KEEP = 'KP'
    CHATBOOKS = 'CH'
    DELETE = 'DL'
    STATUS_CHOICES = (
        (UNREVIEWED, 'trash'),
        (KEEP, 'floppy-disk'),
        (CHATBOOKS, 'heart'),
        (DELETE, 'trash'),
    )
    path = models.TextField(default='')
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=UNREVIEWED,
    )


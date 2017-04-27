from django.db import models

class PicFile(models.Model):
    UNREVIEWED = 'UN'
    KEEP = 'KP'
    CHATBOOKS = 'CH'
    DELETE = 'DL'
    STATUS_CHOICES = (
        (UNREVIEWED, 'Unreviewed'),
        (KEEP, 'Keep'),
        (CHATBOOKS, 'Chatbooks'),
        (DELETE, 'Delete'),
    )
    path = models.TextField(default='')
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=UNREVIEWED,
    )


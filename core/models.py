from django.db import models
from enum import Enum

# Create your models here.
class VideoFile(models.Model):
    """
    A class for uploading video to the server.
    """

    def forDjango(cls):
        cls.do_not_call_in_templates = True
        return cls

    @forDjango
    class VideoFileStatus(Enum):
        NEW = 1
        PROCESSING = 4
        READY = 7

    file = models.FileField(upload_to="", max_length=1024)  # If upload_to=="" then file will be uploaded to the MEDIA_ROOT path set in settings.
    uploaded_at = models.DateTimeField(auto_now_add=True)
    fps = models.IntegerField(default=25)
    video_width = models.IntegerField(default=0, blank=True)
    video_height = models.IntegerField(default=0, blank=True)
    status = models.IntegerField(default=VideoFileStatus.NEW.value)
    output_file = models.FileField(upload_to="", max_length=1024, blank=True)
    csv_file = models.FileField(upload_to="", max_length=1024, blank=True)


    @property
    def url(self):
        return self.file.url


class WTV2D_data(models.Model):
    processing = models.BooleanField(default=False, blank=False)


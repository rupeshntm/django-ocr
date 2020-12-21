from django.db import models
import cv2

# Create your models here.

class FilesUpload(models.Model):
    file = models.FileField()
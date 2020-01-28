from django.db import models
from django.utils import timezone
# Create your models here.


class Camera_One_Image(models.Model):
    name = models.CharField(max_length=200)
    #image = models.ImageField(upload_to='camera_one_images')
    image_url = models.CharField(max_length=1000, default="https://i.picsum.photos/id/113/536/354.jpg")
    down_time = models.CharField(max_length=100,default="19 10 1997 05:35")
    down_date = models.CharField(max_length=100,default="19 10 1997")
    created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.name


class Camera_Two_Image(models.Model):
    name = models.CharField(max_length=200)
    #image = models.ImageField(upload_to='camera_two_images')
    image_url = models.CharField(max_length=1000, default="https://i.picsum.photos/id/113/536/354.jpg")
    down_time = models.CharField(max_length=100, default="19 10 1997 05:35")
    down_date = models.CharField(max_length=100, default="19 10 1997")
    created = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.name


class StateModel(models.Model):
    camera_one = models.CharField(max_length=200,default='empty')
    camera_two = models.CharField(max_length=200,default='empty')
    updated = models.DateTimeField(auto_now = True)




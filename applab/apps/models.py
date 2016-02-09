from django.db import models

class App(models.Model):
    app_id = models.IntegerField()
    title = models.TextField()
    short_desc = models.TextField()
    desc  = models.TextField()
    version = models.CharField(max_length=20)
    platform = models.TextField()
    release_date = models.DateField()
    sunset_date = models.DateField()
    app_icon_path = models.TextField()
    author = models.TextField()
    author_contact = models.EmailField



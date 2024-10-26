from django.db import models

# Create your models here.
class message(models.Model):
    text = models.TextField()
    pub_time = models.TimeField(auto_now=True)
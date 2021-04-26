from django.db import models

# Create your models here.

class API_KEY(models.Model):
    key = models.CharField(max_length=50, blank=False, null=True, unique=True)
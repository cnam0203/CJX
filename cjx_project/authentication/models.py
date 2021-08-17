from django.db import models
import jwt

# Create your models here.
SECRET_KEY = 'cjx_project'

class API_KEY(models.Model):
    key = models.CharField(max_length=200, blank=False, null=True, unique=True)

    def save(self, *args, **kwargs):
        self.key = jwt.encode({"key": self.key}, SECRET_KEY, algorithm="HS256")
        super(API_KEY, self).save(*args, **kwargs)

        
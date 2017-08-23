from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)

    urecipients = models.CharField(max_length=20, default='')
    udelivery_address = models.CharField(max_length=100, default='')
    upostcode = models.CharField(max_length=6, default='')
    uphone_number = models.CharField(max_length=11, default='')
from django.db import models
from django.contrib.auth.models import User


class th_districts(models.Model):
    id = models.AutoField(primary_key=True)
    zip_code = models.CharField(max_length=255)
    name_th = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    amphure_id = models.CharField(max_length=255)



class brooks_match_qrcode(models.Model):
    id = models.AutoField(primary_key=True)
    temp_type = models.CharField(max_length=255)
    date_match = models.CharField(max_length=255)
    specimen_id = models.IntegerField()
    specimen_qrcode = models.CharField(max_length=255)
    brooks_qrcode = models.CharField(max_length=255)
    user_match = models.CharField(max_length=255)

class generated_qrcode(models.Model):
    id = models.AutoField(primary_key=True)
    times = models.IntegerField()
    qrcode = models.CharField(max_length=255)
    size = models.CharField(max_length=255)
    duplicate = models.IntegerField()
    date_create = models.DateField(null = True, blank=True)
    user_create = models.IntegerField()

    """ ################################################################################ """
    


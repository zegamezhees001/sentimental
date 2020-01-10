from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from Team.models import TeamModel




class Permission(models.Model):
    id_permission = models.AutoField(primary_key=True)
    name_permission = models.CharField(max_length=255 , unique=True)

class Attachment(models.Model):
    id_attachment = models.AutoField(primary_key=True,unique=True)
    name_attachment = models.CharField(max_length=255 ,unique=True)
    id_permission = models.ForeignKey(Permission , null=False , on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="images/", default="media/photos/image.jpg")
    id_attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    tel = models.CharField(max_length=15, blank=True)
    employeeID = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)


class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    last_login = models.DateTimeField(null=True, blank=True )

class Role_user(models.Model):
    id_role = models.AutoField(primary_key=True)
    id_team = models.ForeignKey(TeamModel, null=False , on_delete=models.CASCADE)
    id_user = models.ForeignKey(User , null=False , on_delete=models.CASCADE)
    id_attachment = models.ForeignKey(Attachment , null=False , on_delete=models.CASCADE)
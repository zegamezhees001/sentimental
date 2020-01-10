from django.db import models
from django.utils import timezone
# Create your models here.
class TeamModel(models.Model):
    id_team = models.AutoField(primary_key=True)
    name_team = models.CharField(max_length=255 , null=False)
    create_date = models.DateTimeField(default=timezone.now)

from django.db import models

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "event"
        verbose_name = "イベント"
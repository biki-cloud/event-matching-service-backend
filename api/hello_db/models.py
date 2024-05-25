from django.db import models

# Create your models here.


class Hello(models.Model):
    word = models.CharField(max_length=100)

    class Meta:
        db_table = "hello_db"
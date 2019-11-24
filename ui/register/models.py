from django.db import models

# Create your models here.
class register(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    mqttuser=models.CharField(max_length=100)
    mqttpass=models.CharField(max_length=100)
    port=models.IntegerField()


    def __str__(self):
        return self.username

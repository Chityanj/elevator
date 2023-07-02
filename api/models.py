from django.db import models

# Create your models here.
class Elevator(models.Model):
    current_floor = models.PositiveIntegerField(default=1)
    door_opened = models.BooleanField(default=False)
    in_maintenance = models.BooleanField(default=False)

    def __str__(self):
        return f"Elevator {self.pk}"
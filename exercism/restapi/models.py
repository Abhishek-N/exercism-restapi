from django.db import models

# Create your models here.


class Users(models.Model):
    name = models.CharField(max_length=100)
    owes = models.JSONField(blank=True)
    owed_by = models.JSONField(blank=True)
    balance = models.FloatField(blank=True)

    class Meta:
        db_table = "users"
        ordering = ["name"]

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    owes = models.JSONField(default=dict)
    owed_by = models.JSONField(default=dict)
    balance = models.FloatField(default=0.0)

    class Meta:
        db_table = "users"
        ordering = ["name"]

    def __str__(self):
        return self.name

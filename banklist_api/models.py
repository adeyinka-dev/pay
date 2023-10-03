from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=255)
    logo = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

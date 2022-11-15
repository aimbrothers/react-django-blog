from django.db import models


class Tag(models.Model):
    label = models.CharField(max_length=64)

    def __str__(self):
        return self.label

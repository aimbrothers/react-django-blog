from django.db import models

from backend.utils.models import BaseModel


class Tag(BaseModel):
    label = models.CharField(max_length=64)

    def __str__(self):
        return self.label

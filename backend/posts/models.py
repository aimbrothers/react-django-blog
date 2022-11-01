from django.db import models

from users.models import BackendUser


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(BackendUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

    @property
    def author(self):
        return self.user.username
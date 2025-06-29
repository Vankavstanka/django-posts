from django.db import models

class Post(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    body = models.TextField()
    userId = models.IntegerField()

    def __str__(self) -> str:        # отображение в админке
        return f"{self.id}: {self.title[:30]}"

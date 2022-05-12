from django.db import models
from django.contrib.auth import get_user_model
from django_extensions.db.fields import AutoSlugField

# Create your models here.

USER_MODEL = get_user_model()


class Article(models.Model):
    author = models.ForeignKey(to=USER_MODEL, related_name='author', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    slug = AutoSlugField(populate_from=['title'])
    status = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    @property
    def is_online(self) -> bool:
        if self.status:
            return True
        return False

    def switch_status(self) -> None:
        self.status = not self.status
        self.save()

    def __str__(self) -> str:
        return f'{self.author} -> {self.slug} at {self.pub_date}'




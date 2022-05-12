from django.db import models


# Create your models here.

class Contact(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100,)
    content = models.CharField(max_length=500,)
    created_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self) -> str:
        return f'{self.name} ({self.email}) at {self.created_at}'

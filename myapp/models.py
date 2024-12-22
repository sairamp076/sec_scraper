from django.db import models

class Company(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=255)
    cik = models.CharField(max_length=10, unique=True)
    downloaded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ticker} - {self.title}"

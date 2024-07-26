from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=100)
    institution_number = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT)

class Branch(models.Model):
    name = models.CharField(max_length=100)
    transit_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField(default='admin@utoronto.ca')
    capacity = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.last_modified = timezone.now()
        return super(Branch, self).save(*args, **kwargs)

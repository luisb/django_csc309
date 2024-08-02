from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Bank(models.Model):
    name = models.CharField(max_length=100)
    swift_code = models.CharField(max_length=100)
    institution_number = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.RESTRICT)

    def get_absolute_url(self):
        return reverse("bank-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.name
    

class Branch(models.Model):
    name = models.CharField(max_length=100)
    transit_number = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField(default='admin@utoronto.ca')
    capacity = models.IntegerField(null=True, blank=True)
    last_modified = models.DateTimeField()
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Branches"

    def save(self, *args, **kwargs):
        self.last_modified = timezone.now()
        return super(Branch, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("branch-detail", kwargs={"pk": self.pk})

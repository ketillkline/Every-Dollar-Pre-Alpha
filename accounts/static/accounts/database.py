from django.db import models
from django.contrib.auth.models import User


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    date = models.DateField(null=True, blank=True)
    value = models.FloatField()
    method = models.CharField()
    frequency = models.CharField()
    category = models.CharField()
    description = models.CharField(max_length=200)


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    amount = models.FloatField()
    pay_day = models.CharField(max_length=2)

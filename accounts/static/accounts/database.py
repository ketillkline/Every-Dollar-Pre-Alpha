from django.db import models

class Frequency(models.Model):
    label = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.label

class Method(models.Model):
    pass

class Category(models.Model):
    pass
class Income(models.Model):
    name = models.CharField()
    date = models.DateField(null=True, blank=True)
    value = models.FloatField()
    method = models.CharField()
    frequency = models.CharField()
    category = models.CharField()
    description = models.CharField(max_length=200)

class Expense(models.Model):
    name = models.CharField()
    date = models.DateField(null=True, blank=True)
    value = models.FloatField()
    method = models.CharField()
    frequency = models.CharField()
    category = models.CharField()
    description = models.CharField(max_length=200)

from django.db import models

# Create your models here.


class Company(models.Model):
    company = models.CharField(max_length=64)
    fact_Qliq_data1 = models.IntegerField()
    fact_Qliq_data2 = models.IntegerField()
    fact_Qoil_data1 = models.IntegerField()
    fact_Qoil_data2 = models.IntegerField()
    forecast_Qliq_data1 = models.IntegerField()
    forecast_Qliq_data2 = models.IntegerField()
    forecast_Qoil_data1 = models.IntegerField()
    forecast_Qoil_data2 = models.IntegerField()

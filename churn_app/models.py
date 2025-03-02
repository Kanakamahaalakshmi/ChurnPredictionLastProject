from django.db import models
from django.db import models

class ChurnPrediction(models.Model):
    customer_id = models.CharField(max_length=50)
    tenure = models.FloatField()
    monthly_charges = models.FloatField()
    total_charges = models.FloatField()
    prediction = models.CharField(max_length=10)  # "Churn" or "No Churn"

    def __str__(self):
        return f"Customer {self.customer_id} - {self.prediction}"

# Create your models here.

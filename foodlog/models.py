from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models



class FoodlogModel(models.Model):
    title = models.CharField(max_length=100)
    calorie = models.PositiveIntegerField()
    MEAL_TYPE = [
                    ("BF","BF"),
                    ("Lunch","Lunch"),
                    ("Dinner","Dinner"),
                    ("Snacks","Snacks")
    ]
    
    meal_type = models.CharField(max_length=10,choices=MEAL_TYPE,default="Snacks")
    serving_size = models.CharField(max_length=100)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="foodlog")
    created_at = models.DateTimeField(auto_now_add=True)
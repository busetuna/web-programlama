from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'dietitian'),
        (2, 'client'),
    )
    GOAL_CHOICES = (
        ('gain_weight', 'Kilo Alma'),
        ('lose_weight', 'Kilo Verme'),
        ('maintain_weight', 'Form Koruma'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, null=True)
    assigned_dietitian = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'user_type': 1})
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

class NutritionPlan(models.Model):
    dietitian = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='plans')
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='nutrition_plans')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

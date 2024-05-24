from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,NutritionPlan
from django.contrib.auth.models import Group
from django import forms

class NutritionPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = ['client', 'title', 'description']

    
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name','email','goal', 'password1', 'password2', 'email','age','weight')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 2  # client
        user.is_staff = True
        if commit:
            user.save()
            group = Group.objects.get(name='client')
            user.groups.add(group)
        return user
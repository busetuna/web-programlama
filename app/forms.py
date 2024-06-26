from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,NutritionPlan
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class NutritionPlanForm(forms.ModelForm):
    class Meta:
        model = NutritionPlan
        fields = ['title', 'description', 'client']
        
    def __init__(self, *args, **kwargs):
        dietitian = kwargs.pop('dietitian', None)
        super().__init__(*args, **kwargs)
        if dietitian:
            self.fields['client'].queryset = CustomUser.objects.filter(assigned_dietitian=dietitian)


    
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
    

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))    
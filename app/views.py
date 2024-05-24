from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView
from .models import NutritionPlan
from .forms import CustomUserCreationForm
from django.contrib.auth import login as auth_login
from .models import *
import random
class DietitianRequiredMixin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.user_type == 1

class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 2

def index(request):
    return render(request, "index.html")

def login(request):
    return redirect('admin:login')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 2  # client
            user.is_staff=True
            user.save()

            if user.user_type == 2:  # client
                dietitians = CustomUser.objects.filter(user_type=1, goal=user.goal)  
                if dietitians.exists():
                    assigned_dietitian = random.choice(dietitians)  
                    user.assigned_dietitian = assigned_dietitian
                    user.save() 

            return redirect('index')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
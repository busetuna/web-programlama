from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, ListView, DetailView
from .models import NutritionPlan
from .forms import CustomUserCreationForm, NutritionPlanForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from .models import *
import random
class DietitianRequiredMixin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.user_type == 1

class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.user_type == 2

@login_required
def index(request):
    if request.user.user_type == 1:  # Eğer kullanıcı bir diyetisyen ise
        assigned_users = CustomUser.objects.filter(assigned_dietitian=request.user.id)
        nutrition_plans = NutritionPlan.objects.filter(dietitian=request.user)

        context = {
            'assigned_users': assigned_users,
            'nutrition_plans': nutrition_plans,
        }
        return render(request, 'home_dietitian.html', context)
    elif request.user.user_type == 2:
        assigned_plans = NutritionPlan.objects.filter(client=request.user)

        context = {
            'assigned_plans': assigned_plans,
        }
        return render(request, 'home_user.html', context)
    else:
        return HttpResponse("Hoş geldiniz!")  # Eğer kullanıcı admin ya da tanımsız bir rolde ise

@login_required
def assign_nutrition_plan(request):
    if request.user.user_type != 1:
        return HttpResponse("Bu sayfaya erişim izniniz yok.")

    if request.method == 'POST':
        form = NutritionPlanForm(request.POST, dietitian=request.user)
        if form.is_valid():
            nutrition_plan = form.save(commit=False)
            nutrition_plan.dietitian = request.user
            nutrition_plan.save()
            return redirect('index')
    else:
        form = NutritionPlanForm(dietitian=request.user)

    return render(request, 'assign_nutrition_plan.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Giriş başarılı olursa ana sayfaya yönlendir
        else:
            return HttpResponse("Geçersiz giriş")  # Giriş başarısız olursa hata mesajı 
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')

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


def search_recipe(request):
    api_id = "63b31812"
    api_key = "61d97eef2e3e04acbbe8eadefd2b06d9"
    query = request.GET.get('query', '')
    url = f"https://api.edamam.com/search?q={query}&app_id={api_id}&app_key={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        recipes = []
        for hit in data['hits']:
            recipe = {
                'name': hit['recipe']['label'],
                'ingredients': hit['recipe']['ingredientLines']
            }
            recipes.append(recipe)
        return render(request, "search_recipe.html", {"recipes": recipes})
    else:
        print("Hata:", response.status_code)
        return None
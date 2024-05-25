from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('login_view',views.login_view,name='login_view'),
    path('signup',views.register,name='signup'),
    path('home',views.home,name='home'),
    path('assign-nutrition-plan', views.assign_nutrition_plan, name='assign_nutrition_plan'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('weight_entry', views.weight_entry, name='weight_entry'),
    path('plan_view/', views.plan_view, name='plan_view'),
    path('client_view/', views.client_view, name='client_view'),
    path('search_recipe', views.search_recipe, name='search_recipe'),
]
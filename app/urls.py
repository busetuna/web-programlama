from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("login/",views.login_view,name='login'),
    path("signup/",views.register,name='signup'),
    path('assign-nutrition-plan/', views.assign_nutrition_plan, name='assign_nutrition_plan'),
    path('logout/', views.logout_view, name='logout'),
]
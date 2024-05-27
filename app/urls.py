from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from django.urls import path

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
    path('set-session/', views.set_session, name='set_session'),
    path('get-session/', views.get_session, name='get_session'),
    path('delete-session/', views.delete_session, name='delete_session'),
    path('set-cookie/', views.set_cookie, name='set_cookie'),
    path('get-cookie/', views.get_cookie, name='get_cookie'),
    path('delete-cookie/', views.delete_cookie, name='delete_cookie'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', CustomLoginView.as_view(), name='login'),
]
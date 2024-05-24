from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, NutritionPlan
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm
from django.utils.translation import gettext, gettext_lazy as _
import random
from .forms import NutritionPlanForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'user_type','goal','assigned_dietitian')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type','goal','assigned_dietitian', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
    list_display = ('username', 'email', 'user_type', 'is_staff','assigned_dietitian')
    search_fields = ('username', 'email')
    ordering = ('username',)
    def save_model(self, request, obj, form, change):
        if obj.user_type == 2:  # client
            dietitians = CustomUser.objects.filter(user_type=1, goal=obj.goal)  # goal ile uyumlu diyetisyenler
            if dietitians.exists():
                assigned_dietitian = random.choice(dietitians)  # Rastgele bir diyetisyen seçme
                obj.assigned_dietitian = assigned_dietitian
                obj.save()
        super().save_model(request, obj, form, change)

    
    
class NutritionPlanAdmin(admin.ModelAdmin):
    model = NutritionPlan
    form=NutritionPlanForm
    list_display = ('title', 'dietitian', 'client', 'created_at')
    list_filter = ('dietitian', 'client')
    search_fields = ('title', 'dietitian__username', 'client__username')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if request.user.user_type == 1:
            return qs.filter(dietitian=request.user)
        elif request.user.user_type == 2:
            return qs.filter(client=request.user)
        return qs.none() 


    def save_model(self, request, obj, form, change):
        if not obj.pk and not request.user.is_superuser:
            obj.dietitian = request.user
        else:
            obj.dietitian = form.cleaned_data['dietitian']
        super().save_model(request, obj, form, change)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'dietitian' and request.user.user_type==1:
            kwargs["queryset"] = CustomUser.objects.filter(id=request.user.id)
        elif db_field.name == 'client':
            
            kwargs["queryset"] = CustomUser.objects.filter(assigned_dietitian=request.user)
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

@receiver(post_save, sender=get_user_model())
def assign_user_to_group(sender, instance, created, **kwargs):
    if created:
        user = instance
        if user.user_type == 1:
            group, _ = Group.objects.get_or_create(name='dietitian')
            user.groups.add(group)
            assign_permissions(group, 'dietitian')
        elif user.user_type == 2:
            group, _ = Group.objects.get_or_create(name='client')
            user.groups.add(group)
            assign_permissions(group, 'client')

def assign_permissions(group, user_type):
    content_type = ContentType.objects.get_for_model(NutritionPlan)
    if user_type == 'dietitian':
        # Dietitian should have all permissions
        permissions = Permission.objects.filter(content_type=content_type)
    elif user_type == 'client':
        # Client should have only view permission
        permissions = Permission.objects.filter(content_type=content_type, codename='view_nutritionplan')

    for perm in permissions:
        group.permissions.add(perm)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(NutritionPlan, NutritionPlanAdmin)

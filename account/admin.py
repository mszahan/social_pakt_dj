from django.contrib import admin
from .models import *



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'image']







# only for check up no use here
# @admin.register(PortfolioPricing)
# class CustomerModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'package_name', 'price', 'category']

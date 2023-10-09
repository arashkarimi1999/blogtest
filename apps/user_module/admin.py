from django.contrib import admin
from .models import User,Avatar
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


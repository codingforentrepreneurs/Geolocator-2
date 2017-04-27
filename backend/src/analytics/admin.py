from django.contrib import admin

# Register your models here.
from .models import UserSession

admin.site.register(UserSession)
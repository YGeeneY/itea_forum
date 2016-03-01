from django.contrib import admin
from .models import UserDetails, UserMessages

# Register your models here.

admin.site.register(UserDetails)
admin.site.register(UserMessages)
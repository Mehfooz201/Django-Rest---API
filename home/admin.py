from django.contrib import admin
from .models import Person, Color

# Register your models here.

admin.site.register(Color)

admin.site.register(Person)

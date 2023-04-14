from django.contrib import admin

from .models import Category, Graphic

# Register the Graphic and Category models with the admin site
admin.site.register(Graphic)
admin.site.register(Category)

# register the ImageUpload model in photos/admin.py:
from django.contrib import admin

from .models import ImageUpload

admin.site.register(ImageUpload)

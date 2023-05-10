from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ImageUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField("image")
    public_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image {self.id} uploaded by {self.user.username}"

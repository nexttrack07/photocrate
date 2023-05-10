from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from graphics.viewsets import CategoryViewSet, GraphicViewSet
from photocrate.users.api.views import UserViewSet
from photos.views import BackgroundRemovalPrediction, ImageUploadListAPIView, UploadView

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"graphics", GraphicViewSet, basename="graphic")

urls = [
    path("upload-image/", UploadView.as_view(), name="upload-image"),
    path("images", ImageUploadListAPIView.as_view(), name="images"),
    path(
        "remove_background/",
        BackgroundRemovalPrediction.as_view(),
        name="remove_background",
    ),
    path(
        "remove_background/<str:id>",
        BackgroundRemovalPrediction.as_view(),
        name="remove_background",
    ),
]

app_name = "api"
urlpatterns = router.urls

urlpatterns.extend(urls)

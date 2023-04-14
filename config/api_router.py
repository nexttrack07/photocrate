from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from graphics.viewsets import CategoryViewSet, GraphicViewSet
from photocrate.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"graphics", GraphicViewSet, basename="graphic")

app_name = "api"
urlpatterns = router.urls

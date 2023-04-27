from django.urls import path

from search.views import SearchGraphics

urlpatterns = [
    path("graphics/<str:query>/", SearchGraphics.as_view()),
]

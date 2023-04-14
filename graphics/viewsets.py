from rest_framework import viewsets

from .models import Category, Graphic
from .serializers import CategorySerializer, GraphicSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GraphicViewSet(viewsets.ModelViewSet):
    queryset = Graphic.objects.all()
    serializer_class = GraphicSerializer

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, RoomViewSet

router = DefaultRouter()
router.register(r'', PropertyViewSet, basename='property')
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]
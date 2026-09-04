# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import PropertyViewSet, RoomViewSet

# router = DefaultRouter()
# router.register(r'', PropertyViewSet, basename='property')
# router.register(r'rooms', RoomViewSet, basename='room')

# urlpatterns = [
#     path('', include(router.urls)),
# ]

from django.urls import path
from .views import PropertyViewSet, RoomViewSet

property_list = PropertyViewSet.as_view({'get': 'list', 'post': 'create'})
property_detail = PropertyViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

room_list = RoomViewSet.as_view({'get': 'list', 'post': 'create'})
room_detail = RoomViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})

urlpatterns = [
    path('', property_list, name='property-list'),
    path('<int:pk>/', property_detail, name='property-detail'),
    path('rooms/', room_list, name='room-list'),
    path('rooms/<int:pk>/', room_detail, name='room-detail'),
]
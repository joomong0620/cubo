from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, HeaterViewSet, MoodLightStatusViewSet,
    SensorStatusViewSet, CryDetectionViewSet
)

router = DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'heater', HeaterViewSet)
router.register(r'moodlight', MoodLightStatusViewSet)
router.register(r'sensor', SensorStatusViewSet)
router.register(r'cry', CryDetectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

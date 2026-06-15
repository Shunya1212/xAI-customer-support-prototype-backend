from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.specie import views


router = DefaultRouter()
router.register('specie', views.SpecieViewSet)
router.register('growth-state', views.GrowthStateViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
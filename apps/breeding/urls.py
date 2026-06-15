from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.breeding import views


router = DefaultRouter()
router.register('breeding-pair', views.BreedingPairViewSet)
router.register('egg-batch', views.EggBatchViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
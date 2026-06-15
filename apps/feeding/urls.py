from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.feeding import views


router = DefaultRouter()
router.register('food', views.FoodViewSet, basename='food')
router.register('feeding-plan', views.FeedingPlanViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
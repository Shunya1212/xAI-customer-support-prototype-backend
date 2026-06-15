from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.animal import views


router = DefaultRouter()
router.register('animal', views.AnimalViewSet, basename='animal')


urlpatterns = [
    path('', include(router.urls)),
    path('size-log-transaction/', views.SizeLogTransactionView.as_view(), name='sizelog-list'),
    path('dead-log-transaction/', views.DeadLogTransactionView.as_view(), name='deadlog-list'),
]
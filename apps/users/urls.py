from django.urls import path, include
from apps.users import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('user', views.UserViewset, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.CustomObtainJSONWebToken.as_view(), name='login'),
    path('sign-out/', views.SignOut.as_view(), name='sign-out'),
    path('change-password/', views.ChangePassword.as_view(), name='change-password'),
]

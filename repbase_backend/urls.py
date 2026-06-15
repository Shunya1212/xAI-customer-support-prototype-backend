"""
URL configuration for repbase_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/animal/', include('apps.animal.urls')),
    path('api/specie/', include('apps.specie.urls')),
    path('api/breeding/', include('apps.breeding.urls')),
    path('api/feeding/', include('apps.feeding.urls')),
    path('api/users/', include('apps.users.urls')),
    # path('api/health/', include('apps.health.urls')),
    # path('api/member/', include('apps.member.urls')),
    # path('api/facility/', include('apps.facility.urls'))
]

admin.site.site_header = 'RepBase App Administration'
admin.site.index_title = 'RepBase App Admin'
admin.site.site_title = 'RepBase App Administration'
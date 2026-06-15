from django.contrib import admin

class BaseTabularInline(admin.TabularInline):
    extra = 0
    def get_queryset(self, request):
        return super().get_queryset(request).actives()

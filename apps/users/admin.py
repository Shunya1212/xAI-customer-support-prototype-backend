from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'first_name', 'last_name', 'group_display', 'is_active']
    search_fields = ['username', 'first_name', 'last_name']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'groups']
    readonly_fields = get_user_model().base_attrs()
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email', )
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    filter_horizontal = UserAdmin.filter_horizontal
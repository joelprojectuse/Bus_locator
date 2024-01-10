from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {
         'fields': ('Name', 'DOB', 'phone', 'role', 'sector', 'depo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'Name', 'DOB', 'phone', 'role', 'sector', 'depo', 'password1', 'password2'),
        }),
    )
    # Add filter_horizontal for user_permissions
    filter_horizontal = ('user_permissions',)
    list_display = ('username', 'email', 'role', 'is_staff')
    search_fields = ('username', 'email', 'role', 'phone')
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Route)
admin.site.register(DriverLocation)

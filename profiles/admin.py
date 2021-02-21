from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields':('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'gender')}),
        (_('Contacts'), {'fields': ('phone_no', 'location', 'picture')}),
        (_('Permissions'), {'fields':('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important Dates'), {'fields':('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None,{
            'classes':('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(get_user_model(), CustomUserAdmin)

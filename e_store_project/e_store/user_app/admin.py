from django.contrib import admin
from user_app.models import User, Role, UserRoles, BlacklistedToken
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
                        'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',
                       'first_name', 'last_name', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    ordering = ('id',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(UserRoles)
admin.site.register(BlacklistedToken)

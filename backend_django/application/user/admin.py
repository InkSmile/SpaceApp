from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'created_at', 'last_login', 'is_admin', 'is_staff', 'is_active')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'last_login')

    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    add_fieldsets = (
        (
            None,
            {   
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

admin.site.register(User, CustomUserAdmin)




from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from accounts.models import userDetails

class userDetailsInline(admin.StackedInline):
    model = userDetails
    can_delete = False
    verbose_name_plural = 'Profile & Address Details'
    fk_name = 'user'

class CustomUserAdmin(BaseUserAdmin):
    inlines = (userDetailsInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_phone', 'is_staff')
    
    def get_phone(self, obj):
        if hasattr(obj, 'userdetails') and obj.userdetails.phone:
            return obj.userdetails.phone
        return "-"
    get_phone.short_description = "Phone"

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(userDetails)
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('user_avatar', 'user', 'phone', 'city', 'state', 'zipcode')
    search_fields = ('user__username', 'user__email', 'phone', 'city', 'state')
    list_filter = ('state', 'city')

    def user_avatar(self, obj):
        if obj.profile_pic:
            return format_html(
                '<img src="{}" style="width: 36px; height: 36px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_pic.url
            )
        return format_html('<span style="color: #94a3b8; font-size: 11px;">No photo</span>')
    user_avatar.short_description = "Avatar"

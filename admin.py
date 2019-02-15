from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _

from account.forms import ManagerUserCreationForm
from .models import User, RegisterLink


# Register your models here.


class UserAdmin(BaseUserAdmin):
    change_list_template = 'admin/account_change_list.html'
    add_form = ManagerUserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'email', 'phone_number', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_display_links = ('name',)
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'phone_number', 'date_of_birth')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'date_of_birth'),
        }),
    )
    search_fields = ('email', 'name', 'phone_number')
    ordering = ('-date_joined',)
    
    def get_urls(self):
        urls = super(UserAdmin, self).get_urls()
        post_urls = [
            path('user/send_invitation/', self.admin_site.admin_view(self.admin_send_invitation), name='user-send-invitation'),
        ]
        return post_urls + urls

    def admin_send_invitation(self, request):
        if request.method == 'GET':
            return TemplateResponse(request, 'admin/account_send_invitation_confirm.html', None)
        elif request.method == 'POST':
            users = User.objects.filter(is_staff=False)
            for user in users:
                link = RegisterLink.objects.create(user=user)
                user.email_user("서강대학교 멋쟁이 사자처럼 사이트에 가입해주세요.", "안녕하세요, %s님!\n멋쟁이 사자처럼에 오신걸 진심으로 환영합니다!\n\n1시간 안에 아래 링크를 통해 서강대학교 멋쟁이 사자처럼 사이트에 가입해주세요:\n%s\n\n감사합니다." % (user.name, request.get_host() + reverse('register', kwargs={'uuid': link.uuid.hex})), settings.DEFAULT_FROM_EMAIL)
            return redirect('admin:account_user_changelist')


class RegisterLinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'register_until', 'register_available')
    list_display_links = ('user',)


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(RegisterLink, RegisterLinkAdmin)

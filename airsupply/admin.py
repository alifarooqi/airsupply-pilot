from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import re_path
from .models import Item, Category, Order, Cart, LineItem, Place, InterPlaceDistance, DroneLoad, ClinicManager
from airsupply.tokens import send_activation_link
from django.shortcuts import redirect
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CMInline(admin.StackedInline):
	model = ClinicManager
	can_delete = False
	verbose_name_plural = 'clinic managers'


class CustomUserAdmin(UserAdmin):
    inlines = (CMInline,)

    def __init__(self, *args, **kwargs):
        super(UserAdmin,self).__init__(*args,**kwargs)
        UserAdmin.list_display = list(UserAdmin.list_display) + ['send_invitation_link']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(r'link/(?P<private_key>[0-9]+)', self.sendLink, name='link'),
        ]
        return custom_urls + urls

    def send_invitation_link(self,obj):
        return format_html(
            '<a class="button" href="{}">Send</a>', "link/"+str(obj.pk))

    def sendLink(self,request,private_key):
        send_activation_link(request, private_key)
        return redirect('http://127.0.0.1:8000/admin/auth/user/')


admin.site.register(Place)
admin.site.register(InterPlaceDistance)
admin.site.register(Item)
admin.site.register(LineItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(DroneLoad)
admin.site.register(ClinicManager)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

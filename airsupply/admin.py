from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Item, Category, Order, Cart, LineItem, Place, InterPlaceDistance, DroneLoad, ClinicManager


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

    def send_invitation_link(self, obj):
        return format_html('<a class="button" href="{}">Send</a>',"/admin?id="+str(obj.pk))


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
admin.site.register(User, UserAdmin)

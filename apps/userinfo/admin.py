from django.contrib import admin

from userinfo.models import UserInfo

class UserInfoAdmin(admin.ModelAdmin):
    # Field information to be display
    list_display = ('id','nickname', 'username', 'password','coin','diamond','is_superuser')
    fields = ['username', 'password']
    list_editable = ['nickname','coin','is_superuser','diamond']
    search_fields =('nickname','username','coin','diamond')
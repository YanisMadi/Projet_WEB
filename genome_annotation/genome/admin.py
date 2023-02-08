from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'prenom', 'nom', 'numero_tel', 'role', 'last_login', 'is_validated')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.is_validated = False
            obj.set_password(obj.password)
        obj.save()

admin.site.register(User, UserAdmin)

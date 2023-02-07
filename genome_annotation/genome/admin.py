from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'prenom', 'nom', 'numero_tel', 'role', 'last_login', 'is_validated')
    ordering = ('username',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.is_validated = False
        obj.save()

admin.site.register(User, UserAdmin)

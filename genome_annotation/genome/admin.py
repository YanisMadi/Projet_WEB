from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'prenom', 'nom', 'numero_tel', 'role', 'last_login', 'is_validated')
    ordering = ('username',)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.is_validated = False
        obj.set_password(form.cleaned_data["password"])
        obj.save()
        return super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)

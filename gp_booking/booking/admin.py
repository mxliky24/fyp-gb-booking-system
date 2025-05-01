from multiprocessing.resource_tracker import register

from django.contrib import admin
from .models import Patient, Doctor, Appointment, Slot, Review, Role, CustomUser

# Custom admin for handling user creation with hashed password
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

    # Automatically hashes password on user creation via admin panel
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password') and not change:
            print("Setting password hash")
            obj.set_password(form.cleaned_data['password'])
        super(CustomUserAdmin, self).save_model(request, obj, form, change)

# Registers all models to appear in Django admin dashboard
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Review)
admin.site.register(Patient)
admin.site.register(Role)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Slot)




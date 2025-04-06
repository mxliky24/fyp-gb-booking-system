from multiprocessing.resource_tracker import register

from django.contrib import admin
from .models import Patient, Doctor, Appointment, Slot, Review, Role, CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('password') and not change:
            print("Setting password hash")
            obj.set_password(form.cleaned_data['password'])
        super(CustomUserAdmin, self).save_model(request, obj, form, change)

# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Review)
admin.site.register(Patient)
admin.site.register(Role)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Slot)




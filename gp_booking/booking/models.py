from booking.user_manager import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime


# Defines system roles (e.g. PATIENT, DOCTOR)
class Role(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"role {self.name}"
# Custom user model replacing default auth with email login
class CustomUser(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True) # Email used as unique login identifier
    password = models.CharField(max_length=150)

    objects = CustomUserManager() # Custom manager handles user creation logic

    USERNAME_FIELD = 'email' # Overrides username to use email
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    backend = 'booking.backend.EmailBackend'   # Specifies custom backend for auth
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)  # Assigns role to user (e.g. Doctor or Patient)

# Stores additional patient-specific info (linked 1:1 with CustomUser)
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone  = models.CharField(max_length=20, blank=True, null=True)
    backend = 'booking.backend.EmailBackend'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

# Stores doctor-specific info including specialism and profile picture
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='doctor_pictures', blank=True, null=True)
    backend = 'booking.backend.EmailBackend'

    def __str__(self):
        return f"Dr.{self.user.get_full_name() or self.user.username}"

# Represents bookable time slots for a doctor
class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)    # Tracks if slot is already taken

    def __str__(self):
        return f"{self.doctor} {self.date} {self.time} ({'Booked' if self.is_booked else 'Available'})"

    # Returns a human-readable date/time format
    def to_date(self):
        month = self.date.strftime('%B')
        week_day = self.date.strftime('%A')
        day = self.date.strftime('%d')
        time = self.time.strftime('%H')
        min = self.time.strftime('%M')
        return f"{month} {week_day} {day} {time}:{min}"

# Represents a patient's booked appointment with a slot and status
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices= [
            ("Pending", "Pending"),
            ("Confirmed", "Confirmed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Pending",    # Default appointment status
    )

    # Automatically updates booking state of slots when saving
    def save(self, *args, **kwargs):
        if self.pk:
            old = Appointment.objects.get(pk=self.pk)
            # Frees up the previous slot if it’s been changed
            if old.slot != self.slot:
                old.slot.is_booked = False
                old.slot.save()
        self.slot.is_booked = True  # Marks current slot as booked
        self.slot.save()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.patient} {self.slot.doctor} ({self.slot.date} at {self.slot.time})"


# Stores patient reviews for doctors including rating and comment(Didn't have enough time to finish)
class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=255)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.doctor} {self.patient} {self.review_text}"


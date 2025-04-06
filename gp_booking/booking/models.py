from booking.user_manager import CustomUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator


class Role(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"role {self.name}"

class CustomUser(AbstractUser, PermissionsMixin):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']
    backend = 'booking.backend.EmailBackend'
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)


class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone  = models.CharField(max_length=20, blank=True, null=True)
    backend = 'booking.backend.EmailBackend'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='static/doctor_pictures', blank=True, null=True)
    backend = 'booking.backend.EmailBackend'

    def __str__(self):
        return f"Dr.{self.user.get_full_name() or self.user.username}"


class Slot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} {self.date} {self.time} ({'Booked' if self.is_booked else 'Available'})"

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
        default="Pending",
    )

    def __str__(self):
        return f"{self.patient} {self.slot.doctor} ({self.slot.date} at {self.slot.time})"

class Review(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    review_text = models.TextField(max_length=255)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])

    def __str__(self):
        return f"{self.doctor} {self.patient} {self.review_text}"


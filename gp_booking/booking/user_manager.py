from django.contrib.auth.base_user import BaseUserManager

# Custom manager to support email-based user creation
class CustomUserManager(BaseUserManager):
    # Creates a regular user with email and password
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address')) # Ensures email is required
        email = self.normalize_email(email) # Normalises email casing
        user = self.model(email=email, **extra_fields)
        user.set_password(password)   # Hashes password before saving
        user.save()
        return user

    # Creates a superuser with all required permissions
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True) # Required for admin access
        extra_fields.setdefault('is_superuser', True)  # Required for full permissions
        extra_fields.setdefault('is_active', True)  # Ensures account is active

        # Validates critical superuser fields
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)  # Delegates to create_user

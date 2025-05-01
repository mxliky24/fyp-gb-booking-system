from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()  # Retrieves the active custom user model (CustomUser)
class EmailBackend(BaseBackend): # Enables login using email instead of username
    def authenticate(self,request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # Tries to find user by email
        except User.DoesNotExist:
            return None   # Returns None if email not found

        if check_password(password, user.password):   # Verifies password against hashed value
            return user  # Authenticated successfully

        return None # Password check failed


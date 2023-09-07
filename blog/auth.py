from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()

class CustomModelBackend(ModelBackend):
    """
    Allows user to login with either email or password.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on their username or email and password.

        Args:
            request (HttpRequest): The request object, if available.
            username (str): The username or email provided for authentication.
            password (str): The password provided for authentication.
            **kwargs: Additional keyword arguments.

        Returns:
            User: The authenticated user if successful, or None if authentication fails.
        """
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Retrieve a user by their user ID.

        This method retrieves a user from the database based on their unique
        user ID (primary key). If a user with the specified user ID exists,
        it is returned; otherwise, it returns None.

        Args:
            user_id (int): The unique user ID (primary key) of the user to retrieve.

        Returns:
            User: The user object if found, or None if no user with the given ID exists.

        Raises:
            None
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

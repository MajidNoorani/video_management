from core.exceptions import CustomAPIException
from rest_framework import status


class CustomAccessException(CustomAPIException):
    """Custom exception for invalid regex patterns."""

    @property
    def status_code(self):
        return status.HTTP_403_FORBIDDEN

    @property
    def default_message(self):
        return "User is not Allowed."

    def __init__(self, message=None):
        self.message = message or self.default_message
        super().__init__(self.message)

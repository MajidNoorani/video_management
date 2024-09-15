from rest_framework.views import exception_handler
from rest_framework.response import Response
from abc import ABC, abstractmethod


class CustomAPIException(ABC, Exception):
    """Abstract base class for custom exceptions."""

    def __init__(self, message=None):
        # Use the default message if none is provided
        if message is None:
            message = self.default_message
        self.message = message
        super().__init__(self.message)

    @property
    @abstractmethod
    def status_code(self):
        """Must be implemented in the subclass to return the HTTP status code."""  # noqa
        pass

    @property
    @abstractmethod
    def default_message(self):
        """Must be implemented in the subclass to return the default message."""  # noqa
        pass


def custom_exception_handler(exc, context):
    # Handle only custom exceptions
    if isinstance(exc, CustomAPIException):
        return Response(
            {"error": exc.message},
            status=exc.status_code
        )

    # If the exception is not a custom one, let DRF handle it as usual
    return exception_handler(exc, context)

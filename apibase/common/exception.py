class AppError(Exception):
    """Base API Exception."""
    code = 500
    message = "An unknown error occurred."

    def __init__(self, message=None):
        if message:
            self.message = message
        super().__init__(self.message)

class ItemNotFound(AppError):
    code = 404
    message = "Item not found."

class InvalidInput(AppError):
    code = 400
    message = "Invalid input received."

class NotAuthorized(AppError):
    code = 401
    message = "Not authorized."

class Forbidden(AppError):
    code = 403
    message = "Access forbidden."

class Conflict(AppError):
    code = 409
    message = "Conflict detected."

class ServiceUnavailable(AppError):
    code = 503
    message = "Service temporarily unavailable."

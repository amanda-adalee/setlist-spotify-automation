class ResponseException(Exception):

    def __init__(self, status_code, message="This is a test"):
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f"Response gave Message: {self.message} and status code: {self.status_code}."
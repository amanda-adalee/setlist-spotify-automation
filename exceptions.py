class ResponseException(Exception):

    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return f"Response gave status code: {self.status_code}."
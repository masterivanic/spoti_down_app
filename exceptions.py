
import enum


class SpotifyCustomerException(Exception):

    def __init__(self, code, msg, reason=None):
        self.code = self.ErrorType()
        self.msg = msg
        self.reason = reason

    def __str__(self):
        return 'status code: {0}, msg:{1} , reason: {2}'.format(self.code, self.msg, self.reason)

    class ErrorType(enum.Enum):
        NO_CONTENT = 204
        INTERNAL_SERVER_ERROR = 500
        SUCCESS = 200

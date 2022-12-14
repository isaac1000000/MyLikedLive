# A set of custom exceptions to help with error handling

class FailedToAuthorizeException(Exception):
    def __init__(self, endpoint="Generic"):
        self.endpoint = endpoint
        self.message = "Failed to authorize"
        super().__init__(self.message)

    def __str__(self):
        return "{message} at endpoint: {endpoint}".format(message=self.message,
            endpoint=self.endpoint)

class RequestFaultException(Exception):
    def __init__(self, request_address, response_code="generic"):
        self.request_address = request_address
        self.response_code = response_code
        self.message = "Invalid return"
        super().__init__(self.message)

    def __str__(self):
        return "{message} from address: {return_address}\
            with response code: {response_code}".format(message=self.message,
            return_address=self.request_address, response_code=self.response_code)

class ConfigFaultException(Exception):
    def __init__(self, error_at="file_presence", type="generic"):
        self.error_at = error_at
        self.type = type
        self.message = "Error in resources/config.json"
        super().__init__(self.message)
    def __str__(self):
        return "{message} at {error_at} of type {type}".format(message=self.message,
            error_at=self.error_at, type=self.type)

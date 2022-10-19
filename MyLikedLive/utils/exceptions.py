class FailedToAuthorizeException(Exception):
    def __init__(self, endpoint="Generic"):
        self.endpoint = endpoint
        self.message = "Failed to authorize"
        super().__init__(self.message)

    def __str__(self):
        return "{message} at endpoint: {endpoint}".format(message=self.message,
            endpoint=self.endpoint)

class RequestFaultException(Exception):
    def __init__(self, request_address, response_code="Generic"):
        self.request_address = request_address
        self.response_code = response_code
        self.endpoint = endpoint
        self.message = "Invalid return"
        super().__init__(self.message)

    def __str__(self):
        return "{message} from address: {return_address}\
            with response code: {response_code}".format(message=self.message,
            return_address=self.return_address, response_code=self.response_code)

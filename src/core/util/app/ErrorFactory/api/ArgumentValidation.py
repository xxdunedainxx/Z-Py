from .CoreInternalError import InternalAPIError

class InvalidArgumentProvideed(InternalAPIError):
    def __init__(self,arg, expectedDataType):
        super().__init__(
            message=f"{arg} data type not allowed for this API. Expected {expectedDataType}",
            returnCode=400)

class ArgumentRequired(InternalAPIError):
    def __init__(self,arg):
        super().__init__(
            message=f"{arg} is required!",
            returnCode=400)
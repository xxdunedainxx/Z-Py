from .CoreInternalError import InternalAPIError

class InvalidAPIMethod(InternalAPIError):
    def __init__(self,method):
        super().__init__(
            message=f"{method} not allowed for this API",
            returnCode=405)

class InvalidMethodForRoute(InternalAPIError):
    def __init__(self,method,route):
        super().__init__(
            message=f"{method} not allowed for this specific route {route}",
            returnCode=405)
from flask import Response

class InternalAPIError(Exception):

    def __init__(self, message, returnCode, custom_header = None):
        self.msg=message
        self.rCode=returnCode
        self.custom_header=custom_header

        self.raise_error()

    def raise_error(self):
        return {"message" : self.msg, "ok" : False},self.rCode, self.custom_header

DEFAULT_INTERNAL_SERVER_ERROR={"message" : "Internal Server issues..", "ok" : False},501

def PayloadMustExist(fields: str):
    api_error=InternalAPIError(
        message=f"Payload and field \"id\" cannot be null. Or further fields must be provided: {fields} !",
        returnCode=400
    )

    return api_error.raise_error()

def AuthenticationRequired():
    api_error=InternalAPIError(
        message=f"User must authenticate!",
        returnCode=401,
        custom_header={"WWW-Authenticate" : "Digest realm=\"access to core app\""}
    )

    return api_error.raise_error()
class PreFlightHttpFailed(Exception):
    def __init__(self, error: str = ""):
        Exception.__init__(self,f"Http Preflight request failed!Error : {error}")
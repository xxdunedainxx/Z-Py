import sys, traceback


def errorStackTrace( e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    trace = traceback.format_exc()
    errorMessage = ("STACK TRACE ERROR :: " + str(e) + ".. Line number: " + str(
        exc_tb.tb_lineno) + "-- STACK TRACEBACK: " + str(trace))
    return errorMessage

class InvalidChannelSyncConfiguration(Exception):
    def __init__(self,channel, reason="UNKNOWN"):
        Exception.__init__(self,f"Failed to add {channel} to sync config. Reason: \'{reason}\'")

class MethodRequiresOverride(Exception):
    def __init__(self,method):
        Exception.__init__(self,f"Method \'{method}\' must be overriden!")
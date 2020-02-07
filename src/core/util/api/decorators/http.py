# General library imports
from functools import wraps
import os

# Flask imports
from flask import request

# log in user import
from ...web.http import get_loged_in_user

# Logging
from ...Logging.LogFactory import LogFactory


HTTP_LOGGER_DIRECTORY=".\\log\\http_info.log"

def override_http_log_dir(ndir: str):
    HTTP_LOGGER_DIRECTORY=ndir


def http_logger(api,http_log_override=None):
    @wraps(api)
    def logger_wrapper(*args, **kwargs):
            Logger = LogFactory(HTTP_LOGGER_DIRECTORY)
            Logger.write_log(data=f"Method - {request.method} // Endpoint - {request.base_url} // User {get_loged_in_user()}")
            Logger.commit_data()
            Logger.dispose_stream()
            return api(*args,**kwargs)
    return logger_wrapper
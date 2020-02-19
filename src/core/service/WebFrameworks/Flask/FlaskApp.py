from ..IWebFramework import IWebFramework
from .conf.FlaskAppConfig import FlaskAppConfig

class FlaskApp(IWebFramework):

    def __init__(self, config: FlaskAppConfig):
        super().__init__(config=config)
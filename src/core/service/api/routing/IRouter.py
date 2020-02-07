from ...ServiceCore import Service
from ....conf.API.routes.RouteConfig import RouteConfig
from flask_restplus import Namespace,Resource

class IRouter(Service):

    def __init__(self,routerConfig: RouteConfig):
        super().__init__(serviceConfig=routerConfig)

    def get_route(self,method: str)->str:
        pass

    def _validate_route(self,method: str, api):
        pass
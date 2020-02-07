from .IRouter import IRouter
from ....conf.API.routes.RouteConfig import RouteConfig
from ....util.app.ErrorFactory.api.RoutingErrors import InvalidAPIMethod,InvalidMethodForRoute,InternalAPIError

# For Route check decorator
from functools import wraps
from flask_restplus import Namespace,Resource

class Router(IRouter):

    def __init__(self,routerConfig: RouteConfig):
        self.core_route=""
        self.api_specific_resource=""
        self.supported_methods=[]
        self.api_specific_routes={}
        super().__init__(routerConfig=routerConfig)

        self.core_route=routerConfig.core_route
        self.api_specific_resource=routerConfig.api_specific_resource
        self.supported_methods=routerConfig.supported_methods
        self.api_specific_routes=routerConfig.api_specific_routes

    #def get_route(self,method: str)->str:
    #    return self._validate_route(
    #        method=method)

    # Custom Route Check Decorator
    def route_check(self,method:str):
        def route_check_decorate(api):
            @wraps(api)
            def validate(*args,**kwargs):
                validate_path = self._validate_route(
                    method=method,
                    api=api)
                if validate_path[0]["ok"] is True:
                    return api(*args,**kwargs)
                else:
                    return validate_path
            return validate
        return route_check_decorate

    def _validate_route(self,
                        method: str,
                        api: Resource):
        if method in self.supported_methods:
            return {"ok" : True},200
        elif method not in self.supported_methods:
            invalidMethod=InvalidAPIMethod(method=method)
            return invalidMethod.raise_error()
        #elif self.api_specific_routes[method] != route:
        #    invalidRouteMethod=InvalidMethodForRoute(
        #        method=method,
        #        route=route)
        #    return invalidRouteMethod.raise_error()
        else:
            genericError=InternalAPIError(
                message="Something went wrong validating the route.",
                returnCode=500)
            return genericError.raise_error()


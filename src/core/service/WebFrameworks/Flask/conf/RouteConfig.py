from ...ServiceConfig import ServiceConfig
from ...Configuration import InMemConfig, DefaultServiceConfigurations

class RouteConfig(ServiceConfig):

    def __init__(self,
                 file,
                 requiredAttributes: []=None,
                 defaultAttributes: {}=None):

        self.core_route=None
        self.api_specific_resource=None
        self.supported_methods=None
        self.method_docs = None
        self.api_specific_routes = None

        self.route_required_attributes=[
            "core_route",
            "api_specific_resource"
        ]

        if requiredAttributes is not None:
            self.route_required_attributes.extend(requiredAttributes)

        super().__init__(file,self.route_required_attributes,defaultAttributes)
        self._check_defaults()

    def _check_defaults(self):
        if getattr(self, "supported_methods") is None:
            self.supported_methods=[
                "get",
                "post",
                "delete",
                "patch"
            ]

        if getattr(self, "api_specific_routes") is None:
            self.api_specific_routes={
                "get" : "get",
                "post" : "create",
                "delete" : "remove",
                "patch" : "update"
            }

class RouterInMemoryConfig(InMemConfig):
    def __init__(self, core_route: str, api_specific_resource: str,
                 api_specific_routes: {},
                 supported_methods: [str],
                 log_file: str = DefaultServiceConfigurations.log_file,
                 log_level: str = DefaultServiceConfigurations.log_level,
                 logging_enabled: bool = DefaultServiceConfigurations.logging_enabled,
                 svc_name: str = DefaultServiceConfigurations.svc_name,
                 svc_description: str = DefaultServiceConfigurations.svc_description,
                 svc_namespace: str = DefaultServiceConfigurations.svc_namespace,
                 authors: [str] = DefaultServiceConfigurations.authors,
                 last_update: str = DefaultServiceConfigurations.last_update
                 ):
        super().__init__()
        self.core_route=core_route
        self.api_specific_resource=api_specific_resource
        self.api_specific_routes=api_specific_routes
        self.supported_methods=supported_methods
        self.log_file=log_file
        self.log_level=log_level
        self.logging_enabled=logging_enabled
        self.svc_name = svc_name
        self.svc_description= svc_description
        self.svc_namespace=svc_namespace
        self.authors= authors
        self.last_update = last_update

    def attr(self):
        return [
            "core_route",
            "api_specific_resource",
            "api_specific_routes",
            "supported_methods",
            "log_file",
            "log_level",
            "logging_enabled",
            "svc_name",
            "svc_description",
            "svc_namespace",
            "authors",
            "last_update"
        ]


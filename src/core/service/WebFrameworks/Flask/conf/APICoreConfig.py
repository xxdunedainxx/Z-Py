from .....conf.ServiceConfig import ServiceConfig
from .RouteConfig import RouteConfig
from .....conf.Configuration import InMemConfig, DefaultServiceConfigurations
class APICoreConfig(ServiceConfig):

    def __init__(self,
                 file,
                 routerConfig: RouteConfig,
                 requiredAttributes: []=None,
                 defaultAttributes: {}=None,
                 ):

        # Dependency Injection from RouterConfiguration
        self._router_config=routerConfig



        # Namespace descriptors
        self.resource_name=None
        self.api_namespace_name=None
        self.api_namespace_description=None
        self._supported_api_responses = None
        self.method_docs = None
        self.expected_models=None



        # Required
        required_api_attributes=[
            "api_namespace_name","api_namespace_description"
        ]

        if requiredAttributes is not None:
            required_api_attributes.extend(requiredAttributes)

        super().__init__(file,required_api_attributes,defaultAttributes)
        self._check_defaults()

    def router_config(self)->RouteConfig:
        return self._router_config

    def set_router_config(self, r: RouteConfig):
        self._router_config=r

    def _check_defaults(self):
        if getattr(self, "_supported_api_responses") is None:
            self._supported_api_responses=[
                200,
                401,
                500]

        if getattr(self, "method_docs") is None:
            self.method_docs={
                "get" : {
                    200: 'Success',401 : 'Unauthorized', 500 : 'Internal Server Error'
                },
                "post": {
                    200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'
                },
                "patch": {
                    200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'
                },
                "delete": {
                    200: 'Success', 401: 'Unauthorized', 500: 'Internal Server Error'
                }

            }

class APIInMemoryConfig(InMemConfig):

    def __init__(self,
                 resource_name: str,
                 api_namespace_name: str,
                 api_namespace_description: str,
                 method_docs: dict,
                 supported_api_responses: [int]=None,
                 log_file: str = DefaultServiceConfigurations.log_file,
                 log_level: str = DefaultServiceConfigurations.log_level,
                 logging_enabled: bool = DefaultServiceConfigurations.logging_enabled,
                 svc_name: str = DefaultServiceConfigurations.svc_name,
                 svc_description: str = DefaultServiceConfigurations.svc_description,
                 svc_namespace: str = DefaultServiceConfigurations.svc_namespace,
                 authors: [str] = DefaultServiceConfigurations.authors,
                 last_update: str = DefaultServiceConfigurations.last_update):
        super().__init__()
        self.resource_name=resource_name
        self.api_namespace_name=api_namespace_name
        self.api_namespace_description=api_namespace_description
        self._supported_api_responses=supported_api_responses
        self.log_file=log_file
        self.log_level=log_level
        self.logging_enabled=logging_enabled
        self.svc_name = svc_name
        self.svc_description= svc_description
        self.svc_namespace=svc_namespace
        self.authors= authors
        self.last_update = last_update
        self._supported_api_responses=supported_api_responses
        self.method_docs=method_docs

    def attr(self):
        return [
            "resource_name",
            "api_namespace_name",
            "api_namespace_description",
            "_supported_api_responses",
            "log_file",
            "log_level",
            "logging_enabled",
            "svc_name",
            "svc_description",
            "svc_namespace",
            "authors",
            "last_update",
            "_supported_api_responses",
            "method_docs"
        ]
from ..ServiceCore import Service
from .IAPICore import IAPI
from .routing.Router import Router
from ...conf.API.apis.APICoreConfig import APICoreConfig
from ...util.api.validators.InternalAPIValidators import InternalAPIValidator
from ...util.app.ErrorFactory.api.ArgumentValidation import ArgumentRequired,InvalidArgumentProvideed
from .IAPICore import IAPIArg
from ...util.Logging.LogFactory import LogFactory
from ...util.api.decorators.http import http_logger
# Flask framework imports
from flask_restplus import Namespace, Resource, model, fields
from flask import request

class APIArg(IAPIArg):

    def __init__(self, arg, dataType):
        super().__init__(arg,dataType)
        self.arg=arg
        self.dataType=dataType

class API(IAPI):

    #region Constructor
    def __init__(self,apiConfig: APICoreConfig,services: [Service],inputValidation: InternalAPIValidator):
        self._supported_api_responses=[]
        self.namespace_object:Namespace=None
        self._service_config=apiConfig
        self._setup_service_logger()
        self._build_api_models()
        super().__init__(
            apiConfig=apiConfig,
            services=services,
            inputValidation=inputValidation)

        self.api_validation=inputValidation

    #endregion

    #region Private Methods
    def _setup_service_logger(self):
        self.log=LogFactory(file=self._service_config.log_file,
                             log_level=self._service_config.log_level)

    # Constructs a Flask Namespace object
    def _build_namespace(self)->None:
        self.namespace_object=Namespace(
            name=self.build_resource_route(),
            description=self.api_config().api_namespace_description)

    def _build_router(self)->None:
        self.route_manager=Router(routerConfig=self
                                  .api_config()
                                  .router_config())

    # TODO
    def _build_api_models(self):
        if self._service_config.expected_models is None:
            return
        else:
            return

    #endregion

    #region Pubic Methods
    def payload_to_tuple_helper(self, payload: {})->tuple:
        t = tuple()
        for key in payload.keys():
            p=payload[key]
            t2=(p,)
            t = t + t2
        return t


    def validate_required_args(self,req: [APIArg], passed_args: {}):
        for required_arg in req:
            if passed_args is None or required_arg.arg not in passed_args.keys():
                raise ArgumentRequired(
                    arg=required_arg.arg
                )
            elif type(passed_args[required_arg.arg]) != required_arg.dataType:
                raise InvalidArgumentProvideed(
                    arg=required_arg.arg,
                    expectedDataType=required_arg.dataType
                )

    def api_config(self)->APICoreConfig:
        return self._service_config

    def build_resource_route(self)->str:
        return(f"{self.route_manager.core_route}/"
               f"{self.route_manager.api_specific_resource}")
               #f"{self.route_manager.api_specific_routes}")

    #endregion

    #region API Resource Builder
    # Builds out the Flask API Resource
    def build_api_resource(self)->Namespace:
        APIReference = self
        @APIReference.namespace_object.route(APIReference.build_resource_route())
        class API_Resource(Resource):

            #@APIReference.namespace_object.route(f"{APIReference.build_resource_route()}/{APIReference.route_manager.api_specific_routes['get']}")
            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["get"])
            def get(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["post"])
            def post(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["patch"])
            def patch(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["delete"])
            def delete(self):
                pass

        return APIReference.namespace_object
    #endregion



from ..IServiceCore import IService
from ...conf.API.apis.APICoreConfig import APICoreConfig
from .routing.Router import Router
from ...util.api.validators.InternalAPIValidators import InternalAPIValidator

# Flask framework imports
from flask_restplus import Namespace, Resource, model, reqparse
from flask import request

expected_api_parser = reqparse.RequestParser()
expected_api_parser.add_argument('X-Authentication', location='headers')

class IAPIArg():
    def __init__(self,arg,passedArg):
        pass

class IAPI(IService):


    def __init__(self,apiConfig: APICoreConfig,services: [IService],inputValidation: InternalAPIValidator):
        self._supported_api_responses=[]
        self.namespace_object:Namespace=None
        self.route_manager:Router=None
        self.resource_name=None
        super().__init__(serviceConfig=apiConfig)

        self._build()

    def validate_required_args(self,req: [IAPIArg], passed_args: {}):
        pass

    #region Private Methods
    def _route(self):
        pass

    def _build(self)->None:


        # Constructs router controller
        self._build_router()

        # Construct Namespace object
        self._build_namespace()

        # API Resource
        self.namespace_object=self.build_api_resource()

    def _build_router(self)->None:
        pass

    # Constructs a Flask Namespace object
    def _build_namespace(self)->None:
        pass

    def _pre_process_validation(self,**kwargs):
        pass


    #endregion

    #region Pubic Methods
    def api_config(self)->APICoreConfig:
        pass

    def return_codes(self,msg: {}, code: int=200):
        pass


    def build_resource_route(self)->str:
        pass
    #endregion

    # Builds out the Flask API Resource
    def build_api_resource(self)->Namespace:
        APIReference=self

        class API_Resource(Resource):

            def get(self):
                pass

            def post(self):
                pass

            def patch(self):
                pass

            def delete(self):
                pass

        return APIReference.namespace_object






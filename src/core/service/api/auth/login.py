#region Custom Library Imports
from ....service.ServiceCore import Service
from ....service.api.APICore import API
from ....conf.API.apis.APICoreConfig import APICoreConfig
from ....service.api.routing.Router import Router
from ....service.helpers.security.Authenticator import Authenticator
from ....util.Logging.LogFactory import LogFactory
from ....util.ErrorFactory.GeneralErrors import errorStackTrace
from ....util.api.validators.InternalAPIValidators import InternalAPIValidator

#region Decorators
from ....util.api.decorators.http import http_logger
#endregion
#endregion
#region Flask framework imports
from flask_restplus import Namespace, Resource,fields
from flask import request, session
#endregion
#region Basic API
class LoginAPI(API):

    #region Constructor
    def __init__(self,apiConfig: APICoreConfig,services: [Service],inputValidation: InternalAPIValidator=InternalAPIValidator()):
        super().__init__(
            apiConfig=apiConfig,
            services=services,
            inputValidation=inputValidation)

        # [0] == Authenticator
        self.auth: Authenticator = services[0]
    #endregion

    #region Private Methods


    #endregion

    #region Pubic Methods

    #endregion

    #region API Resource Builder
    # Builds out the Flask API Resource
    def build_api_resource(self)->Namespace:
        APIReference = self
        @APIReference.namespace_object.route(APIReference.api_config().resource_name)
        class API_Resource(Resource):

            #@APIReference.namespace_object.route(f"{APIReference.build_resource_route()}/{APIReference.route_manager.api_specific_routes['get']}")
            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["get"])
            @APIReference.route_manager.route_check(method="get")
            @http_logger
            def get(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["post"])
            @APIReference.route_manager.route_check(method="post")
            @APIReference.namespace_object.expect(APIReference.namespace_object.model(
                'Login_POST', {
                    'email': fields.String(description="Username",
                                          example="john.smith",
                                          required=False),
                    'password': fields.Integer(description="password",
                                                  example="changeme",
                                                  required=False)
                }
            ))
            @http_logger
            def post(self):
                try:
                    payload = APIReference.namespace_object.payload
                    if payload.keys() != APIReference.namespace_object.models.get("Login_POST").keys():
                        APIReference.log.write_log(
                            data=f"Invalid payload, must contain these attributes {APIReference.namespace_object.models.get('Login_POST')}",
                            level=LogFactory.warning
                        )
                        return {
                                   "messsage": f"Invalid payload, must contain these attributes {APIReference.namespace_object.models.get('Login_POST')}"}, 400
                    else:
                        auth=APIReference.auth.login(email=payload["email"], password=payload["password"])
                        rtoken=auth.decode("UTF-8")
                        return {"token" : rtoken, "message" : "logged in!"}, 200
                except Exception as e:
                    APIReference.log.write_log(
                        data=f"Critical API Error {errorStackTrace(e)}",
                        level=LogFactory.error
                    )
                    return {"message": "Internal Server Error"}, 500

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["patch"])
            @APIReference.route_manager.route_check(method="patch")
            @http_logger
            def patch(self):
                pass

            @APIReference.namespace_object.doc(responses=APIReference.api_config().method_docs["delete"])
            @APIReference.route_manager.route_check(method="delete")
            @http_logger
            def delete(self):
                pass

        return APIReference.namespace_object
    #endregion

#endregion
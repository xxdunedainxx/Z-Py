#region custom library import
from ...IHttp import IHttp
from ......conf.ServiceConfig import ServiceConfig
from ......util.ErrorFactory.GeneralErrors import errorStackTrace
from ......util.Logging.LogFactory import LogFactory
from ......util.app.ErrorFactory.build.BuildErrors import MissingConfiguration
#endregion
#region Python imports
import requests
from requests import Response
#endregion
#region IHTTP
class RequestsConnector(IHttp):

    #region constructor
    def __init__(self,httpConfig: ServiceConfig,rootEndpoint: str = "", defaultHeader:{} = None, apiTimeout: int = 60, sslVerification: bool = False):
        super().__init__(
            httpConfig,
            requests,
            defaultHeader=defaultHeader if not hasattr(httpConfig, "defaultHeader") else httpConfig.defaultHeader
        )
        self.endpoint=rootEndpoint if not hasattr(httpConfig, "rootEndpoint") else httpConfig.rootEndpoint
        self._default_timeout=apiTimeout
        self._default_ssl_verify=sslVerification

        # Defaults override
        if hasattr(httpConfig,"endpoint") and rootEndpoint is "":
            MissingConfiguration(file="RequestsConnector",config="endpoint")
        if hasattr(httpConfig,"timeout"):
            self._default_timeout = httpConfig.timeout
        if hasattr(httpConfig,"verify"):
            self._default_ssl_verify = httpConfig.verify


    #endregion


    #endregion

    def override_endpoint(self, nendpoint: str):
        self.endpoint=nendpoint

    #region CRUD Methods

    def post(self, endpoint, data, apiTimeout: int = None, sslVerification: bool = None ):
        return self.__central_handler(
            method="POST",
            endpoint=f"{self.endpoint}{endpoint}",
            headers=self._default_header,
            data=data,
            verify=sslVerification if sslVerification is not None else self._default_ssl_verify,
            timeout=apiTimeout if apiTimeout is not None else self._default_timeout,
        )

    def get(self, endpoint, data = None, apiTimeout: int = None, sslVerification: bool = None ):
        return self.__central_handler(
            method="GET",
            endpoint=f"{self.endpoint}{endpoint}",
            headers=self._default_header,
            data=data,
            verify=sslVerification if sslVerification is not None else self._default_ssl_verify,
            timeout=apiTimeout if apiTimeout is not None else self._default_timeout,
        )

    def patch(self,endpoint, data,  apiTimeout: int = None, sslVerification: bool = None ):
        return self.__central_handler(
            method="PATCH",
            endpoint=f"{self.endpoint}{endpoint}",
            headers=self._default_header,
            data=data,
            verify=sslVerification if sslVerification is not None else self._default_ssl_verify,
            timeout=apiTimeout if apiTimeout is not None else self._default_timeout,
        )

    def delete(self,endpoint, data, apiTimeout: int = None, sslVerification: bool = None):
        return self.__central_handler(
            method="DELETE",
            endpoint=f"{self.endpoint}{endpoint}",
            headers=self._default_header,
            data=data,
            verify=sslVerification if sslVerification is not None else self._default_ssl_verify,
            timeout=apiTimeout if apiTimeout is not None else self._default_timeout,
        )

    def __central_handler(self,endpoint, headers, verify, timeout, data=None, method="GET"):
        try:
            self._log.write_log(data=f"HTTP Request | METHOD = {method} to endpoint {endpoint}")
            val= requests.request(method,endpoint,headers=headers, data=data, verify=verify, timeout=timeout)
            return val
        except Exception as e:
            self._log.write_log(
                data=f"RequestsConnector failed with error {errorStackTrace(e)}",
                level=LogFactory.error
            )
            r=Response()
            r.status_code=500
            return r
    #endregion

#endregion
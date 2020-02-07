#region Custom imports
from ..Connector import Connector
from ....conf.ServiceConfig import ServiceConfig
from ....util.Logging.LogFactory import LogFactory
from ....util.app.ErrorFactory.Http import PreFlightHttpFailed
from ....util.ErrorFactory.GeneralErrors import errorStackTrace
#endregion

#region IHTTP
class IHttp(Connector):

    #region constructor
    def __init__(self,httpConfig: ServiceConfig, httpClientLibrary: object, defaultHeader: {} = None):
        super().__init__(httpConfig)

        if defaultHeader is None:
            self._default_header={}
        else:
            self._default_header=defaultHeader
        self._client_library=httpClientLibrary


    #endregion

    #region Http Methods
    def post(self, *args, **kwargs):
        pass
    def get(self, *args, **kwargs):
        pass
    def patch(self, *args, **kwargs):
        pass
    def delete(self, *args, **kwargs):
        pass
    #endregion
    def override_endpoint(self, nendpoint):
        pass
#endregion
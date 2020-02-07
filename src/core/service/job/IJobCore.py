from ..ServiceCore import Service
from ...conf.ServiceConfig import ServiceConfig


class IJob(Service):

    def __init__(self,jobConfig: ServiceConfig,services: [Service]):
        super().__init__(serviceConfig=jobConfig)


    #region Private Methods
    def _check_services(self, svcs: [Service]):
        pass

    def _establish_job_services(self,svcs: [Service]):
        pass

    def _pre_process_check(self):
        pass

    def _main(self):
        pass

    # Clean up your room :D
    def _clean_up(self):
        pass

    #endregion
    #region Pubic Methods

    def execute(self):
        pass

    # TODO Enable multi threading module on this interface???  :D
    def multi_thread(self):
        pass

    #endregion





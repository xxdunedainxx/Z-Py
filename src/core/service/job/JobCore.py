from .IJobCore import IJob
from ..ServiceCore import Service
from ...conf.ServiceConfig import ServiceConfig
from ...util.ErrorFactory.core.JobErrors import  InvalidNumberOfServicesProvided,OverideServiceNumber

class Job(IJob):

    def __init__(self, jobConfig: ServiceConfig, services: [Service]):
        super().__init__(jobConfig=jobConfig, services=services)

        self._check_services(svcs=services)

        self._establish_job_services(
            svcs=services
        )

    # region Private Methods
    def _check_services(self, svcs: [Service]):
        if hasattr(self,"expected_services") is False:
            self.expected_services=0

        if self.expected_services == 0:
            raise OverideServiceNumber()
        elif len(svcs) != self.expected_services:
            raise InvalidNumberOfServicesProvided(
                expected=self.expected_services,
                provided=len(svcs))

    def _pre_process_check(self):
        pass

    def _establish_job_services(self, svcs: [Service]):
        pass

    def _main(self):
        pass

    # Clean up your room :D
    def _clean_up(self):
        pass

    # endregion

    # region Pubic Methods

    def execute(self):
        # Before executing main, ensure pre process stuff is set up
        self._pre_process_check()

        # Execute Main
        self._main()

        # Post code clean up
        self._clean_up()

    # TODO Enable multi threading module on this interface???  :D
    def multi_thread(self):
        pass

    # endregion





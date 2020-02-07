from .IHelperCore import IHelper
from ...conf.ServiceConfig import ServiceConfig
class Helper(IHelper):

    def __init__(self,helperConfig: ServiceConfig):
        super().__init__(helperConfig=helperConfig)
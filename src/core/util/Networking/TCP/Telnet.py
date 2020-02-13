#region Python imports
from telnetlib import Telnet
#endregion
#region TelnetClient
class TelnetClient:

    def __init__(self, host: str, port: int):
        self.__client: Telnet = Telnet(host, port)

    @staticmethod
    def ping(host: str, port: int) -> bool:
        success = True
        test: Telnet = None
        try:
            test = Telnet(host, port)
            test.close()
        except Exception as e:
            success = False
        return success
#endregion
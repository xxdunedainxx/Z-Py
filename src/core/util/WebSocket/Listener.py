#region General Imports
import json
import time
import websocket
import asyncio
import requests
import datetime
import traceback
import sys
#endregion

class WebSocketListener():
    #region Constructor
    def __init__(self,
                 socket_url: str,
                 web_socket_name: str):

        self._socket_url=socket_url
        self.name=web_socket_name
        self._socket: websocket=None
    #endregion
    #region _on_message_handler
    # Requires Override
    def _on_message_handler(self, msg: str):
        raise MethodRequiresOverride(method="_on_message_handler")
    #endregion
    #region stream_on_message
    def stream_on_message(self, message:str):
        try:
            self._on_message_handler(msg=message)
        except Exception as e:
            raise e
    #endregion
    #region stream_on_error
    def stream_on_error(self, ws: websocket, error: str):
        raise Exception(f"Socket stream had a critical error: {error}")
    #endregion
    #region stream_on_close
    def stream_on_close(self, ws: websocket)->str:
        return f"WEB SOCKET ({self.name}) STREAM CLOSED!!"
    #endregions
    #region init_socket
    def init_socket(self, url: str)->str:
        rtmResponse = requests.get(url)
        rtmJson = json.loads(rtmResponse.content.decode("utf-8").replace("'", '"'))
        returnUrl = rtmJson['url']
        return returnUrl
    #endregion
    #region run_listener
    def run_listener(self)->None:

        websocket.enableTrace(True)
        wsUrl = self.init_socket(self._socket_url)

        self._socket = websocket.WebSocketApp(wsUrl,
                                    on_message=self.stream_on_message,
                                    on_error=self.stream_on_error,
                                    on_close=self.stream_on_close)

        self._socket.run_forever()
    #endregion
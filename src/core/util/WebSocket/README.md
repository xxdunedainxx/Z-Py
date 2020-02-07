This class can be used to create a TCP stream with a TCP socket. 

NOTE: this requires the websocket_client package (pip install websocket_client)
URL : https://pypi.org/project/websocket_client/

Example usage: 

class CustomListener(WebSocketListener):
    def __init__(self,
                 socket_url: str,
                 web_socket_name: str):

        super().__init__(socket_url, web_socket_name)

    def _on_message_handler(self, msg: str):
    	print(f"got a message {msg}")
listen=CustomListener(socket_url="somedomain:somePort", web_socket_name="someFriendlyName")

# runs daemon
listen.run_listener()
from src.core.service.WebFrameworks.WebFrameworkConfig import WebFrameworkConfig
from src.core.conf.ServiceConfig import InMemConfig

class FlaskAppConfig(WebFrameworkConfig):
    DEBUG_DEFAULT=True
    CORS_DEFAULT=False
    CORS_RESOURCE_SETTING_DEFAULT=None
    CORS_CREDS_DEFAULT=False
    ANGULAR_DEFAULT=None
    ANGULAR_CLIENT_DEFAULT=None
    DEFAULT_SECRET_KEY_LEN=15


    def __init__(self, file):
        self.debug=None
        self.ENV=None
        self.title=None
        self.version=None
        self.description=None
        self.cors_enabled=None
        self.cors_resource_setting=None
        self.cors_with_creds=None
        self.angular_client=None
        self.angular_client_directory=None
        self.secret_key_len=FlaskAppConfig.DEFAULT_SECRET_KEY_LEN

        super().__init__(file=file)

class FlaskInMemoryConfig(InMemConfig):



    def __init__(self,title,
                 version,description,env,
                 debug=FlaskAppConfig.DEBUG_DEFAULT, cors=FlaskAppConfig.CORS_DEFAULT,cors_resource_setting=FlaskAppConfig.CORS_RESOURCE_SETTING_DEFAULT, cors_creds=FlaskAppConfig.CORS_CREDS_DEFAULT,
                 angular=FlaskAppConfig.ANGULAR_DEFAULT, angular_client=FlaskAppConfig.ANGULAR_CLIENT_DEFAULT, secret_key_len=FlaskAppConfig.DEFAULT_SECRET_KEY_LEN):
        super().__init__()
        self.debug=debug
        self.ENV=env
        self.title=title
        self.version=version
        self.description=description
        self.cors_enabled=cors
        self.cors_resource_setting=cors_resource_setting
        self.cors_with_creds=cors_creds
        self.angular_client=angular
        self.angular_client_directory=angular_client
        self.secret_key_len=secret_key_len
    def attr(self):
        return [
            "debug",
            "ENV",
            "title",
            "version",
            "description",
            "cors_enabled",
            "cors_resource_setting",
            "angular_client",
            "angular_client_directory",
            "secret_key_len"
        ]
from ..IWebFramework import IWebFramework
from .conf.FlaskAppConfig import FlaskAppConfig, FlaskInMemoryConfig
from ...ServiceCore import Service

class FlaskApp(IWebFramework):

    def __init__(self,
                 config: FlaskAppConfig,
                 # Service by default no services
                 serviceInjection: dict = None
    ):
        super().__init__(config=config)

        if serviceInjection is None:
            self.core_services = {}
        else:
            self.core_services = serviceInjection

    def _configure_api_services(self):
        if "BuildAPI" in self._config.service_configs:
            for api in self._config.service_configs["apis"]:
                self._add_api_resource(conf=api)
            try:
                self._services["BuildAPI"]: BuildAPI = BuildAPI(
                    apiConfig=FlaskAppConfig(
                        FlaskInMemoryConfig(
                            title=self._config.service_configs["BuildAPI"]["configs"]["title"],
                            version=self._config.service_configs["BuildAPI"]["configs"]["version"],
                            description=self._config.service_configs["BuildAPI"]["configs"]["description"],
                            env=self._config.service_configs["BuildAPI"]["configs"]["env"],
                            debug=self._config.service_configs["BuildAPI"]["configs"]["debug"] if "debug" in
                                                                                                  self._config.service_configs[
                                                                                                      "BuildAPI"][
                                                                                                      "configs"].keys()
                            else FlaskAppConfig.DEBUG_DEFAULT,
                            cors=self._config.service_configs["BuildAPI"]["configs"]["cors"] if "cors" in
                                                                                                self._config.service_configs[
                                                                                                    "BuildAPI"][
                                                                                                    "configs"].keys()
                            else FlaskAppConfig.CORS_DEFAULT,
                            cors_resource_setting=self._config.service_configs["BuildAPI"]["configs"][
                                "cors_resource_setting"] if "cors_resource_setting" in
                                                            self._config.service_configs["BuildAPI"]["configs"].keys()
                            else FlaskAppConfig.CORS_RESOURCE_SETTING_DEFAULT,
                            cors_creds=self._config.service_configs["BuildAPI"]["configs"][
                                "cors_creds"] if "cors_creds" in self._config.service_configs["BuildAPI"][
                                "configs"].keys()
                            else FlaskAppConfig.CORS_DEFAULT,
                            angular=self._config.service_configs["BuildAPI"]["configs"]["angular"] if "angular" in
                                                                                                      self._config.service_configs[
                                                                                                          "BuildAPI"][
                                                                                                          "configs"].keys()
                            else FlaskAppConfig.ANGULAR_DEFAULT,
                            angular_client=self._config.service_configs["BuildAPI"]["configs"][
                                "angular_client"] if "angular_client" in self._config.service_configs["BuildAPI"][
                                "configs"].keys()
                            else FlaskAppConfig.ANGULAR_CLIENT_DEFAULT,
                        ) if self._config.service_configs["BuildAPI"]["location"] is None else
                        self._config.service_configs["BuildAPI"]["location"]
                    ),
                    apis=self._apis
                )
                self.build()
            except KeyError as e:
                raise MissingConfiguration(
                    file="Build Service Config section",
                    config=str(e.args)
                )
            except Exception as e:
                raise e
        else:
            raise BuildFailure("\'BuildAPI\' not present in build config!")

    def _grab_api_services(self):
        pass

    def _configure_security_layer(self):
        pass
        """if "security" in self._config.service_configs.keys():
            self._logger.write_log(
                data="Security layer enabled. Setting up",
                level=LogFactory.trace
            )

            if "session_exp_days" in self._config.service_configs["security"].keys():
                JwtAuth.exp_day_policy = self._config.service_configs["security"]["session_exp_days"]
                SessionHandler.exp_day_policy = self._config.service_configs["security"]["session_exp_days"]

            if "session_exp_seconds" in self._config.service_configs["security"].keys():
                JwtAuth.exp_seconds_policy = self._config.service_configs["security"]["session_exp_seconds"]
                SessionHandler.exp_seconds_policy = self._config.service_configs["security"]["session_exp_seconds"]

            if "jwt_algorithm" in self._config.service_configs["security"].keys():
                JwtAuth.jwt_algo = self._config.service_configs["security"]["jwt_algorithm"]

            if "secret_keys_length" in self._config.service_configs["security"].keys():
                JwtAuth.jwt_secret_key = RandomStringGenerator.random_string(
                    self._config.service_configs["security"]["secret_keys_length"])"""

    def build(self):
        pass

    def run(self):
        pass
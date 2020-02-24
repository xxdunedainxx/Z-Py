#region Custom Imports
from .conf.CoreConfiguration import CoreConfiguration
from ..core.util.Logging.LogFactory import LogFactory
from ..core.util.app.ErrorFactory.build.BuildErrors import BuildFailure,MissingConfiguration
from ..core.service import IServiceCore
from ..core.service.api.IAPICore import IAPI
from ..core.service.job.IJobCore import IJob
from ..core.conf.API.apis.APICoreConfig import APICoreConfig, APIInMemoryConfig
from ..core.conf.Configuration import DefaultServiceConfigurations
from ..core.conf.ServiceConfig import ServiceConfig,ServiceConfigInMemory
from ..core.conf.Flask.FlaskConfiguration import FlaskConfiguration,FlaskInMemoryConfig
from ..core.conf.API.routes.RouteConfig import RouteConfig, RouterInMemoryConfig
from ..core.service.helpers.security.JwtAuth import JwtAuth
from ..core.service.helpers.security.SessionHandler import SessionHandler
from ..core.service.helpers.security.Authenticator import Authenticator
from ..core.service.helpers.security.RandomStringGenerator import RandomStringGenerator
#endregion
#region API Specific Imports
from ..core.service.api.root.BuildAPI import BuildAPI
#endregion
#region General Package Imports
import sys
import os
from importlib import util as importlib_util, import_module
#endregion

class BuildApplication():

    def __init__(self, conf_file: str= "./conf/build.json"):

        self._config: CoreConfiguration=CoreConfiguration(file=conf_file)
        self._services:{} = {}
        self._apis: [IAPI] = []
        self._logger = LogFactory(
            file=self._config.core_logging_file,
            log_level=self._config.core_logging_level
        )

    #region Core Methods
    def __validate_python_version(self):
        runtime_version=float(str(sys.version_info.major) + "." + str(sys.version_info.minor))
        required_version=float(self._config.python_version.split('.')[0] + "." + self._config.python_version.split(".")[1])

        if runtime_version < required_version:
            raise BuildFailure("Failed to build app. Minimum python version of" + str(required_version) +  " needed to run this project.")

    def __check_library_dependencies(self):
        for library in self._config.library_requirements:
            test_import=importlib_util.find_spec(library)

            if test_import is None:
                raise BuildFailure(f"Required package not found: \'{library}\'. Make sure you run setup.py")

    def __check_sub_modules(self):
        for submodule in self._config.submodules:
            if os.path.isdir(submodule) is False:
                raise BuildFailure(f"Expected submodule does not exist! \'{submodule}\'. Make sure you run  \'git submodule init\' and \'git submodule update\', or RUN setup.py")

    def __build_check(self):
        self.__validate_python_version()
        self.__check_library_dependencies()
        self.__check_sub_modules()

    def _init_services(self):
        self._configure_core_services()

        self._configure_api_services()
    #endregion

    def _grab_api_services(self,svcs: [str])->[IServiceCore]:
        rServices: [IServiceCore] = []
        for svc in svcs:
            if svc in self._services.keys():
                rServices.append(self._services[svc])
        return rServices

    def _add_api_resource(self, conf: {})->IAPI:
        if conf["enabled"] is True:
            self._logger.write_log(data=f"{conf['name']} is enabled", level=LogFactory.info)
            api_config: APICoreConfig = None
            router_config: RouteConfig = None
            try:
                for configuration in conf["configs"]:

                    if "_type" in configuration.keys():
                        if configuration["_type"] == "Router":
                            router_config=RouteConfig(
                                file=(
                                    RouterInMemoryConfig(
                                        core_route=configuration["configs"]["core_route"],
                                        api_specific_resource=configuration["configs"]["api_specific_resource"],
                                        api_specific_routes=configuration["configs"]["api_specific_routes"],
                                        supported_methods=configuration["configs"]["supported_methods"],
                                        log_file=configuration["default_config_override"]["log_file"]
                                            if configuration["default_config_override"] is not None and
                                                "log_file" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.log_file,
                                        log_level=configuration["default_config_override"]["log_level"]
                                            if configuration["default_config_override"] is not None and
                                                "log_level" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.log_level,
                                        logging_enabled=configuration["default_config_override"]["logging_enabled"]
                                            if configuration["default_config_override"] is not None and
                                                "logging_enabled" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.logging_enabled,
                                        svc_name=configuration["default_config_override"]["svc_name"]
                                            if configuration["default_config_override"] is not None and
                                                "svc_name" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.svc_name,
                                        svc_description=configuration["default_config_override"]["svc_description"]
                                            if configuration["default_config_override"] is not None and
                                                "svc_description" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.svc_description,
                                        svc_namespace=configuration["default_config_override"]["svc_namespace"]
                                            if configuration["default_config_override"] is not None and
                                                "svc_namespace" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.svc_namespace,
                                        authors=configuration["default_config_override"]["authors"]
                                            if configuration["default_config_override"] is not None and
                                                "authors" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.authors,
                                        last_update=configuration["default_config_override"]["last_update"]
                                            if configuration["default_config_override"] is not None and
                                                "last_update" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.last_update
                                    )
                                ) if configuration["location"] is None else configuration["location"]
                            )
                        elif configuration["_type"] == "api":
                            api_config=APICoreConfig(
                                file=(
                                    APIInMemoryConfig(
                                        api_namespace_name=configuration["configs"]["api_namespace_name"],
                                        api_namespace_description=configuration["configs"]["api_namespace_description"],
                                        resource_name=configuration["configs"]["resource_name"],
                                        method_docs=configuration["configs"]["method_docs"]
                                        if
                                        "method_docs" in configuration["configs"].keys()
                                        else
                                        self._config.service_configs["default_service_config"]["swagger"][
                                            "method_docs"],
                                        supported_api_responses=configuration["configs"]["_supported_api_responses"]
                                        if
                                        "method_docs" in configuration["configs"].keys()
                                        else
                                        self._config.service_configs["default_service_config"]["swagger"][
                                            "_supported_api_responses"],
                                        log_file=configuration["default_config_override"]["log_file"]
                                            if configuration["default_config_override"] is not None and
                                                "log_file" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.log_file,
                                        log_level=configuration["default_config_override"]["log_level"]
                                            if configuration["default_config_override"] is not None and
                                                "log_level" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.log_level,
                                        logging_enabled=configuration["default_config_override"]["logging_enabled"]
                                            if configuration["default_config_override"] is not None and
                                                "logging_enabled" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.logging_enabled,
                                        svc_name=configuration["default_config_override"]["svc_name"]
                                            if configuration["default_config_override"] is not None and
                                                "svc_name" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.svc_name,
                                        svc_description=configuration["default_config_override"]["svc_description"]
                                            if configuration["default_config_override"] is not None and
                                                "svc_description" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.svc_description,
                                        svc_namespace=configuration["default_config_override"]["svc_namespace"]
                                            if configuration["default_config_override"] is not None and
                                                "svc_namespace" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.svc_namespace,
                                        authors=configuration["default_config_override"]["authors"]
                                            if configuration["default_config_override"] is not None and
                                                "authors" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.authors,
                                        last_update=configuration["default_config_override"]["last_update"]
                                            if configuration["default_config_override"] is not None and
                                                "last_update" in configuration["default_config_override"].keys()
                                            else
                                                DefaultServiceConfigurations.last_update
                                    )
                                ) if configuration["location"] is None else configuration["location"],
                                routerConfig=None
                            )
                        else:
                            self._logger.write_log(data=f"{configuration['_type']} unrecognized type!",
                                                   level=LogFactory.warning)
                    else:
                        self._logger.write_log(data=f"\'_type\' not specified in configuration", level=LogFactory.warning)
            except KeyError as e:
                raise MissingConfiguration(
                    file="Build Service Config section",
                    config=str(e.args)
                )
            except Exception as e:
                raise e
            # Establish router config to api config connection
            router_config.initialize_config()
            api_config.set_router_config(r=router_config)
            api_config.initialize_config()

            # Grab class and construct
            api_class: IAPI = getattr(import_module(conf['module'], package=self._config.root_namespace),conf['name'])
            instance=api_class(
                               apiConfig=api_config,
                               services=self._grab_api_services(svcs=conf["services"]) if "services" in conf.keys() else [] ,
            )
            self._apis.append(instance)
        else:
            self._logger.write_log(data=f"{conf['name']} is disabled", level=LogFactory.warning)
            return None

    def __grab_svc_dependencies(self, svcs: str)->[IServiceCore]:
        rsvcs = []
        for s in svcs:
            if s in self._services.keys():
                rsvcs.append(self._services[s])
        return rsvcs

    def _add_core_resource(self, configuration: {})->IServiceCore:
        if configuration["enabled"] is True:
            try:
                svc_config = ServiceConfig(
                    file=(
                        ServiceConfigInMemory(
                            log_file=configuration["default_config_override"]["log_file"]
                            if configuration["default_config_override"] is not None and
                               "log_file" in configuration["default_config_override"].keys()
                            else
                            DefaultServiceConfigurations.log_file,
                            log_level=configuration["default_config_override"]["log_level"]
                            if configuration["default_config_override"] is not None and
                               "log_level" in configuration["default_config_override"].keys()
                            else
                            DefaultServiceConfigurations.log_level,
                            logging_enabled=configuration["default_config_override"]["logging_enabled"]
                            if configuration["default_config_override"] is not None and
                               "logging_enabled" in configuration["default_config_override"].keys()
                            else
                            DefaultServiceConfigurations.logging_enabled,
                            svc_name=configuration["default_config_override"]["svc_name"]
                            if configuration["default_config_override"] is not None and
                               "svc_name" in configuration["default_config_override"].keys()
                            else
                            DefaultServiceConfigurations.svc_name,
                            svc_description=configuration["default_config_override"]["svc_description"]
                            if configuration["default_config_override"] is not None and
                               "svc_description" in configuration["default_config_override"].keys()
                            else
                            DefaultServiceConfigurations.svc_description,
                            svc_namespace=configuration["default_config_override"]["svc_namespace"]
                            if configuration["default_config_override"] is not None and
                               "svc_namespace" in configuration["default_config_override"].keys()
                            else
                            DefaultServiceConfigurations.svc_namespace,
                            authors=configuration["default_config_override"]["authors"]
                            if configuration["default_config_override"] is not None and
                               "authors" in configuration["default_config_override"].keys()
                            else
                            DefaultServiceConfigurations.authors,
                            last_update=configuration["default_config_override"]["last_update"]
                            if configuration["default_config_override"] is not None and
                               "last_update" in configuration["default_config_override"].keys()
                            else
                            DefaultServiceConfigurations.last_update,
                            attribute_override=configuration["configs"] if "configs" in configuration.keys() else None
                        )
                    ) if configuration["location"] is None else configuration["location"]
                )
                svc_config.initialize_config()
                # Grab class and construct
                svc_class: IServiceCore = getattr(import_module(configuration['module'], package=self._config.root_namespace), configuration['name'])
                if len(configuration["services"]) == 0:
                    instance = svc_class(
                        svc_config
                    )
                else:
                    instance = svc_class(
                        svc_config,
                        services=self.__grab_svc_dependencies(svcs=configuration["services"])
                    )
                if "svc_key_override" in configuration.keys():
                    self._services[configuration["svc_key_override"]]=instance
                else:
                    self._services[configuration["name"]]=instance
            except KeyError as e:
                raise MissingConfiguration(
                    file="Build Service Config section",
                    config=str(e.args)
                )
            except Exception as e:
                raise e
        else:
            return None

    def _configure_api_services(self):
        if "BuildAPI" in self._config.service_configs:
            for api in self._config.service_configs["apis"]:
                self._add_api_resource(conf=api)
            try:
                self._services["BuildAPI"]: BuildAPI = BuildAPI(
                    apiConfig=FlaskConfiguration(
                        FlaskInMemoryConfig(
                           title=self._config.service_configs["BuildAPI"]["configs"]["title"],
                           version=self._config.service_configs["BuildAPI"]["configs"]["version"],
                           description=self._config.service_configs["BuildAPI"]["configs"]["description"],
                           env=self._config.service_configs["BuildAPI"]["configs"]["env"],
                           debug=self._config.service_configs["BuildAPI"]["configs"]["debug"] if "debug" in self._config.service_configs["BuildAPI"]["configs"].keys()
                            else FlaskConfiguration.DEBUG_DEFAULT,
                           cors=self._config.service_configs["BuildAPI"]["configs"]["cors"] if "cors" in self._config.service_configs["BuildAPI"]["configs"].keys()
                            else FlaskConfiguration.CORS_DEFAULT ,
                           cors_resource_setting=self._config.service_configs["BuildAPI"]["configs"]["cors_resource_setting"] if "cors_resource_setting" in self._config.service_configs["BuildAPI"]["configs"].keys()
                            else FlaskConfiguration.CORS_RESOURCE_SETTING_DEFAULT,
                           cors_creds=self._config.service_configs["BuildAPI"]["configs"]["cors_creds"] if "cors_creds" in self._config.service_configs["BuildAPI"]["configs"].keys()
                            else FlaskConfiguration.CORS_DEFAULT,
                           angular=self._config.service_configs["BuildAPI"]["configs"]["angular"] if "angular" in self._config.service_configs["BuildAPI"]["configs"].keys()
                            else FlaskConfiguration.ANGULAR_DEFAULT,
                           angular_client=self._config.service_configs["BuildAPI"]["configs"]["angular_client"] if "angular_client" in self._config.service_configs["BuildAPI"]["configs"].keys()
                            else FlaskConfiguration.ANGULAR_CLIENT_DEFAULT,
                        ) if self._config.service_configs["BuildAPI"]["location"] is None else self._config.service_configs["BuildAPI"]["location"]
                    ),
                    apis=self._apis
                )
                self._services["BuildAPI"].build()
            except KeyError as e:
                raise MissingConfiguration(
                    file="Build Service Config section",
                    config=str(e.args)
                )
            except Exception as e:
                raise e
        else:
            raise BuildFailure("\'BuildAPI\' not present in build config!")

    def _configure_security_layer(self):
        if "security" in self._config.service_configs.keys():
            self._logger.write_log(
                data="Security layer enabled. Setting up",
                level=LogFactory.trace
            )

            if "session_exp_days" in self._config.service_configs["security"].keys():
                JwtAuth.exp_day_policy=self._config.service_configs["security"]["session_exp_days"]
                SessionHandler.exp_day_policy=self._config.service_configs["security"]["session_exp_days"]

            if "session_exp_seconds" in self._config.service_configs["security"].keys():
                JwtAuth.exp_seconds_policy=self._config.service_configs["security"]["session_exp_seconds"]
                SessionHandler.exp_seconds_policy=self._config.service_configs["security"]["session_exp_seconds"]

            if "jwt_algorithm" in self._config.service_configs["security"].keys():
                JwtAuth.jwt_algo=self._config.service_configs["security"]["jwt_algorithm"]

            if "secret_keys_length" in self._config.service_configs["security"].keys():
                JwtAuth.jwt_secret_key=RandomStringGenerator.random_string(self._config.service_configs["security"]["secret_keys_length"])

    def _configure_core_services(self):
        for core_svc in self._config.service_configs["core"]:
            self._add_core_resource(configuration=core_svc)

    def build(self):
        # Pre-build check
        self.__build_check()

        # initialize services from config
        self._init_services()

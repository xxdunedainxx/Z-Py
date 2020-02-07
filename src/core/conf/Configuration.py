from ...core.util.Logging.LogFactory import LogFactory
import json


# BASE CLASS FOR CONFIGURATION OBJECTS


class DefaultServiceConfigurations:

    log_file="\\log\\dump.log"
    log_level="ALL"
    logging_enabled=True
    svc_name="Service Name placeholder"
    svc_description="Service Description placeholder"
    svc_namespace="dot.walk.to.service.place.holder"
    authors=["zach.mcfadden"]
    last_update="UNKNOWN!"
    version="0"


    def __init__(self):
        pass

class InMemConfig():

    def __init__(self, **kwargs):
        pass

    def attr(self)->[]:
        pass

class Configuration():

    def __init__(self,file,requiredAttributes,defaultAttributes):
        self._required_attributes=requiredAttributes
        self._defaults=defaultAttributes
        self.config_file=file

        self.default_output_header="-----------------"
        self.dev_mode_enabled=True

        self.log_file: str = ".\\log\\dump.log"
        self.log_level: str=  LogFactory.all
        self.logging_enabled: bool = True


    def initialize_config(self):
        if type(self.config_file) is str:
            self._read_config(self.config_file)
        elif issubclass(type(self.config_file), InMemConfig):
            self._extract_attributes()
        else:
            return

    def _extract_attributes(self):
        for attr in self.config_file.attr():
            self.__setattr__(attr, getattr(self.config_file,attr))

    def _read_config(self,file):
        self._initialize_object(json.load
                                (open(file)))
        self._check_defaults()

    def _initialize_object(self,json):

        for config_item in json.keys():
            if self._attribute_exists(json,config_item):
                 setattr(self,config_item,json[config_item])

            elif self._is_default(config_item):
                setattr(self,config_item,self._grab_default(config_item))

            elif self._is_attribute_required(config_item):
                raise Exception(f"Required config item for {type(self).__name__} {config_item}")

    def _check_defaults(self):
        for default in self._defaults.keys():
            if hasattr(self,default) and getattr(self,default) is not None:
                continue
            else:
                setattr(self,default,self._defaults[default])

    def _attribute_exists(self,obj,key):
        if key in obj.keys():
            return True
        else:
            return False

    def _is_attribute_required(self,key):
        if self._required_attributes is not None and key in self._required_attributes:
            return True

    def _is_default(self,key):
        if key in self._defaults.keys():
            return True
        else:
            return False

    def _grab_default(self,key):
        return self._defaults[key]


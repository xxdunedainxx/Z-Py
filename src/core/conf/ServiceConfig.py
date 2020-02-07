from ..conf.Configuration import Configuration, InMemConfig,DefaultServiceConfigurations
class ServiceConfig(Configuration):


    required_attributes = [""]
    default_attributes = {}

    def __init__(self,file,requiredAttributes: [] = None, defaultAttributes: {} = None):
        self.svc_name:  str= DefaultServiceConfigurations.svc_name
        self.svc_description: str=DefaultServiceConfigurations.svc_description
        self.svc_version: str=DefaultServiceConfigurations.version
        self.svc_namespace: str=DefaultServiceConfigurations.svc_namespace
        self.authors: [str]=DefaultServiceConfigurations.authors
        self.last_update: str=DefaultServiceConfigurations.last_update

        super().__init__(
                file,
                requiredAttributes=requiredAttributes if requiredAttributes is not None else ServiceConfig.required_attributes,
                defaultAttributes=defaultAttributes if defaultAttributes is not None else ServiceConfig.default_attributes
        )

class ServiceConfigInMemory(InMemConfig):

    def __init__(self,svc_name=DefaultServiceConfigurations.svc_name,
              svc_description=DefaultServiceConfigurations.svc_description,
              svc_version=DefaultServiceConfigurations.version,
              svc_namespace=DefaultServiceConfigurations.svc_namespace,
              authors=DefaultServiceConfigurations.authors,
              last_update=DefaultServiceConfigurations.last_update,
              log_file=DefaultServiceConfigurations.log_file,
              log_level=DefaultServiceConfigurations.log_level,
              logging_enabled=DefaultServiceConfigurations.logging_enabled,
              attribute_override=None):
        self.svc_name=svc_name
        self.svc_description=svc_description
        self.svc_version=svc_version
        self.svc_namespace=svc_namespace
        self.authors=authors
        self.last_update=last_update
        self.attribute_override=attribute_override
        self.log_file=log_file
        self.log_level=log_level
        self.logging_enabled=logging_enabled
        if self.attribute_override is not None and type(self.attribute_override) is dict:
            for attribute in attribute_override.keys():
                setattr(self,attribute,attribute_override[attribute])

        super().__init__()

    def attr(self):
        rarray = [
             "svc_name",
             "svc_description",
             "svc_version",
             "svc_namespace",
             "authors",
             "log_file",
             "log_level",
             "logging_enabled"
         ]
        if self.attribute_override is not None and type(self.attribute_override) is dict:
            for attribute in self.attribute_override.keys():
                rarray.append(attribute)
        return rarray
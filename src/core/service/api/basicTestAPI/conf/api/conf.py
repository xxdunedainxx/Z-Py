from ......conf.API.apis.APICoreConfig import APICoreConfig
from ..route.conf import conf as RouterConfiguration

conf=APICoreConfig(
    file=".\\src\\core\\service\\api\\basicTestAPI\\conf\\api\\conf.json",
    routerConfig=RouterConfiguration)
conf.initialize_config()

print("conf done :)")
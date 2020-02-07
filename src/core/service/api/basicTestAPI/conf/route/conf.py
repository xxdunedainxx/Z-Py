from ......conf.API.routes.RouteConfig import RouteConfig
conf=RouteConfig(file=".\\src\\core\\service\\api\\basicTestAPI\\conf\\route\\conf.json")
conf.initialize_config()

print("conf done :)")
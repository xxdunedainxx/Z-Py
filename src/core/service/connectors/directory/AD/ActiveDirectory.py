from ldap3 import Server, Connection, ALL
from ..DirectorySystem import DirectorySystem
from .....conf.ServiceConfig import ServiceConfig
from .....util.app.ErrorFactory.build.BuildErrors import MissingConfiguration

class ADConnector(DirectorySystem):

    def __init__(self,ldapConf: ServiceConfig = None, server = "", user = "", pw = "", userOU="", groupOU="", autoConnect: bool = False):
        super().__init__(connectorConfig=ldapConf)

        if ldapConf is None:
            self.ad_server = server
            self.bind_username = user
            self.bind_password = pw
            self.bind_server = None
            self.ad_connection = None
            self.autoConnect=autoConnect
        else:
            self.__extract_conf_attributes(ldapConf=ldapConf)

        if self.autoConnect:
            self.ad_connect()
        if userOU is "" or groupOU is "":
            print(
                "WARNING, userOU and groupOU are blank. This will effect the get_ad_user and get_ad_group methods. You can set ")
        self.userOU = userOU
        self.groupOU = groupOU

    def __extract_conf_attributes(self, ldapConf: ServiceConfig):
        required_attributes = ["ad_server","bind_username", "bind_password"]
        optional_attributes = ["userOU", "groupOU", "autoConnect"]
        # Defaults override

        for req in required_attributes:
            if hasattr(ldapConf, req):
                setattr(self, req, (getattr(ldapConf,req)))
            else:
                MissingConfiguration(file="ADConnector", config=req)

        for opt in optional_attributes:
            if hasattr(ldapConf, opt):
                setattr(self, opt, (getattr(ldapConf,opt)))

    def ad_get(self, baseDN, searchFilter, attributes=['samAccountName','distinguishedName','objectCategory'], size_limit=5000):
        if self.ad_connection is None:
            raise Exception('ldap_get error -- An ldap connection does not exist! ldap_connection is None')

        try:
            getData = self.ad_connection.search(baseDN, searchFilter, attributes=attributes, size_limit=size_limit,
                                                paged_size=size_limit)
            if getData is True:
                ad_return_objects = self.ad_connection.entries
                page_cookie = None
                # Paginated results
                if self.ad_connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']:
                    page_cookie = self.ad_connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']

                    while page_cookie:
                        getData = self.ad_connection.search(baseDN, searchFilter, attributes=attributes,
                                                            size_limit=size_limit, paged_size=size_limit,
                                                            paged_cookie=page_cookie)
                        ad_return_objects.extend(self.ad_connection.entries)

                        if self.ad_connection.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']:
                            page_cookie = self.ad_connection.result['controls']['1.2.840.113556.1.4.319']['value'][
                                'cookie']
                        else:
                            page_cookie = None
                            return ad_return_objects
                else:
                    return self.ad_connection.entries
            else:
                return None
        except Exception as e:
            print(str(e))

    def get_ad_user(self, filter, attributes=['samAccountName','distinguishedName','objectCategory'], size_limit=5000):
        return self.ad_get(self.userOU, filter, attributes, size_limit)

    def get_ad_group(self, filter, attributes=['samAccountName','distinguishedName','objectCategory']):
        return self.ad_get(self.groupOU, filter, attributes)

    def ad_connect(self):
        if self.ad_connection is None:
            self.bind_server = Server(self.ad_server, get_info=ALL)
            try:
                self.ad_connection = Connection(self.bind_server, self.bind_username, self.bind_password,
                                                auto_bind=True)
            except Exception as e:
                print(str(e))
        else:
            raise Exception(
                'ldap_connector error -- an existing ldap connection already exists for this class instance')

    def ad_reset_connection(self, server, user, pw):
        # can be used to unbind / rebind to an AD / LDAP server
        if self.ad_connection is None:
            self.ad_connect(self)
        else:
            self.ad_connection.unbind()
            self.ad_connection = None
            self.ldap_server = server
            self.bind_username = user
            self.bind_password = pw
            self.ad_connect(self)

    def get_org_users(self, managerName, attributes):
        directReports = []
        if "directReports" not in attributes:
            attributes.append("directReports")

        manager = self.get_ad_user(f"(samaccountname={managerName})", attributes=attributes)

        if manager is not None and len(manager) > 0 and len(manager[0].directReports) > 0:
            directReports.extend(manager)
            for direct in manager[0].directReports:
                directRepAd = self.get_ad_user(filter=f"(samaccountname={self.split_dn(direct)})",
                                               attributes=attributes)
                if directRepAd is not None and len(directRepAd) > 0:
                    if len(directRepAd[0].directReports) > 0:
                        # recursive call
                        directReports.extend(
                            self.get_org_users(managerName=self.split_dn(direct), attributes=attributes))
                    else:
                        directReports.extend(directRepAd)
        else:
            return manager

        return directReports

    def split_dn(self, dn):
        return dn.split("=")[1].split(",")[0]

    def ldap_close(self):
        self.ad_connection.unbind()


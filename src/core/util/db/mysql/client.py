import pymysql as mysql

class py_mysql:

    SQL_BOOLS=["and", "or"]

    def __init__(self, config, autoCommit=False):
        self.mysqlConfig = None
        self._connection = None
        self._cursor = None
        self.newConnection(config, autoCommit)

    def setMySQLConnection(self, config, autoCommit=False):
        self.mysqlConfig = config
        self._connection = mysql.connect(host=config['host'], user=config['user'], password=config['password'],
                                         db=config['database'], autocommit=autoCommit)

    def newConnection(self, config, autoCommit=False):
        if (self._connection is not None) and (self._connection.open is True):
            self.killConnection()
        self.setMySQLConnection(config, autoCommit)

        self._cursor = self._connection.cursor()

    def killCursor(self):
        if self._cursor is not None:
            self._cursor.close()
            self._cursor=None

    def initCursor(self, nCursor = None):
        self.killCursor()
        if nCursor is None:
            self._cursor = self._connection.cursor()
        else:
            self._cursor=nCursor

    def killConnection(self):
        self._cursor.close()
        if self._connection.open is True:
            self._connection.close()

    def __getAllQuery(self,query, paramatized=None):
        self.initCursor()
        if paramatized is None:
            self._cursor.execute(query)
        else:
            self._cursor.execute(query, (paramatized))

        if (self._cursor.rowcount is 0) or (self._cursor.description is None):
            return None
        else:
            r= self._cursor.fetchall()
            self.killCursor()
            return r
    def executeQuery(self, query, paramatized=None,fetchAll=True):
        if fetchAll:
            return self.__getAllQuery(query=query, paramatized=paramatized)

        if paramatized is None:
            self._cursor.execute(query)
        else:
            self._cursor.execute(query, (paramatized))
        if (self._cursor.rowcount is 0) or (self._cursor.description is None):
            return None


    def fetchItem(self):
        return self._cursor.fetchone()
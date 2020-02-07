class DB_Return_Flag:

    success="200"
    not_found="404"
    duplicate="409"
    error="500"

    def __init__(self, flag: str, content: object=None):
        self.contnet=content
        self.flag=flag
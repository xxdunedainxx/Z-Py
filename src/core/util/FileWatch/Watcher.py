import os
from datetime import datetime

class FileWatcher():

    def __init__(self, files: [str]):
        self.files : [str] = files
        self.last_modified_times: {} = {}

        self._init_modify_times()

    def _init_modify_times(self)->None:
        for f in self.files:
            self.last_modified_times[f]=self.get_modify_time_helper(file=f)

    def is_modified_single(self, file: str)->bool:
        last_modify=self.get_modify_time_helper(file=file)

        if last_modify != self.last_modified_times[file]:
            self.last_modified_times[file]=last_modify
            return True
        else:
            return False

    def is_modified_all(self)->{bool}:
        rHash: {} = {}

        for f in self.files:
            rHash[f]=self.is_modified_single(file=f)

        return rHash

    def get_modify_time_helper(self, file: str)->datetime:
        return datetime.utcfromtimestamp(os.stat(file).st_mtime)
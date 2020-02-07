from datetime import datetime
import os

"""
LOG LEVELS DEFINED 
    DEBUG: Information interesting for Developers, when trying to debug a problem.
    INFO: Information interesting for Support staff trying to figure out the context of a given error
    WARN to FATAL: Problems and Errors depending on level of damage.
"""



class LogFactory():

    #region Log Levels
    error="ERROR"
    info="INFO"
    trace="TRACE"
    debug="DEBUG"
    warning="WARNING"
    all="ALL"
    #endregion


    def __init__(self,file, log_level="ALL", auto_commit: bool = True):

        # file path
        self._file_path=file
        self._log_level=log_level
        self._auto_commit=auto_commit

        # create log directory if it does not exist
        if self._dir_exists() == False and (self._is_local_path(file=file) == False):
            self._create_log_direrctory()

        # Establish file stream
        self.establish_file_stream()

    def _is_local_path(self, file):
        if os.sep not in file:
            return True
        else:
            return False

    def establish_file_stream(self):
        self._file_stream=open(self._file_path,'a')

    def dispose_stream(self):
        if self._file_stream.closed is False:
            self._file_stream.close()

    def _create_log_direrctory(self,f=None):
        if f is None:
            os.mkdir(self._parse_directory_from_file(self._file_path))
        else:
            os.mkdir(self._parse_directory_from_file(f))

    def _parse_directory_from_file(self,file):
        # Probs a better way to do this lol
        t=file.split(os.sep)
        t=t[:(len(t) - 1)]

        directory=""
        for d in t:
            directory+=f"{d}{os.sep}"

        return directory

    def _dir_exists(self):
        if os.path.isdir(self._parse_directory_from_file(self._file_path)):
            return True
        else:
            return False
    def commit_data(self):
        self._file_stream.flush()

    def write_log(self,data,level="INFO"):
        # If the level is enabled to to cached
        if LogFactory.LOG_LEVELS(level,self._log_level):
            msg=f"[{level}: {str(datetime.now())}] {data}\n"
            print(msg)
            self._file_stream.write(msg)
            if self._auto_commit:
                self.commit_data()

    @staticmethod
    def LOG_LEVELS(level,logger_level):
        levels={
            LogFactory.debug : [LogFactory.debug, LogFactory.warning,LogFactory.error],
            'INFO' : [LogFactory.info,LogFactory.warning,LogFactory.error],
            'TRACE' : [LogFactory.debug,LogFactory.warning,LogFactory.error,LogFactory.info, LogFactory.trace],
            'ALL' : [LogFactory.debug,LogFactory.warning,LogFactory.error,LogFactory.info, LogFactory.trace],
            'ERROR' : [LogFactory.error]
        }

        if level in levels[logger_level]:
            return True
        else:
            return False


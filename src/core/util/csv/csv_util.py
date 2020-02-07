# For CSV Export
import csv
import os
import datetime
import shutil

# CSV Export helpers
class CSV_Util():
    def __init__(self, headers: [str], file_name: str):
        self.headers: [str]=headers
        self.name : str=file_name


        self.csv_writer: csv.DictWriter= self.create_csv()
    #region create_csv
    def create_csv(self)->csv.DictWriter:
        writer = csv.DictWriter(open(self.name, 'w+', newline="\n"), fieldnames=self.headers)
        writer.writeheader()
        return writer
    #endregion
    #region write_row
    def write_row(self,row : {}):
        try:
            self.csv_writer.writerow(
                row
            )
        except Exception as e:
            print(e)
    #endregion

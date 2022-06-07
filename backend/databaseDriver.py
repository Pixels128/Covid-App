from datetime import datetime, timedelta
from dataclasses import dataclass
import sqlite3

@dataclass
class DatabaseDriver:
    fileName:str = ''
    def setFile(self, fileName):
        self.fileName = fileName
        return self
    def __run(self, *args):
        con = sqlite3.connect(self.fileName)
        cur = con.cursor()
        cur.execute(*args)
        con.commit()
        output = cur.fetchall()
        con.close()
        return output
    def flagWithCovid(self, uuid, hasCovid=True):
        time = datetime.now()
        self.__run("INSERT OR REPLACE INTO Cases (UserID, hasCovid, ReportedOn) VALUES (?, ?, ?) ", (uuid, hasCovid, time))
    def hasCovid(self, id):
        data = self.__run("SELECT hasCovid FROM Cases WHERE UserID = :userID", {"userID":id})
        if not data: return False
        return bool(data[0][0])
    def dateReported(self, id):
        data = self.__run("SELECT ReportedOn FROM Cases WHERE UserID = :userID", {"userID":id})
        if not data: return None
        return str(data[0][0])

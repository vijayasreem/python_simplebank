# sb_log.py
import os.path
import os
from datetime import datetime
LogDir = "History/"


def Check():
    if not os.path.exists(LogDir):
        os.mkdir(LogDir)

def WriteLog(AccountNumber: int, Message) -> None:
    Check()
    path = f"{LogDir}{AccountNumber}.log"
    if not os.path.exists(path):
        CreateFile(path)
    with open(f"{LogDir}{AccountNumber}.log", 'r+') as file:
        data = file.read()
        file.seek(0, 0)
        file.write(datetime.now().strftime(f"(%Y-%m-%d %H:%M:%S): {Message}")+ '\n' + data)

def CreateFile(filename):
    open(filename, 'a').close()

def ReadLog(AccountNumber: int, Lines=25) -> list:
    Check()
    path = f"{LogDir}{AccountNumber}.log"
    if not os.path.exists(path):
        CreateFile(path)
    lines = []
    with open(path, "r") as file:
        try:
            for i in range(0,Lines):
                lines.append(next(file).strip())
        except StopIteration:
            pass
        finally:
            return lines
    

# sb_dbm.py
import pymysql.cursors
from handler import Handler
import etc
import main
# Database Manager

class NoConnectionError(Exception):
    def __init__(self, message="Database connection unavailable"):
        self.message = message
        super().__init__(message)

class DBHandler(Handler):
    __setup__ = False

    @staticmethod
    def Setup(config : dict) -> None:
        DBHandler.Host=config['host']
        DBHandler.User=config['user']
        DBHandler.Password=config['password']
        #DBHandler.Database=config['database'] -> Causes error at connection when database doesn't exist
        DBHandler.Port=int(config['port'])
        DBHandler.__setup__ = True
        etc.Debug("Database handler ready.")

    @staticmethod
    def Initialize() -> None:
        """Setup database connection."""
        try:
            if not DBHandler.__setup__:
                raise Exception("Database Handler used before setting it up.")
            DBHandler.Connection = pymysql.connect(
                host=DBHandler.Host,
                user=DBHandler.User,
                password=DBHandler.Password,
                #database=DBHandler.Database,
                port=DBHandler.Port,
                charset='utf8',
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor)

        except Exception as x:
            print("An error occurred while setting up connection with the MySQL Database: ", x)
            raise
        else:
            etc.Debug("Database connection estabilished.")

    @staticmethod
    def Deinitialize() -> None:
        DBHandler.Connection.close()

        pass

    @staticmethod
    def Available() -> bool:
        return DBHandler.Connection.open

    @staticmethod
    def GetCursor():
        if not DBHandler.Available():
            raise NoConnectionError()
        return DBHandler.Connection.cursor()

    @staticmethod
    def Execute(Query: str) -> list:
        """Returns multiple Key/Value pairs."""
        if not DBHandler.Available():
            raise NoConnectionError()
        with DBHandler.GetCursor() as cursor:
            cursor.execute(Query)
            return cursor.fetchall()
    @staticmethod
    def ExecuteScalar(Query: str) -> dict:
        """Returns a single Key/Value pair"""
        if not DBHandler.Available():
            raise NoConnectionError()
        with DBHandler.GetCursor() as cursor:
            cursor.execute(Query)
            return cursor.fetchone()
    @staticmethod
    def ExecuteNQuery(Query: str) -> None:
        """Executes query without returning the result"""
        if not DBHandler.Available():
            raise NoConnectionError()
        with DBHandler.GetCursor() as cursor:
            cursor.execute(Query)

    @staticmethod
    def GetDatabases() -> list:
        with DBHandler.GetCursor() as cur:
            cur.execute("SHOW DATABASES")
            return ["".join(x.values()) for x in cur.fetchall()]

    @staticmethod
    def CheckDatabase(config):
        DBHandler.Execute("CREATE DATABASE IF NOT EXISTS "
                          f"{config['database']} CHARACTER SET utf8 "
                          "COLLATE utf8_hungarian_ci")
        DBHandler.Connection.select_db(config['database'])
        DBHandler.Execute("CREATE TABLE IF NOT EXISTS accounts("
                          "account_number BIGINT(19) NOT NULL PRIMARY KEY,"
                          "name VARCHAR(30) NOT NULL,"
                          "gender TINYINT NOT NULL CHECK (gender BETWEEN 0 and 1),"
                          "age TINYINT NOT NULL CHECK (age BETWEEN 0 and 100),"
                          "balance INT NOT NULL DEFAULT 0 CHECK (balance >= 0))")
        DBHandler.Execute("CREATE TABLE IF NOT EXISTS cards("
                          "card_number BIGINT(19) NOT NULL PRIMARY KEY,"
                          "expiry VARCHAR(10) NOT NULL,"
                          "pin SMALLINT(4) NOT NULL,"
                          "cvc SMALLINT(3) NOT NULL,"
                          "account_number BIGINT(19) NOT NULL,"
                          "FOREIGN KEY (account_number) REFERENCES "
                          "accounts(account_number))")

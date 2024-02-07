import random
import etc
from enum import IntEnum as Enum
from database import DBHandler as db


# Bank Accounts
class AccountNullError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Gender(Enum):
    MALE = 0
    FEMALE = 1


class Client():
    def __init__(self, Name, Gender, Age):
        self.Name = Name
        self.Gender = Gender
        self.Age = Age

class Account(Client):
    def __init__(self, Name, Gender, Age, Balance=0, accountNumber=None):
        super().__init__(Name, Gender, Age)
        self.Balance = Balance
        self.AccountNumber = etc.fixedrandom(18) if accountNumber is None else accountNumber # A MySQL csak ennyit enged
        etc.Debug(f"Created Account({Name}, {Gender}): {self.AccountNumber}")

    def __str__(self):
        return f"Account Number: {self.AccountNumber}\nName: {self.Name}\nGender: {self.Gender}\nAge: {self.Age}\nBalance: {self.Balance}"
    @classmethod
    def Deposit(self, Amount):
        self.Balance += Amount

    @classmethod
    def Withdraw(self, Amount):
        self.Balance -= Amount

    @staticmethod
    def FromDBRecord(record):
        return Account(record['name'], record['gender'], record['age'], record['balance'], record['account_number'])

    @staticmethod
    def GetFromDB(AccountNumber):
        query = f"SELECT * FROM accounts WHERE accounts.account_number = {AccountNumber}"
        with db.GetCursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        if result is None:
            etc.Debug("Entry not found in database")
            return None
        else:
            account = Account.FromDBRecord(result)
            return account

    @staticmethod
    def FromCardNumber(CardNumber):
        query=f"SELECT * FROM accounts, cards WHERE accounts.account_number = cards.account_number AND cards.card_number = '{CardNumber}'"
        return Account.FromDBRecord(db.ExecuteScalar(query))

    @staticmethod
    def AddToDB(account):
        if Account.GetFromDB(account.AccountNumber) is None:
            etc.Debug("No such user in db. Adding...")
            with db.GetCursor() as cursor:
                query="INSERT INTO accounts(account_number,name,gender,age,balance) " \
                    f"VALUES('{account.AccountNumber}','{account.Name}',{account.Gender},{account.Age},{account.Balance})"
                try:
                    cursor.execute(query)
                except Exception as x:
                    print("Failed to add Account entry to database: ", x)
                else:
                    etc.Debug("New Account entry: " + str(account))
        else:
            print("User already exists")
#    @classmethod
#    def AddToDB(self):
#        Account.AddToDB(self)

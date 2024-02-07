import account
import random
import etc
from database import DBHandler as db
from account import Account

class Card():
    def __init__(self, AccountNumber: int, Expiry: str = None, PIN: int = None, CVC: int = None, CardNumber: int = None):
        self.Account = AccountNumber
        self.CardNumber = etc.fixedrandom(18) if CardNumber is None else CardNumber
        self.Expiry = etc.getExpiry() if Expiry is None else Expiry
        self.PIN = etc.fixedrandom(4) if PIN is None else PIN
        self.CVC = etc.fixedrandom(3) if CVC is None else CVC
        etc.Debug(f"DEBUG: Created Card {self.CardNumber}:{self.Expiry}:{self.PIN}:{self.CVC}")
        etc.Debug(f"Associated account: {AccountNumber}")

    def __str__(self):
        return f"Card Number: {self.CardNumber}\nExpiry: {self.Expiry}\nPIN: {self.PIN}\nCVC: {self.CVC}\nAccount: {self.Account}"

    @staticmethod
    def GetFromDB(CardNumber):
        query = f"SELECT * FROM cards WHERE cards.card_number = {CardNumber}"
        with db.GetCursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        if result is None:
            etc.Debug("Entry not found in database")
            return None
        else:
            card = Card.FromDBRecord(result)
            #card = Card(
             #   result['card_number'],
             #   result['expiry'],
             #   result['pin'],
#                result['cvc'],
#                result['account_number'],)
            return card
    @classmethod
    def GetAccount(self):
        return Account.GetFromDB(self.CardNumber)
    @staticmethod
    def FromAccount(AccountNumber):
        query = f"SELECT card_number FROM cards WHERE cards.account_number = '{AccountNumber}'"
        cardnum = db.ExecuteScalar(query)['card_number']
        return Card.GetFromDB(cardnum) if cardnum is not None else None

    def FromDBRecord(record):
        return Card(record['account_number'], record['expiry'], record['pin'], record['cvc'], record['card_number'])

    @staticmethod
    def AddToDB(card):
        if Card.GetFromDB(card.CardNumber) is None:
            etc.Debug("No such user in db. Adding...")
            with db.GetCursor() as cursor:
                query="INSERT INTO cards(card_number,expiry,pin,cvc,account_number) " \
                    f"VALUES({card.CardNumber},'{card.Expiry}',{card.PIN},{card.CVC},{card.Account})"
                try:
                    cursor.execute(query)
                except Exception as x:
                    print("Failed to add Card entry to database: ", x)
                else:
                    etc.Debug("New Card entry: " + str(card))
        else:
            print("Card already exists")

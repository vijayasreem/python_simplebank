#!/usr/bin/env python3
# main.py
import conf
import importlib.util
import etc
from account import Account, Gender
from database import DBHandler as db
from card import Card
import os
#from time import sleep
import log
from time import sleep as sl
from datetime import datetime


def sleep(seconds):
    try:
        sl(seconds)
    except KeyboardInterrupt:
        pass

# Verbose
Debug = False
configPath = "Config.json"
defaultConfig = {
    "host": "localhost",
    "user" : "root",
    "password" : "",
    "port" : "3306",
    "database" : "simplebank" }

def Logo():
    if importlib.util.find_spec('pyfiglet'): from pyfiglet import figlet_format as fig; print(fig("SimpleBank"))

def Clear():
    os.system('clear' if os.name == 'posix' else 'cls')

# Entry point
if __name__ == '__main__':
    Config = conf.Read(configPath, defaultConfig)
    db.Setup(Config)
    db.Initialize()
    db.CheckDatabase(Config)

    login=False
    while True:
        if not login:
            # Main Menu
            Clear()
            Logo()
            print("Welcome to SimpleBank!\n\nPlease select from the options found below:")
            print("""
            1. Create new account
            2. Login to existing account
            3. Exit\n""")
            try:
                choice = int(input("Option: "))
            except ValueError:
                print("Invalid Number")
            except KeyboardInterrupt:
                print("\nGoodbye.")

                # Ugly, but prevents KeyboardInterrupt from being raised
                try:
                    sleep(3)
                except:
                    pass
                finally:
                    Clear()
                    exit()
            match choice:
                case 1: # Create Account

                    while True: # Exit only when a new account was successfully created, or when a KeyboardInterrupt occurs
                        Clear()
                        Logo()
                        print("\nPlease enter your Personal Data below:\n")
                        try:
                            name=input("Name: ")
                            gender=input("Gender: ")
                            if gender.lower() == "male":
                                gender=0
                            elif gender.lower() == "female":
                                gender=0
                            else:
                                print("Invalid gender.\nPossible values: Male, Female")
                                sleep(3)
                                continue
                            age=int(input("Age: "))
                            if age > 100 or age <= 0:
                                print("Invalid age entered, please try again.")
                                sleep(3)
                                continue
                        except KeyboardInterrupt:
                            break
                        except ValueError:
                            print("Invalid Number, please try again.")
                        else:
                            # List details, create account
                            newacc = Account(name,gender,age)
                            Account.AddToDB(newacc)
                            newcard = Card(newacc.AccountNumber)
                            Card.AddToDB(newcard)

                            try:
                                print("\nAccount Details:\n")
                                print(newacc)
                                print("\nCard Details:\n")
                                print(newcard)
                                print("\nSuccessfully created new account.\nPlease save your card information, then press Enter to return to the main menu.\n")
                                input()
                            except:
                                pass
                            finally:
                                break
                case 2: # Login
                    while not login: # Only exit when valid credentials were entered, or a KeyboardInterrupt occurs
                        Clear()
                        Logo()
                        print("Please enter your credentials to login:\n")

                        try:
                            name=input("Name: ")
                            cardnum=int(input("Card Number: "))
                            cvc=int(input("CVC Number: "))
                            pin=int(input("PIN: "))
                            expiry=input("Expiry(YY/MM): ")
                        except ValueError:
                            print("Invalid Number, please try again.")
                        except KeyboardInterrupt:
                            break
                        else:
                            query=(f"SELECT * FROM cards WHERE cards.card_number = {cardnum} AND "
                                    f"(SELECT accounts.name FROM accounts, cards "
                                    f"WHERE cards.card_number = '{cardnum}' AND "
                                    f"accounts.account_number = cards.account_number)='{name}' "
                                    f"AND cards.cvc = {cvc} AND cards.pin = {pin} "
                                    f"AND cards.expiry = '{expiry}'")
                            result = db.ExecuteScalar(query)
                            if result is None:
                                print("Invalid credentials. Please try again, or Interrupt to return to main menu.")
                                sleep(2)
                                continue
                            else:
                                global card
                                card = Card.FromDBRecord(result)
                                global account
                                account = Account.FromCardNumber(card.CardNumber)
                                print ("\nSuccessfully logged in.\n")
                                login = True
                                try:
                                    sleep(2)
                                except KeyboardInterrupt:
                                    pass
                case 3:
                    print("Bye")
                    try:
                        sleep(2)
                    except:
                        pass
                    finally:
                        Clear()
                        exit()
                case other:
                    print("Invalid option.")
                    sleep(2)
        else:
            while True:
                Clear()
                Logo()
                print("Please choose from the options below:")
                print("""
                1. View Balance
                2. Withdraw
                3. Deposit
                4. Transaction History
                5. Make Transaction\n""")
                try:
                    option = int(input("Choice: "))
                except KeyboardInterrupt:
                    login = False
                    print("\nSuccessfully Logged out.\n")
                    account = None
                    card = None
                    sleep(2)
                    break
                except ValueError:
                    print("Invalid Number.")
                    try:
                        sleep(2)
                    except KeyboardInterrupt:
                        pass
                else:
                    match option:
                        case 1:
                            Clear()
                            Logo()
                            try:
                                print("\nYour current balance: $" + str(account.Balance))
                                input("\nPress Enter to continue.\n")
                            except KeyboardInterrupt:
                                pass
                            finally:
                                continue
                        case 2:
                            while True:
                                Clear()
                                Logo()
                                try:
                                    amount = int(input("\nPlease enter amount to Withdraw: "))
                                except ValueError:
                                    print("Invalid number.")
                                except KeyboardInterrupt:
                                    break
                                else:
                                    if amount <= 0:
                                        print("Please enter a positive number.")
                                        sleep(2)
                                        continue
                                    if amount > account.Balance:
                                        print("Entered amount exceeds your available balance.")
                                        sleep(2)
                                        continue
                                    else:
                                        account.Balance -= amount
                                        db.ExecuteNQuery(f"UPDATE accounts SET accounts.Balance = {account.Balance} WHERE accounts.account_number = {account.AccountNumber}")
                                        print(f"\nSuccessfully withdrawn ${amount}. New Balance: {account.Balance}\n")
                                        log.WriteLog(account.AccountNumber, f"Withdrawn ${amount}")
                                        input("\nPress Enter to continue")
                                        break
                            pass
                        case 3:
                            while True:
                                Clear()
                                Logo()
                                try:
                                    amount = int(input("\nPlease enter amount to Deposit: "))
                                except ValueError:
                                    print("Invalid number.")
                                except KeyboardInterrupt:
                                    break
                                else:
                                    if amount <= 0:
                                        print("Please enter a positive number.")
                                        sleep(2)
                                        continue
                                    else:
                                        account.Balance += amount
                                        db.ExecuteNQuery(f"UPDATE accounts SET accounts.Balance = {account.Balance} WHERE accounts.account_number = {account.AccountNumber}")
                                        print(f"\nSuccessfully deposited ${amount}. New Balance: {account.Balance}\n")
                                        log.WriteLog(account.AccountNumber, f"Deposited ${amount}")
                                        input("\nPress Enter to continue.")
                                        break
                        case 4:
                            while True:
                                Clear()
                                Logo()
                                try:
                                    reply = input("\nEnter the amount of lines to be displayed (Default: 25): ")
                                    if not reply:
                                        amount = 25
                                    else:
                                        amount = int(reply)
                                except ValueError:
                                    print("Invalid number.")
                                    sleep(2)
                                    continue
                                except KeyboardInterrupt:
                                    break
                                else:
                                    if amount <= 0 or amount > 100:
                                        print("Please enter a number between 0 and 100.")
                                        sleep(2)
                                        continue
                                    print(f"\nTransaction History:\n")
                                    history = log.ReadLog(account.AccountNumber, amount)
                                    if not len(history):
                                        print("No recorded transactions yet.")
                                    else:
                                        [print(x) for x in history]
                                    input("\nPress Enter to continue.")
                                    break
                        case 5:
                            while True:
                                Clear()
                                Logo()
                                try:
                                    accnum = int(input("\nEnter Account Number to transfer to: "))
                                    amount = int(input("Enter amount to transfer: "))
                                except KeyboardInterrupt:
                                    break
                                except ValueError:
                                    print("Invalid number.")
                                    continue
                                else:
                                    if accnum == account.AccountNumber:
                                        print("Please enter an account number other than your own.")
                                        sleep(2)
                                        continue
                                    target = Account.GetFromDB(accnum)
                                    if target is None:
                                        print("Target account doesn't exist.")
                                        sleep(2)
                                        continue

                                    if amount <= 0:
                                        print("Please enter a positive number.")
                                    elif amount > account.Balance:
                                        print("Entered ammount exceeds your current balance.")
                                        sleep(2)
                                        continue
                                    account.Balance -= amount
                                    db.ExecuteNQuery(f"UPDATE accounts SET accounts.balance = {account.Balance} WHERE accounts.account_number = {account.AccountNumber}")
                                    target.Balance += amount
                                    db.ExecuteNQuery(f"UPDATE accounts SET accounts.balance = {account.Balance} WHERE accounts.account_number = {target.AccountNumber}")
                                    log.WriteLog(account.AccountNumber, f"Transferred ${amount} to {target.Name} ({target.AccountNumber})")
                                    log.WriteLog(accnum, f"Receieved ${amount} from {account.Name} ({account.AccountNumber})")
                                    print(f"Successfully transferred ${amount} to {target.Name} ({target.AccountNumber}).")
                                    input("\nPress Enter to continue")
                                    break
    #Cleanup
    db.Deinitialize()


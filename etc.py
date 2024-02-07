from random import randint as rand
from datetime import datetime, timedelta
from main import Debug as debug
from time import sleep
# Helper functions

def fixedrandom(n: int) -> int:
    """Fixed length random"""
    return rand(10**(n-1), (10**n)-1)


def getExpiry() -> str:
    expiry = datetime.today() + timedelta(days=1460)
    return f"{expiry.strftime('%y/%m')}"

# Why not
def Debug(Message: str) -> None:
    if debug:
        print(f"DEBUG: {Message}")

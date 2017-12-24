import os
import sys

class Account:
    ID = 0
    NAME = ""
    TYPE = 0
    CURRENCY = 0
    RATE_TO = 0.0
    BALANCE = 0.0

    def __init__(self, name):
        pass

    def check_sanity(self):
        pass
        # Verify account db file exist
        ## Configure:
        ### account name
        ### currency
        ### account type
        ### conversion rate
        ### transaction lookup table

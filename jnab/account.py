import os
import sys

class Account:

    def __init__(self, account_dict):
        self.ID = 0
        self.NAME = ""
        self.TYPE = 0
        self.CURRENCY = 0
        self.RATE_TO = 0.0
        self.BALANCE = 0.0

    def check_sanity(self):
        pass
        # Verify account db file exist
        ## Configure:
        ### account name
        ### currency
        ### account type
        ### conversion rate
        ### transaction lookup table

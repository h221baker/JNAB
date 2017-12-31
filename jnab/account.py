import os
import sys

class Account:

    def __init__(self, account_dict):
        self.ID = account_dict['ID']
        self.NAME = account_dict['NAME']
        self.TYPE = account_dict['TYPE']
        self.CURRENCY = account_dict['CURRENCY']
        self.RATE_TO = account_dict['RATE_TO']
        self.BALANCE = account_dict['BALANCE']

    def check_sanity(self):
        pass
        # Verify account db file exist
        ## Configure:
        ### account name
        ### currency
        ### account type
        ### conversion rate
        ### transaction lookup table

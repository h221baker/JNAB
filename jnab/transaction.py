import logging

import datetime
from enum import Enum

from util import get_logger

logger = get_logger("transaction")


class TransactionError(Exception):
    pass


class TransactionInvalidAttributeError(TransactionError):
    pass


class Type(Enum):
    CREDIT = 1
    DEBIT = 2
    TRANSFER = 3


class Transaction(object):
    transaction_db_attributes = [
        'ID', 'DATE', 'NAME', 'TYPE', 'BUDGET_ID', 'AMOUNT', 'META', 'CLEAR'
    ]

    def __init__(self, transaction_dict={}):
        for key in transaction_dict:
            if key in self.transaction_db_attributes:
                self.__setattr__(key, transaction_dict[key])

    def __setattr__(self, name, value):
        if name not in self.transaction_db_attributes:
            raise TransactionInvalidAttributeError(
                "Invalid Transaction object attribute %s" % name)

        if name is "DATE" and value:
            datetime.datetime.strptime(value, "%Y-%m-%d")

        super.__setattr__(self, name, value)

    def check_sanity(self):
        for attr in self.transaction_db_attributes:
            if not hasattr(self, attr):
                return False
        return True
        # TODO: more in depth check of each attribute with type and content

    def _dict(self):
        account_dict = {}
        for attr in self.transaction_db_attributes:
            account_dict[attr] = self.__getattribute__(attr)
        return account_dict

    def __repr__(self):
        return repr(self._dict())

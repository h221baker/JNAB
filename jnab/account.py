import logging

import datetime
from enum import Enum

import util
import db

logger = util.get_logger("account")


class Currency(Enum):
    USD = 1     # US Dollar
    EURO = 2    # EURO
    CHF = 3     # Swish Franc
    CNY = 4     # Chinese Yuan
    CAD = 5     # Canadian Dollar


class Type(Enum):
    CHECKING = 1
    CREDIT = 2
    CASH = 3


class AccountError(Exception):
    pass


class AccountInvalidAttributeError(AccountError):
    pass


class Account(object):

    # TODO: Quick adjust account balance

    account_db_attributes = [
            'ID',
            'NAME',
            'TYPE',
            'CURRENCY',
            'RATE_TO',
            'BALANCE',
            'ACTIVE']

    def __init__(self, account_dict={}):
        for key in account_dict:
            if key in self.account_db_attributes:
                self.__setattr__(key, account_dict[key])

    def __setattr__(self, name, value):
        if name not in self.account_db_attributes:
            raise AccountInvalidAttributeError(
                    "Invalid Account object attribute %s" % name)
        # Do not allow permenent account attribute to be changed
        if name in ['ID', 'NAME', 'CURRENTY', 'TYPE'] and hasattr(self, name):
            raise AccountInvalidAttributeError(
                    "Unable to change existing permenent"
                    "account attribute %s" % name)

        # TODO: Peform type check for value set

        # Modify the some attributes before setting it
        if name == 'TYPE':
            if type(value) is int:
                super.__setattr__(self, name, Type(value))
            elif type(value) is str:
                super.__setattr__(
                        self,
                        name,
                        Type(Type.__getattr__(value.upper()).value))
            else:
                raise ValueError("Illegal value type %s" % repr(type(value)))
        elif name == 'CURRENCY':
            if type(value) is int:
                super.__setattr__(self, name, Currency(value))
            elif type(value) is str:
                super.__setattr__(
                        self,
                        name,
                        Currency(Currency.__getattr__(value.upper()).value))
            else:
                raise ValueError("Illegal value type %s" % repr(type(value)))
        elif name == 'NAME':
            super.__setattr__(self, name, value.upper())
        else:
            super.__setattr__(self, name, value)

    def _dict(self):
        account_dict = {}
        for attr in self.account_db_attributes:
            if attr == 'TYPE' or attr == 'CURRENCY':
                account_dict[attr] = self.__getattribute__(attr).value
            else:
                account_dict[attr] = self.__getattribute__(attr)
        return account_dict

    def __repr__(self):
        return repr(self._dict())

    def __str__(self):
        # TODO use corresponding unicode currency symbol
        return "%d - %s: $%f; %s, %s, RATE(%f)" % \
            (self.ID,
                self.NAME,
                self.BALANCE,
                self.CURRENCY.name,
                self.TYPE.name,
                self.RATE_TO)

    def check_sanity(self):
        for attr in self.account_db_attributes:
            if not hasattr(self, attr):
                logger.debug(
                        "Missing attr %s in account_obj" % attr)
                return False
        return True
        # TODO: more in depth check of each field with type and content
        """
        - Configure:
        -- account name
        -- currency
        -- account type
        -- conversion rate
        -- transaction lookup table
        """

    def get_transaction(self, transaction_id):
        return db.DB.get_instance().get_transaction(self, transaction_id)

    def add_transaction(self, transaction_obj):
        if not transaction_obj.DATE:
            transaction_obj.DATE = str(datetime.date.today())

        # TODO: Check if is transfer transaction, if so create new
        #       Transaction for corresponding account and link 2 transactions
        #       If transfer from account with different currency, need to 
        #       prompt user for exchange rate, or amount in origin currency

        # TODO: Update account BALANCE, make sure it is not in negative,
        #       else reject transaction
        if self.BALANCE >= transaction_obj.AMOUNT:
            self.BALANCE = self.BALANCE - transaction_obj.AMOUNT

        transaction_obj.META = None
        db.DB.get_instance().add_transaction(self, transaction_obj)

        # TODO: Update RATE_TO if is transfer transaction

        # Update account data in DB
        db.DB.get_instance().modify_account(self)


    def del_transaction(self, transaction_id):
        return db.DB.get_instance().del_transaction(self, transaction_id)

    def modify_transaction(self, transaction_obj):
        return db.DB.get_instance().modify_transaction(self, transaction_obj)

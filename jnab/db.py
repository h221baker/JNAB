import os
import sys

import logging
import tinydb

from . import account

DEFAULT_DB_FILENAME = 'jnab_db.json'
ACCOUNTS_TABLE_NAME = "ACCOUNTS"
ACCOUNT_TABLE_FORMAT = "JNAB_ACCOUNT_%d"
BUDGETS_TABLE_NAME = "BUDGETS"

class DBLookupError(Exception):
    pass

class DBAccountLookupError(DBLookupError):
    pass

class DBTransactionLookupError(DBLookupError):
    pass

class DBAddError(Exception):
    pass

class DBAccountAddError(DBAddError):
    pass

class DB:

    def __init__(self, db_path, create_new=False):
        if db_path and os.path.exists(db_path):
            self.db = tinydb.TinyDB(db_path)
            if ACCOUNTS_TABLE_NAME in self.db.tables():
                self.accounts_table = self.db.table(ACCOUNTS_TABLE_NAME)
            else:
                raise ValueError("Invalid DB, missing 'accounts' table!")
        elif db_path and create_new:
            logging.info("DB file (%s) is missing, and create_new=%s, hence creating new DB!!" % (db_path, create_new))
            self.db = tinydb.TinyDB(db_path)
            self.accounts_table = self.db.table(ACCOUNTS_TABLE_NAME)
        else:
            raise ValueError("Unexpected dbindex file (%s) is missing" % db_path)

        self.db_path = db_path
        self.account_obj_list = {}


    def _close(self):
        self.db.close()

    def get_transaction(self, transaction_id):
        pass

    def add_transaction(self, account_obj, transaction_obj):
        pass

    def del_transaction(self, account_obj, transaction_obj):
        pass

    def modify_transaction(self, account_obj, transaction_obj):
        pass

    def get_account(self, account_name):
        # Look up if this account have already been loaded
        if account_name in self.account_obj_list:
            assert self.account_obj_list[account_name]
            return self.account_obj_list[account_name]

        # Nop, now load the account from the database
        account_query = tinydb.Query()
        accounts = self.accounts_table.search(account_query.NAME == account_name)
        if not accounts:
            raise DBAccountLookupError("Account '%s' does not exist." % account_name)
        elif len(accounts) > 1:
            raise DBAccountLookupError("Multiple accounts with similar account name found.")
        else:
            new_account_obj = account.Account(accounts[0])

            # An account is found, simple sanity check it have correct number of fields
            # TODO: more complicated sanity check can be added to account, and used as part
            # of overall DB checkup.
            if new_account_obj.check_sanity():
                raise ValueError("Invalid accounts data for account '%s'." % account_name)

            self.account_obj_list[account_name] = new_account_obj
            return new_account_obj;

    def add_account(self, account_obj):
        # Look up if this account have already exist
        try:
            self.get_account(account_obj.NAME)
        except DBAccountLookupError as e:
            # If a DBAccountLookupError is observed that mean the account does not exist
            pass
        else:
            # else throw error that duplicate account is attempted to be created
            raise DBAccountAddError("Attempting add new account with dupicate name '%s'" % account_obj.NAME)

        # TODO: create new table for new account, insert table object into accounts table

    def del_account(self, account_obj):
        pass

    def modify_account(self, new_account_obj):
        pass

    def stage_change(self):
        pass

    def commit(self):
        pass

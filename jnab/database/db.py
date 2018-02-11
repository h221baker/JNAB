import os
import sys

import tinydb

import account
from util import *

DEFAULT_DB_FILENAME = 'jnab_db.json'
ACCOUNTS_TABLE_NAME = "ACCOUNTS"
ACCOUNT_TABLE_NAME_FORMAT = "JNAB_ACCOUNT_%d"
BUDGETS_TABLE_NAME = "BUDGETS"

logger = get_logger("db")


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


class DBDelError(Exception):
    pass


class DBAccountDelError(DBDelError):
    pass


class DB(object):

    singleton_db_obj = None

    @classmethod
    def get_instance(cls):
        return cls.singleton_db_obj

    def __init__(self, db_path, create_new=False):
        if DB.singleton_db_obj:
            raise RuntimeError("An instance of DB already exist!")

        if db_path and os.path.exists(db_path):
            self.db = tinydb.TinyDB(db_path)
            if ACCOUNTS_TABLE_NAME not in self.db.tables():
                self.db.close()
                raise ValueError("Invalid DB, missing 'accounts' table!")
        elif db_path and create_new:
            logger.info(
                    "DB file (%s) is missing,"
                    "and create_new=%s, hence creating new DB!!" %
                    (db_path, create_new))
            self.db = tinydb.TinyDB(db_path)
        else:
            raise ValueError(
                    "Unexpected dbindex file (%s) is missing" % db_path)

        accounts_table = self.db.table(ACCOUNTS_TABLE_NAME)
        self.accountOverview =
            db_account_overview.DBAccountOverview(accounts_table)
        self.account_obj_list = {}

        DB.singleton_db_obj = self

    def _close(self):
        # TODO: check DB sanity and push and pending transactions
        self.db.close()
        DB.singleton_db_obj = None

    def get_recent_transactions(self, account_obj, n=None):
        pass

    def get_transaction(self, account_obj, transaction_id):
        pass

    def add_transaction(self, account_obj, transaction_obj):
        # Get corresponding db table for account
        account_table = self.db.table(
                ACCOUNT_TABLE_NAME_FORMAT % account_obj.ID)
        transaction_obj.ID = account_table._get_next_id()
        account_table.insert(transaction_obj._dict())

    def del_transaction(self, account_obj, transaction_id):
        pass

    def modify_transaction(self, account_obj, new_transaction_obj):
        pass

    def add_account(self, **kwarg):
        return self.accountOverview.add_account(*kwarg)

    def del_account(self, **kwarg):
        return self.accountOverview.del_account(*kwarg)
        account_query = tinydb.Query()
        if account_id and account_name:
            del_account_obj = self.get_account(
                    account_id=account_id,
                    account_name=account_name)
            del_account_obj.ACTIVE = False
            self.accounts_table.update(
                    del_account_obj._dict(),
                    ((account_query.ID == del_account_obj.ID) &
                        (account_query.NAME == del_account_obj.NAME)))
        elif account_id:
            del_account_obj = self.get_account(account_id=account_id)
            del_account_obj.ACTIVE = False
            self.accounts_table.update(
                    del_account_obj._dict(),
                    account_query.ID == del_account_obj.ID)
        elif account_name:
            del_account_obj = self.get_account(account_name=account_name)
            del_account_obj.ACTIVE = False
            self.accounts_table.update(
                    del_account_obj._dict(),
                    account_query.NAME == del_account_obj.NAME)

    def modify_account(self, updated_account_obj):
        account_query = tinydb.Query()
        # Expect an account object that was created via get_account() function
        if (updated_account_obj.ID not in self.account_obj_list) or \
                (updated_account_obj !=
                    self.account_obj_list[updated_account_obj.ID]):
            raise DBLookupError(
                    "Invalid updated_account_obj %s" % updated_account_obj)

        self.accounts_table.update(
                updated_account_obj._dict(),
                ((account_query.NAME == updated_account_obj.NAME) &
                    (account_query.ID == updated_account_obj.ID)))

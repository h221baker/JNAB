import os
import sys

import tinydb

import account
from util import *
from . import db_account_overview


DEFAULT_DB_FILENAME = 'jnab_db.json'
ACCOUNTS_TABLE_NAME = "ACCOUNTS"
ACCOUNT_TABLE_NAME_FORMAT = "JNAB_ACCOUNT_%d"
BUDGETS_TABLE_NAME = "BUDGETS"

logger = get_logger("db")


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
        self.accountOverview = \
            db_account_overview.DBAccountOverview(accounts_table)

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

    def get_all_accounts(self, *warg, **kwarg):
        return self.accountOverview.get_all_accounts(*warg, **kwarg)

    def get_account(self, *warg, **kwarg):
        return self.accountOverview.get_account(*warg, **kwarg)

    def add_account(self, *warg, **kwarg):
        account_obj = self.accountOverview.add_account(*warg, **kwarg)

        # Create new accoutns table using the account id
        # TODO: Test this
        logger.info(
                "Creating new account transaction table for account ID %s" %
                account_obj.ID)
        self.db.table(ACCOUNT_TABLE_NAME_FORMAT % account_obj.ID)

    def del_account(self, *warg, **kwarg):
        return self.accountOverview.del_account(*warg, **kwarg)

    def modify_account(self, *warg, **kwarg):
        return self.accountOverview.modify_account(*warg, **kwarg)

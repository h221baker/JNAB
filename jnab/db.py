import os
import sys

import logging
import tinydb

DEFAULT_DB_FILENAME = 'jnab_db.json'
ACCOUNTS_TABLE_NAME = "ACCOUNTS"
ACCOUNT_TABLE_FORMAT = "JNAB_ACCOUNT_%d"
BUDGETS_TABLE_NAME = "BUDGETS"


class DB:
    db_path = ""

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
            self.db.table(ACCOUNTS_TABLE_NAME)
        else:
            raise ValueError("Unexpected dbindex file (%s) is missing" % db_path)

    def _close(self):
        self.db.close()

    def lookup_account(self, account_name):
        pass

    def lookup_transaction(self, transaction_id):
        pass

    def add_transaction(self, account_obj, transaction_obj):
        pass

    def del_transaction(self, account_obj, transaction_obj):
        pass

    def modify_transaction(self, account_obj, transaction_obj):
        pass

    def add_account(self, account_obj):
        pass

    def del_account(self, account_obj):
        pass

    def modify_account(self, new_account_obj):
        pass

    def stage_change(self):
        pass

    def commit(self):
        pass

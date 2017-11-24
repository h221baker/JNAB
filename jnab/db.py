import os
import sys

import logging
import tinydb

DEFAULT_DB_FILENAME = 'jnab_db.json'

class DB:
    db_path = ""

    def __init__(self, db_path, create_new=False):
        # Load the index table from database
        if not db_path or os.path.exists(db_path):
            # TODO maybe figure out the folder to create the db
            logging.info("Loading default DB")
            db_path = DEFAULT_DB_FILENAME

        if os.path.exists(db_path):
            db = tinydb.TinyDB(db_path)
            print(db)
        elif create_new:
            logging.info("DB file (%s) is missing, and create_new=%s, hence creating new DB!!" % (db_path, create_new))
        else:
            logging.error("Unexpected dbindex file (%s) is missing" % db_path)


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

import os
import sys

import logging
import tinydb

from . import account

DEFAULT_DB_FILENAME = 'jnab_db.json'
DEFAULT_TABLE_NAME = "_default"
ACCOUNTS_TABLE_NAME = "ACCOUNTS"
ACCOUNT_TABLE_NAME_FORMAT = "JNAB_ACCOUNT_%d"
BUDGETS_TABLE_NAME = "BUDGETS"

NEXT_ACCONUT_ID_FIELD_NAME = "NEXT_ACCOUNT_ID"

logger = logging.getLogger("db")
logger.setLevel(logging.DEBUG)

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
            if ACCOUNTS_TABLE_NAME in self.db.tables() and DEFAULT_TABLE_NAME in self.db.tables():
                self.accounts_table = self.db.table(ACCOUNTS_TABLE_NAME)
                self.default_table = self.db.table(DEFAULT_TABLE_NAME)
            else:
                self.db.close()
                raise ValueError("Invalid DB, missing 'accounts' table!")
        elif db_path and create_new:
            logger.info("DB file (%s) is missing, and create_new=%s, hence creating new DB!!" % (db_path, create_new))
            self.db = tinydb.TinyDB(db_path)
            self.accounts_table = self.db.table(ACCOUNTS_TABLE_NAME)
            self.default_table = self.db.table(DEFAULT_TABLE_NAME)
            self.default_table.insert({NEXT_ACCONUT_ID_FIELD_NAME: 1})
        else:
            raise ValueError("Unexpected dbindex file (%s) is missing" % db_path)

        self.db_path = db_path
        self.account_obj_list = {}


    def _close(self):
        self.db.close()

    def _get_next_account_id(self):
        db_metadata = self.default_table.get(doc_id=1)
        return db_metadata[NEXT_ACCONUT_ID_FIELD_NAME]


    def _increment_next_account_id(self):
        db_metadata = self.default_table.get(doc_id=1)
        db_metadata[NEXT_ACCONUT_ID_FIELD_NAME] += 1
        self.default_table.update(db_metadata, doc_ids=[1])
        return db_metadata[NEXT_ACCONUT_ID_FIELD_NAME]

    def get_transaction(self, transaction_id):
        pass

    def add_transaction(self, account_obj, transaction_obj):
        pass

    def del_transaction(self, account_obj, transaction_obj):
        pass

    def modify_transaction(self, account_obj, transaction_obj):
        pass

    def get_account(self, account_id=None, account_name=None):
        if not account_id and not account_name:
            raise DBAccountLookupError("Missing both account id and account name, need at least one need to look up account")
        if account_id and type(account_id) != int:
            raise DBAccountLookupError("Expected type int for account_id, instead got %s" % type(account_id))
        if account_name and type(account_name) != str:
            raise DBAccountLookupError("Expected type str for account_name, instead got %s" % type(account_name))

        # Look up if this account have already been loaded
        if account_id in self.account_obj_list:
            assert self.account_obj_list[account_id]
            return self.account_obj_list[account_id]

        # Nop, now load the account from the database
        account_query = tinydb.Query()
        if account_id and account_name:
            logger.info("Looking up account via account id %d and account name %s" % (account_id, account_name))
            accounts = self.accounts_table.search((account_query.NAME == account_name) & (account_query.id == account_id))
        elif account_id:
            logger.info("Looking up account via account id %d" % (account_id))
            accounts = self.accounts_table.search(account_query.ID == account_id)
        elif account_name:
            logger.info("Looking up account via account name %s" % (account_name))
            accounts = self.accounts_table.search(account_query.NAME == account_name)

        if not accounts:
            raise DBAccountLookupError("Account '%s' does not exist." % account_name)
        elif len(accounts) > 1:
            raise DBAccountLookupError("Multiple accounts with similar account name found.")
        else:
            account_id = accounts[0]['ID']
            if account_id not in self.account_obj_list:
                new_account_obj = account.Account(accounts[0])

                # An account is found, simple sanity check it have correct number of fields
                # TODO: more complicated sanity check can be added to account, and used as part
                # of overall DB checkup.
                if new_account_obj.check_sanity():
                    raise ValueError("Invalid accounts data for account '%s'." % account_name)

                self.account_obj_list[account_id] = new_account_obj
            return self.account_obj_list[account_id]

    def add_account(self, account_obj):
        # Look up if this account have already exist
        try:
            # Using accont name to look up if there is another account with same name
            # Account ID is assumed to be false since this is a newly created account_obj
            self.get_account(account_name=account_obj.NAME)
        except DBAccountLookupError as e:
            # If a DBAccountLookupError is observed that mean the account does not exist
            pass
        else:
            # else throw error that duplicate account is attempted to be created
            raise DBAccountAddError("Attempting add new account with dupicate name '%s'" % account_obj.NAME)

        # Get the next increment of account ID
        # TODO: Test this
        account_obj.ID = self._increment_next_account_id()
        logger.info("Adding new account %s with account id %d." % (account_obj.NAME, account_obj.ID))

        # Insert the account information info into the master accounts table
        self.account_obj_list[account_obj.ID] = account_obj
        self.accounts_table.insert(account_obj.__dict__)

        # Create new accoutns table using the account id
        # TODO: Test this
        new_account_table = self.db.table(ACCOUNT_TABLE_NAME_FORMAT % account_obj.ID)

    def del_account(self, account_obj):
        pass

    def modify_account(self, new_account_obj):
        pass

    def stage_change(self):
        pass

    def commit(self):
        pass

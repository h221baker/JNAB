import account
from util import *
from . import db
from . import db_exceptions

import tinydb

logger = get_logger("db_account_overview")


class DBAccountOverview(object):
    """
    account_tbl: Expect a tinydb table object that represent
                 the general account management table.
    """

    def __init__(self, account_tbl):
        self.account_tbl = account_tbl
        self.account_obj_list = {}

    def get_all_accounts(self):
        # Call get_account() on all accounts to
        # get it loaded into account_obj_list
        for account in self.account_tbl.all():
            logger.debug(repr(account))
            self.get_account(
                account_id=account['ID'], account_name=account['NAME'])
        return self.account_obj_list.values()

    def get_account(self, account_id=None, account_name=None):
        if not account_id and not account_name:
            raise db_exceptions.DBAccountLookupError(
                "Missing both account id and account name,"
                "need at least one need to look up account")
        else:
            if account_id and type(account_id) != int:
                raise db_exceptions.DBAccountLookupError(
                    "Expected type int for account_id, instead got %s" %
                    type(account_id))
            elif account_name and type(account_name) != str:
                raise db_exceptions.DBAccountLookupError(
                    "Expected type str for account_name, instead got %s" %
                    type(account_name))

        # Force account name to always be upper case
        if account_name:
            account_name = account_name.upper()

        # Look up if this account have already been loaded
        if account_id in self.account_obj_list:
            assert self.account_obj_list[account_id]
            return self.account_obj_list[account_id]

        # Nop, now load the account from the database
        account_query = tinydb.Query()
        debug_format_str = "Looking up account via "
        if account_id and account_name:
            debug_format_str += " account id %d and account name %s." % (
                account_id, account_name)
            query_func = (account_query.NAME == account_name) & (
                account_query.ID == account_id)
        elif account_id:
            debug_format_str += " account id %d." % account_id
            query_func = account_query.ID == account_id
        elif account_name:
            debug_format_str += " account name %s." % account_name
            query_func = account_query.NAME == account_name

        logger.debug(debug_format_str)
        accounts = self.account_tbl.search(query_func)

        if not accounts:
            msg = ""
            if account_id:
                msg = "Account ID '%d'" % account_id
            if account_name:
                if not msg:
                    msg += " and "
                msg += "Account NAME '%s' does not exist." % account_name
            raise db_exceptions.DBAccountLookupError(msg)
        elif len(accounts) > 1:
            raise db_exceptions.DBAccountLookupError(
                "Multiple accounts found.")
        else:
            account_id = accounts[0]['ID']
            if account_id not in self.account_obj_list:
                new_account_obj = account.Account(accounts[0])

                # An account is found, simple sanity check it have correct
                # number of fields
                # TODO: more complicated sanity check can be added to account,
                # and used as part of overall DB checkup.
                if not new_account_obj.check_sanity():
                    raise ValueError("Invalid accounts data for account '%s'."
                                     % account_name)

                self.account_obj_list[account_id] = new_account_obj
            return self.account_obj_list[account_id]

    def add_account(self, account_obj):
        # Look up if this account have already exist
        try:
            # Using accont name to look up if there is another account
            # with same name Account ID is assumed to be false since
            # this is a newly created account_obj
            self.get_account(account_name=account_obj.NAME)
        except db_exceptions.DBAccountLookupError as e:
            # If a DBAccountLookupError is observed that mean
            # the account does not exist
            pass
        else:
            # else throw error that duplicate account is attempted
            # to be created
            raise db_exceptions.DBAccountAddError(
                "Attempting add new account with dupicate name '%s'" %
                account_obj.NAME)

        # Get the next increment of account ID
        # TODO: Test this
        account_obj.ID = self.account_tbl._get_next_id()
        logger.info("Adding new account %s with account id %d." %
                    (account_obj.NAME, account_obj.ID))

        # Insert the account information info into the master accounts table
        self.account_obj_list[account_obj.ID] = account_obj
        self.account_tbl.insert(account_obj._dict())

        return account_obj

    def del_account(self, account_id=None, account_name=None):
        account_query = tinydb.Query()
        if account_id and account_name:
            del_account_obj = self.get_account(
                account_id=account_id, account_name=account_name)
            del_account_obj.ACTIVE = False
            self.account_tbl.update(
                del_account_obj._dict(),
                ((account_query.ID == del_account_obj.ID) &
                 (account_query.NAME == del_account_obj.NAME)))
        elif account_id:
            del_account_obj = self.get_account(account_id=account_id)
            del_account_obj.ACTIVE = False
            self.account_tbl.update(del_account_obj._dict(),
                                    account_query.ID == del_account_obj.ID)
        elif account_name:
            del_account_obj = self.get_account(account_name=account_name)
            del_account_obj.ACTIVE = False
            self.account_tbl.update(del_account_obj._dict(),
                                    account_query.NAME == del_account_obj.NAME)

    def modify_account(self, updated_account_obj):
        account_query = tinydb.Query()
        # Expect an account object that was created via get_account() function
        if (updated_account_obj.ID not in self.account_obj_list) or \
                (updated_account_obj !=
                    self.account_obj_list[updated_account_obj.ID]):
            raise db_exceptions.DBLookupError(
                "Invalid updated_account_obj %s" % updated_account_obj)

        self.account_tbl.update(
            updated_account_obj._dict(),
            ((account_query.NAME == updated_account_obj.NAME) &
             (account_query.ID == updated_account_obj.ID)))

import os
import sys
import tempfile
import shutil

import unittest
import logging

from unittest.mock import MagicMock

from jnab import db
from jnab import account
from jnab import transaction

TEST_DB_FOLDER = os.path.join(os.path.dirname(__file__), 'test_resource')


class TestDB(unittest.TestCase):

    SIMPLE_ACCOUNT = {
            "ID": 1,
            "NAME": "Chase Reserve",
            "TYPE": 1,
            "CURRENCY": 1,
            "RATE_TO": 1,
            "BALANCE": 100,
            "ACTIVE": False}

    TEST_TRANSACTION_1 = {
            'ID': 1,
            'DATE': "2018-02-20",
            'NAME': "Sample type",
            'TYPE': 2,
            'BUDGET_ID': None,
            'AMOUNT': 123,
            'META': None,
            'CLEAR': True
            }

    def _setupTestDB(self):
        # TEMP HACK
        for db_file in os.listdir(TEST_DB_FOLDER):
            shutil.copyfile(os.path.join(TEST_DB_FOLDER, db_file),
                            os.path.join(self.temp_dir, db_file))

        # The following the the right solution
        # simpledb = open(os.path.join(self.temp_dir, "simple.json"), mode='w')
        # simpledb.write(self.SIMPLE_DB)
        # simpledb.close()

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self._setupTestDB()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
        if hasattr(self, "database") and self.database:
            self.database._close()

    def test_get_instance_none(self):
        database = db.DB.get_instance()
        self.assertIsNone(database)

    def test_get_instance_not_none(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)
        instance_database = db.DB.get_instance()
        self.assertIsNotNone(instance_database)
        self.assertEqual(self.database, instance_database)

    def test_get_instance_reinit(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)
        with self.assertRaises(RuntimeError):
            db.DB(db_file, create_new=False)

    def test_db_init_sanity(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)

    def test_db_init_no_accounts_table(self):
        db_file = os.path.join(self.temp_dir, "bad_db.json")
        with self.assertRaises(ValueError):
            self.database = db.DB(db_file, create_new=False)

    def test_db_init_not_create_new(self):
        db_file = os.path.join(self.temp_dir, "not_exist.json")
        with self.assertRaises(ValueError):
            self.database = db.DB(db_file, create_new=False)

    def test_db_init_create_new(self):
        db_file = os.path.join(self.temp_dir, "new_db.json")
        self.database = db.DB(db_file, create_new=True)

    def test_db_init_empty_file(self):
        with self.assertRaises(ValueError):
            self.database = db.DB(None, create_new=True)

        with self.assertRaises(ValueError):
            self.database = db.DB("", create_new=True)

    def test_db_get_accounts_sanity(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account(account_name=123)

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account(account_name=1.222)

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account(account_id=1.222)

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account(account_id="123")

    def test_db_get_accounts_bad_input(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)
        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account()

    def test_db_get_accounts_not_exist_name(self):
        db_file = os.path.join(self.temp_dir, "simple.json")

        self.database = db.DB(db_file, create_new=False)
        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account(
                    account_name='Chase NOT Real')

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account(account_id=99)

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account(
                    account_id=99,
                    account_name='Chase NOT Real')

    def test_db_get_account_multiple_accounts(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)
        self.database.accounts_table.search = MagicMock(return_value=[
            {"ID": 1,
                "NAME": "Chase Reserve",
                "TYPE": 1,
                "CURRENCY": 1,
                "RATE_TO": 1,
                "BALANCE": 100},
            {"ID": 2,
                "NAME": "Chase Reserve",
                "TYPE": 1,
                "CURRENCY": 1,
                "RATE_TO": 1,
                "BALANCE": 100}])

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = self.database.get_account(
                    account_name='Chase Reserve')
            self.assertNone(account_obj)
        self.database.accounts_table.search.assert_called_once()

    def test_db_get_account_already_loaded_account_obj(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)
        exsting_account = account.Account(self.SIMPLE_ACCOUNT)

        self.database.account_obj_list[exsting_account.ID] = exsting_account

        account_obj = self.database.get_account(account_id=1)
        self.assertEqual(account_obj, exsting_account)

        account_obj = self.database.get_account(account_name='Chase Reserve')
        self.assertEqual(account_obj, exsting_account)

    def test_db_get_account_invalid_account(self):
        db_file = os.path.join(self.temp_dir, "invalid_account.json")
        self.database = db.DB(db_file, create_new=False)
        with self.assertRaises(ValueError):
            account_obj = self.database.get_account(account_id=1)

    def test_db_add_account_sanity(self):
        simple_account = {
                "NAME": "Chase Reserve",
                "TYPE": 1,
                "CURRENCY": 1,
                "RATE_TO": 1,
                "BALANCE": 100,
                "ACTIVE": False}
        db_file = os.path.join(self.temp_dir, "new_account.json")
        self.database = db.DB(db_file, create_new=True)

        account_obj = account.Account(simple_account)
        self.database.add_account(account_obj)
        self.database._close()

        self.database = db.DB(db_file, create_new=False)
        account_obj_from_db = self.database.get_account(
                account_name=account_obj.NAME)
        self.database._close()

        self.assertIsNotNone(account_obj_from_db)
        self.assertNotEqual(account_obj_from_db, account_obj)
        self.assertEqual(account_obj_from_db.NAME, account_obj.NAME)

    def test_db_add_account_duplicate(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)

        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        with self.assertRaises(db.DBAccountAddError):
            self.database.add_account(account_obj)

    def test_db_del_account_sanity(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)

        self.database.del_account(account_id=1, account_name="Chase Reserve")

        account_obj = self.database.get_account(
                account_id=1, account_name="Chase Reserve")
        self.assertFalse(account_obj.ACTIVE)

    def test_db_del_account_id(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)

        self.database.del_account(account_id=1)

        account_obj = self.database.get_account(
                account_id=1, account_name="Chase Reserve")
        self.assertFalse(account_obj.ACTIVE)

    def test_db_del_account_name(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)

        self.database.del_account(account_name="Chase Reserve")

        account_obj = self.database.get_account(
                account_id=1, account_name="Chase Reserve")
        self.assertFalse(account_obj.ACTIVE)

    def test_db_modify_account_sanity(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)

        account_obj = self.database.get_account(
                account_id=1, account_name="Chase Reserve")
        account_obj.BALANCE = 9999
        self.database.modify_account(account_obj)
        self.database._close()

        self.database = db.DB(db_file, create_new=False)
        account_obj = self.database.get_account(
                account_id=1, account_name="Chase Reserve")
        self.assertEqual(account_obj.BALANCE, 9999)

    def test_db_modify_account_error(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        self.database = db.DB(db_file, create_new=False)

        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        with self.assertRaises(db.DBLookupError):
            self.database.modify_account(account_obj)

    def test_db_get_all_accounts_sanity(self):
        db_file = os.path.join(self.temp_dir, "sample_complete_accounts.json")
        self.database = db.DB(db_file, create_new=False)
        account_list = self.database.get_all_accounts()
        self.assertEqual(len(account_list), 4)

    def test_db_get_recent_transactions_sanity(self):
        db_file = os.path.join(self.temp_dir, "sample_complete_accounts.json")
        self.database = db.DB(db_file, create_new=False)
        account_obj = self.database.get_account(account_id=1)
        recent_trans = self.database.get_recent_transactions(account_obj)

    def test_db_get_transaction_sanity(self):
        pass

    def test_db_add_transaction_sanity(self):
        db_file = os.path.join(self.temp_dir, "sample_complete_accounts.json")
        self.database = db.DB(db_file, create_new=False)
        account_obj = self.database.get_account(account_id=1)
        transaction_obj_1 = transaction.Transaction(self.TEST_TRANSACTION_1)
        self.database.add_transaction(account_obj, transaction_obj_1)


if __name__ == '__main__':
    unittest.main()

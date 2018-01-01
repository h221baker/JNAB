import os
import sys
import tempfile
import shutil

import unittest
import logging

from unittest.mock import MagicMock

from jnab import db
from jnab import account

TEST_DB_FOLDER = os.path.join(os.path.dirname(__file__), 'test_resource')


class TestDB(unittest.TestCase):

    SIMPLE_ACCOUNT={"ID": 1, "NAME": "Chase Reserve", "TYPE": 1, "CURRENCY": 1, "RATE_TO": 1, "BALANCE": 100, "ACTIVE": False}

    def _setupSimpleDB(self):
        # TEMP HACK
        shutil.copyfile(os.path.join(TEST_DB_FOLDER, "simple.json"),
                os.path.join(self.temp_dir, "simple.json"))

        ## The following the the right solution
        # simpledb = open(os.path.join(self.temp_dir, "simple.json"), mode='w')
        # simpledb.write(self.SIMPLE_DB)
        # simpledb.close()

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_db_init_sanity(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = db.DB(db_file, create_new=False);
        database._close();

    def test_db_init_no_accounts_table(self):
        db_file = os.path.join(self.temp_dir, "bad_accounts.json")
        with self.assertRaises(ValueError):
            database = db.DB(db_file, create_new=False);

    def test_db_init_not_create_new(self):
        db_file = os.path.join(self.temp_dir, "not_exist.json")
        with self.assertRaises(ValueError):
            database = db.DB(db_file, create_new=False);

    def test_db_init_create_new(self):
        db_file = os.path.join(self.temp_dir, "new_db.json")
        database = db.DB(db_file, create_new=True);
        database._close()

    def test_db_init_empty_file(self):
        with self.assertRaises(ValueError):
            database = db.DB(None, create_new=True);
            database._close()

        with self.assertRaises(ValueError):
            database = db.DB("", create_new=True);
            database._close()

    def test_db_get_accounts_sanity(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = db.DB(db_file, create_new=False);

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = database.get_account(account_name=123)

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = database.get_account(account_name=1.222)

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = database.get_account(account_id=1.222)

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = database.get_account(account_id="123")

        database._close();

    def test_db_get_accounts_bad_input(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = db.DB(db_file, create_new=False);
        account_obj = database.get_account(account_name='Chase Reserve')
        database._close();


    def test_db_get_accounts_not_exist(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")

        database = db.DB(db_file, create_new=False);
        with self.assertRaises(db.DBAccountLookupError):
            account_obj = database.get_account(account_name='Chase NOT Real')
            self.assertNone(account_obj)
        database._close();

    def test_db_get_account_multiple_accounts(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")

        database = db.DB(db_file, create_new=False);
        database.accounts_table.search = MagicMock(return_value=[{"ID": 1, "NAME": "Chase Reserve", "TYPE": 1, "CURRENCY": 1, "RATE_TO": 1, "BALANCE": 100},
            {"ID": 2, "NAME": "Chase Reserve", "TYPE": 1, "CURRENCY": 1, "RATE_TO": 1, "BALANCE": 100}])

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = database.get_account(account_name='Chase Reserve')
            self.assertNone(account_obj)
        database.accounts_table.search.assert_called_once()
        database._close();

    def test_db_get_account_already_loaded_account_obj(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = db.DB(db_file, create_new=False);
        exsting_account = account.Account(self.SIMPLE_ACCOUNT)

        database.account_obj_list[exsting_account.ID] = exsting_account

        account_obj = database.get_account(account_id=1)
        self.assertEqual(account_obj, exsting_account)

        account_obj = database.get_account(account_name='Chase Reserve')
        self.assertEqual(account_obj, exsting_account)
        database._close();

    def test_db_add_account_sanity(self):
        simple_account={"NAME": "Chase Reserve", "TYPE": 1, "CURRENCY": 1, "RATE_TO": 1, "BALANCE": 100, "ACTIVE": False}
        db_file = os.path.join(self.temp_dir, "new_account.json")
        database = db.DB(db_file, create_new=True);

        account_obj = account.Account(simple_account)
        database.add_account(account_obj)
        database._close()

        database = db.DB(db_file, create_new=False);
        account_obj_from_db = database.get_account(account_name=account_obj.NAME)
        database._close()

        self.assertIsNotNone(account_obj_from_db)
        self.assertNotEqual(account_obj_from_db, account_obj)
        self.assertEqual(account_obj_from_db.NAME, account_obj.NAME)

    def test_db_add_account_duplicate(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = db.DB(db_file, create_new=False);

        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        with self.assertRaises(db.DBAccountAddError):
            database.add_account(account_obj)

        database._close()

    def test_db_del_account_sanity(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = db.DB(db_file, create_new=False);

        #TODO: test different type of input here
        database.del_account(account_id=1, account_name="Chase Reserve")

        account_obj = database.get_account(account_id=1, account_name="Chase Reserve")
        self.assertFalse(account_obj.ACTIVE)

        database._close()

    def test_db_modify_account_sanity(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = db.DB(db_file, create_new=False);

        account_obj = database.get_account(account_id=1, account_name="Chase Reserve")
        account_obj.BALANCE = 9999
        database.modify_account(account_obj)
        database._close()

        database = db.DB(db_file, create_new=False);
        account_obj = database.get_account(account_id=1, account_name="Chase Reserve")
        self.assertEqual(account_obj.BALANCE, 9999)

        database._close()

    def test_db_modify_account_error(self):
        self._setupSimpleDB()
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = db.DB(db_file, create_new=False);

        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        with self.assertRaises(db.DBLookupError):
            database.modify_account(account_obj)
        database._close()


if __name__ == '__main__':
    unittest.main()

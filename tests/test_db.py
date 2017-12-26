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

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_db_init_sanity(self):
        db_file = os.path.join(TEST_DB_FOLDER, "simple.json")
        database = db.DB(db_file, create_new=False);
        database._close();

    def test_db_init_not_create_new(self):
        db_file = os.path.join(self.temp_dir, "not_exist.json")
        with self.assertRaises(ValueError):
            database = db.DB(db_file, create_new=False);
            database._close()

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
        db_file = os.path.join(TEST_DB_FOLDER, "simple.json")
        database = db.DB(db_file, create_new=False);
        account_obj = database.get_account('Chase Reserve')
        assert account_obj
        database._close();

    def test_db_get_accounts_not_exist(self):
        db_file = os.path.join(TEST_DB_FOLDER, "simple.json")
        database = db.DB(db_file, create_new=False);
        with self.assertRaises(db.DBAccountLookupError):
            account_obj = database.get_account('Chase NOT Real')
            assert not account_obj
        database._close();

    def test_db_get_account_multiple_accounts(self):
        db_file = os.path.join(TEST_DB_FOLDER, "simple.json")
        database = db.DB(db_file, create_new=False);
        database.accounts_table.search = MagicMock(return_value=[{"ID": 1, "NAME": "Chase Reserve", "TYPE": 1, "CURRENCY": 1, "RATE_TO": 1, "BALANCE": 100},
            {"ID": 2, "NAME": "Chase Reserve", "TYPE": 1, "CURRENCY": 1, "RATE_TO": 1, "BALANCE": 100}])

        with self.assertRaises(db.DBAccountLookupError):
            account_obj = database.get_account('Chase Reserve')
            assert not account_obj
        database.accounts_table.search.assert_called_once()
        database._close();

    def test_db_get_account_already_loaded_account_obj(self):
        db_file = os.path.join(TEST_DB_FOLDER, "simple.json")
        database = db.DB(db_file, create_new=False);
        fakeAccount = 0x12345678

        database.account_obj_list['Chase Reserve'] = fakeAccount
        account_obj = database.get_account('Chase Reserve')
        assert account_obj == fakeAccount
        database._close();

    def test_db_add_account_sanity(self):
        db_file = os.path.join(self.temp_dir, "new_account.json")
        database = db.DB(db_file, create_new=True);

        account_obj = account.Account({})
        account_obj.NAME = 'Chase Reserve'
        database.add_account(account_obj)

        assert False

    def test_db_add_account_duplicate(self):
        db_file = os.path.join(TEST_DB_FOLDER, "simple.json")
        database = db.DB(db_file, create_new=False);

        account_obj = account.Account({})
        account_obj.NAME = 'Chase Reserve'
        with self.assertRaises(db.DBAccountAddError):
            database.add_account(account_obj)


if __name__ == '__main__':
    unittest.main()

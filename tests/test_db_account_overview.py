import os
import sys
import tempfile
import shutil
import tinydb

import unittest
from unittest.mock import MagicMock

from jnab.database import db
from jnab.database import db_account_overview

TEST_DB_FOLDER = os.path.join(os.path.dirname(__file__), 'test_resource')


class TestDBAccountOverview(unittest.TestCase):
    def _setupTestDB(self):
        # TEMP HACK
        for db_file in os.listdir(TEST_DB_FOLDER):
            shutil.copyfile(
                os.path.join(TEST_DB_FOLDER, db_file),
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

    def test_db_account_overview_init_sanity(self):
        db_file = os.path.join(self.temp_dir, "simple.json")
        database = tinydb.TinyDB(db_file)
        account_tbl = database.table(db.ACCOUNTS_TABLE_NAME)

        db_account_overview.DBAccountOverview(account_tbl)

    def test_db_account_overview_get_all_accounts_sanity(self):
        db_file = os.path.join(self.temp_dir, "sample_complete_accounts.json")
        database = tinydb.TinyDB(db_file)
        account_tbl = database.table(db.ACCOUNTS_TABLE_NAME)

        dbao = db_account_overview.DBAccountOverview(account_tbl)
        account_list = dbao.get_all_accounts()
        self.assertEqual(len(account_list), 4)

    def test_db_get_account_sanity(self):
        account_tbl = MagicMock()
        dbao = db_account_overview.DBAccountOverview(account_tbl)


if __name__ == '__main__':
    unittest.main()

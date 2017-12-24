import os
import sys

import unittest
import logging

from jnab import db

TEST_DB_FOLDER = os.path.join(os.path.dirname(__file__), 'test_resource')


class TestDB(unittest.TestCase):

    def test_db_init_sanity(self):
        db_file = os.path.join(TEST_DB_FOLDER, "simple.json")
        database = db.DB(db_file, create_new=False);
        database._close();

    def test_db_init_not_create_new(self):
        db_file = os.path.join(TEST_DB_FOLDER, "not_exist.json")
        with self.assertRaises(ValueError):
            database = db.DB(db_file, create_new=False);
            database._close()

    def test_db_init_create_new(self):
        db_file = os.path.join(TEST_DB_FOLDER, "new_db.json")
        database = db.DB(db_file, create_new=True);
        database._close()

    def test_db_init_empty_file(self):
        with self.assertRaises(ValueError):
            database = db.DB(None, create_new=True);
            database._close()

        with self.assertRaises(ValueError):
            database = db.DB("", create_new=True);
            database._close()


if __name__ == '__main__':
    unittest.main()

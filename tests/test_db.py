import os
import sys

import unittest
import logging

from jnab import db

TEST_DB_FOLDER = os.path.join(os.path.dirname(__file__), 'test_resource')


class TestDB(unittest.TestCase):

    def test_db_create_sanity(self):
        db_file = os.path.join(TEST_DB_FOLDER, "simple.json")
        database = db.DB(db_file, create_new=True);

if __name__ == '__main__':
    unittest.main()

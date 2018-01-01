import os
import sys
import tempfile
import shutil

import unittest
import logging

from unittest.mock import MagicMock

from jnab import transaction


class TestTransaction(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_transaction_set_attr_sanity(self):
        trans_obj = transaction.Transaction()
        trans_obj.ID = 123
        trans_obj.NAME = "ice cream"
        self.assertEqual(trans_obj.ID, 123)
        self.assertEqual(trans_obj.NAME, "ice cream")

    def test_transaction_set_attr_error(self):
        trans_obj = transaction.Transaction()
        with self.assertRaises(transaction.TransactionInvalidAttributeError):
            trans_obj.BAD_FIELD = 123

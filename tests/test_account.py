import unittest

from jnab import account

class TestAccount(unittest.TestCase):

    SIMPLE_ACCOUNT={"ID": 1, "NAME": "Chase Reserve", "TYPE": 1, "CURRENCY": 1, "RATE_TO": 1, "BALANCE": 100, "ACTIVE": False}

    def test_account_init_sanity(self):
        account_obj = account.Account(self.SIMPLE_ACCOUNT)

    def test_account_set_attr_sanity(self):
        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        account_obj.RATE_TO = 123

        self.assertEqual(account_obj.RATE_TO, 123)

    def test_account_set_attr_error(self):
        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        with self.assertRaises(account.AccountInvalidAttributeError):
            account_obj.ID = 123

        with self.assertRaises(account.AccountInvalidAttributeError):
            account_obj.NAME = 123


if __name__ == '__main__':
    unittest.main()


import unittest

from jnab import account


class TestAccount(unittest.TestCase):

    SIMPLE_ACCOUNT = {
        "ID": 1,
        "NAME": "Chase Reserve",
        "TYPE": 1,
        "CURRENCY": 1,
        "RATE_TO": 1,
        "BALANCE": 100,
        "ACTIVE": False
    }

    def test_account_init_sanity(self):
        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        self.assertIsNotNone(account_obj)

        account_str = repr(account_obj)
        self.assertIsNotNone(account_str)

    def test_account_set_attr_sanity(self):
        account_obj = account.Account(self.SIMPLE_ACCOUNT)

        account_obj.RATE_TO = 123
        self.assertEqual(account_obj.RATE_TO, 123)

    def test_account_set_currency(self):
        account_obj = account.Account("")
        account_obj.CURRENCY = "USD"
        self.assertEqual(account_obj.CURRENCY, account.Currency.USD)

        account_obj2 = account.Account("")
        account_obj2.CURRENCY = 2
        self.assertEqual(account_obj2.CURRENCY, account.Currency.EURO)

    def test_account_set_currency_invalid_type(self):
        account_obj = account.Account("")
        with self.assertRaises(ValueError):
            account_obj.CURRENCY = []
        self.assertFalse(hasattr(account_obj, "CURRENCY"))

    def test_account_set_type(self):
        account_obj = account.Account("")
        account_obj.TYPE = "CHECKING"
        self.assertEqual(account_obj.TYPE, account.Type.CHECKING)

        account_obj2 = account.Account("")
        account_obj2.TYPE = 2
        self.assertEqual(account_obj2.TYPE, account.Type.CREDIT)

    def test_account_set_type_invalid_type(self):
        account_obj = account.Account("")
        with self.assertRaises(ValueError):
            account_obj.TYPE = {}
        self.assertFalse(hasattr(account_obj, "TYPE"))

    def test_account_set_attr_error(self):
        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        with self.assertRaises(account.AccountInvalidAttributeError):
            account_obj.ID = 123

        with self.assertRaises(account.AccountInvalidAttributeError):
            account_obj.NAME = 123

    def test_account_set_attr_extra_attr(self):
        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        with self.assertRaises(account.AccountInvalidAttributeError):
            account_obj.RANDOM = 123

        with self.assertRaises(account.AccountInvalidAttributeError):
            account_obj.SOSO = 123

    def test_account_check_sanity_sanity(self):
        account_obj = account.Account(self.SIMPLE_ACCOUNT)
        self.assertTrue(account_obj.check_sanity())

    def test_account_check_sanity_error(self):
        account_obj = account.Account("")
        self.assertFalse(account_obj.check_sanity())


if __name__ == '__main__':
    unittest.main()

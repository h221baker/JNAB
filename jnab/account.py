class AccountError(Exception):
    pass

class AccountInvalidAttributeError(AccountError):
    pass

class Account(object):

    account_db_attributes = ['ID', 'NAME', 'TYPE', 'CURRENCY', 'RATE_TO', 'BALANCE', 'ACTIVE']

    def __init__(self, account_dict):
        for key in account_dict:
            if key in self.account_db_attributes:
                self.__setattr__(key, account_dict[key])

    def __setattr__(self, name, value):
        if name not in self.account_db_attributes:
            raise AccountInvalidAttributeError("Invalid Account object attribute %s" % name)
        # Do not allow permenent account attribute to be changed
        if name in ['ID', 'NAME', 'CURRENTY', 'TYPE'] and hasattr(self, name):
            raise AccountInvalidAttributeError("Unable to change existing permenent account attribute %s" % name)
        super.__setattr__(self, name, value)

    def _dict(self):
        account_dict = {}
        for attr in self.account_db_attributes:
            account_dict[attr] = self.__getattribute__(attr)
        return account_dict

    def __repr__(self):
        return repr(self._dict())

    def check_sanity(self):
        for attr in self.account_db_attributes:
            if not hasattr(self, attr):
                return False
        # TODO: more in depth check of each field with type and content
        ## Configure:
        ### account name
        ### currency
        ### account type
        ### conversion rate
        ### transaction lookup table

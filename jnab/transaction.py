class TransactionError(Exception):
    pass

class TransactionInvalidAttributeError(TransactionError):
    pass

class Transaction(object):
    transaction_db_attributes = ['ID', 'DATE', 'NAME', 'ACCOUNT_ID', 'BUDGET_ID', 'AMOUNT', 'CLEAR']

    def __init__(self, transaction_dict=None):
        if transaction_dict:
            for attr in self.account_db_attributes:
                self.__setattr__(attr, transaction_dict[attr])

    def __setattr__(self, name, value):
        if name not in self.transaction_db_attributes:
            raise TransactionInvalidAttributeError("Invalid Transaction object attribute %s" % name)
        super.__setattr__(self, name, value)

    def check_sanity(self):
        for attr in self.transaction_db_attributes:
            if not hasattr(self, attr):
                return False
        # TODO: more in depth check of each attribute with type and content

    def _dict(self):
        account_dict = {}
        for attr in self.account_db_attributes:
            account_dict[attr] = self.__getattribute__(attr)
        return account_dict

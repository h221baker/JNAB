class Account(object):

    account_db_fields = ['ID', 'NAME', 'TYPE', 'CURRENCY', 'RATE_TO', 'BALANCE', 'ACTIVE']

    def __init__(self, account_dict):
        for field in self.account_db_fields:
            self.__setattr__(field, account_dict[field])

    # TODO: to make some fields inmutable
    # def __setattr__(self):

    def _dict(self):
        account_dict = {}
        for field in self.account_db_fields:
            account_dict[field] = self.__getattribute__(field)
        return account_dict

    def check_sanity(self):
        pass
        # Verify account db file exist
        ## Configure:
        ### account name
        ### currency
        ### account type
        ### conversion rate
        ### transaction lookup table

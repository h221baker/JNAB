class DBLookupError(Exception):
    pass


class DBAccountLookupError(DBLookupError):
    pass


class DBTransactionLookupError(DBLookupError):
    pass


class DBAddError(Exception):
    pass


class DBAccountAddError(DBAddError):
    pass


class DBDelError(Exception):
    pass


class DBAccountDelError(DBDelError):
    pass


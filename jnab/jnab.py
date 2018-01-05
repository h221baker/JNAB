import cmd
import db

class JnabShell(cmd.Cmd):

    def preloop(self):
        self.database = db.DB(db.DEFAULT_DB_FILENAME, create_new=True)
        self.curr_account = None

    """
    List all active accounts and their ID
    """
    def do_ls(self, line):
        account_list = self.database.get_all_accounts()
        for account in account_list:
            if account.ACTIVE:
                print("%d - %s" % (account.ID, account.NAME))

    """
    Select an account to work on
    """
    def do_sel(self, line):
        # This should always be true from cmd module
        assert type(line) is str

        name = None
        id = None

        if line.isdigit():
            id = int(line)
        elif line.isprintable():
            name = line

        account = None
        try:
            account = self.database.get_account(account_id=id, account_name=name)
        except db.DBAccountLookupError as e:
            # Determine if using account NAME or ID for selection
            print("Invalid account info, unable to find account %s" % line)

        if account:
            print("%d - %s" % (account.ID, account.NAME))

    def do_EOF(self, line):
        self.database._close()
        return True

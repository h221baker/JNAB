from shell import shell
from database import db

jnabDB = db.DB(db.DEFAULT_DB_FILENAME, create_new=False)
shell.JnabShell(jnabDB).cmdloop()

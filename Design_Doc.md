# Main program
- Check if database exist on disk
- Instantiate class DB
- Instantiate different accounts, check for consistency across accounts
- Instantiate interactive console and print available accounts
- Print DB status

# Data base
- Database will be backed by python TinyDB module, data is stored as json format where TinyDB will emulate searchable database.

## TABLES:
### ACCOUNTS:
- ID
- NAME
- TYPE
- CURRENCY
- RATE_TO
- BALANCE

### JNAB_ACCOUNT_${ACCOUNT_ID}:
- ID
- NAME
- BUDGET_ID
- TYPE
	If Type == Transfer:
	- TRANSFER_ACCOUNT_ID
	- TRANSFER_ACCOUNT_TRANSACTION_ID
	Else:
		DO NOTHING
### BUDGETS:
- ID
- NAME
- AMOUNT
- DURATION
- 


## Design goal

	- Storage format in ascii format to allow manual examination
	- Version control, and rollback or action undo (IIF Intuit Interchange Format)
	- Provide random access to application level
	- Lazy read, Write back on exit or explicit save
	- Maintain data consistency

## Implementation
	Database is backed by python TinyDB module, https://pypi.python.org/pypi/tinydb/

	Main components:
	- Class Account: Keep track of financial transactions
	- Class AccountLoader: create the account objects upon loading
	- Class Budget: Maintain budget across all accounts
	- Class BudgetLoader: create the budget account across all accounts

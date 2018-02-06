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
- ID		// Integer
- NAME		// String
- TYPE		// Enum
- CURRENCY	// Enum
- RATE_TO	// Float
- BALANCE	// Float

### JNAB_ACCOUNT_${ACCOUNT_ID}:
- ID				// Integer
- DATE				// String in parseable format
- NAME				// String
- BUDGET_ID			// Integer
- TYPE				// Enumerate
	If Type == Transfer:
	- META.TRANSFER_ACCOUNT_ID				// Integer
	- META.TRANSFER_ACCOUNT_TRANSACTION_ID	// Integer
	Else:
		DO NOTHING
- AMOUNT			// Integer
- CLEAR				// Boolean flag

### BUDGETS:
- ID				// Integer
- NAME				// String
- AMOUNT			// Float
- DURATION			// Enumerate

Types of budget:
- Transportation
- Lodging
- Food
- Misc
- Reoccurring

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

	Shell interface
	- List existing accounts

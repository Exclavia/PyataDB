# PynexDB: A Lightweight Python Database 

PynexDB is a **lightweight**, **easy-to-use** database built entirely in Python. It's designed for small to medium-sized projects where a full-fledged database system like PostgreSQL or MySQL might be overkill. PynexDB allows you to store and retrieve data easily with only a few lines of code. (See [Usage](#usage))

PynexDB only uses standard Python libraries, making it fairly simple at its core, this also makes it easily modifiable. It's essentially a dictionary extension/wrapper using standard container types with added interfacing methods and easier file saving/loading.

Best use case would be embedded in projects for an extended data storage. It has not been tested in heavily accessed environments with frequently changing data. Nor has it been tested in a production environment. Just a little project/tool originally made for personal usage.


## Installation

```
pip install https://github.com/Exclavia/PynexDB/releases/download/Alpha/pynexdb-0.1.4-py3-none-any.whl
```


## Usage

#### See the [Quickstart](docs/quick-start.md) - Full [quickstart_example.py](bin/quickstart_example.py)

The module is fairly small, making it easy to extend yourself if you wish. This snippet should get you started:

```python
from PynexDB import Pynex

## RECOMMENDED ##
# Declare Database & Table objects for
# easier type declaration and to enable type hints
# (IE: new_table: Table = ...)
Database, Table = Pynex.PyDb, Pynex.PyTb

# Initialize new database
db: Database = Pynex.PyDb()

# Create and return a new table in database
new_table: Table = db.table('new_table')

# Insert key value pairs into table example:
new_table.insert(user_id=1, name='John', email='john@example.com')

# Return list of tables within database
tables_list = db.tables

# Return entry from table based on key value
find_from_id = new_table.find(user_id=1)
find_from_name = new_table.find(name='John')

# Returns all rows in the table as a list of dicts
get_all = new_table.get_all()

# Save database to file
db.save('path/to/database.db')

# Load database from file
db.load('path/to/database.db')
```


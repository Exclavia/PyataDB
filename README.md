# PynexDB: A Lightweight Python Database 

PynexDB is a **lightweight**, **easy-to-use**, and **efficient** database built entirely in Python. It's designed for small to medium-sized projects where a full-fledged database system like PostgreSQL or MySQL might be overkill. PynexDB allows you to store and retrieve data easily with only a few lines of code.



## Features

* **No external dependencies:** PynexDB is built with standard Python libraries, so you don't need to install anything extra.
* **Makes use of Python's Pickle module:** Stores data into a serialized binary formatted file. This makes it easy to store and load, as well as making it easy to pull stored data just using standard Python library.
* **Efficient for small datasets:** It's optimized for performance on smaller data sets. It's essentially just an overglorified/extended dictionary type.


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


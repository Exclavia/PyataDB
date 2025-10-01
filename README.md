# PynexDB 🚀

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![GitHub License](https://img.shields.io/github/license/Exclavia/PynexDB)

PynexDB is a **lightweight**, **in-memory**, and **easy-to-use** database built with pure Python. It's designed for simplicity, speed, and ease of use in small to medium-sized projects, offering powerful features like indexing, transactions, and advanced querying without the need for external dependencies.

---

##  Features

* **In-Memory Speed**: All data is held in memory for blazing-fast read and write operations.
* **Indexing**: Create indexes on columns for near-instantaneous lookups on large datasets.
* **ACID-like Transactions**: An atomic transaction context manager ensures data integrity. If an operation fails, the entire transaction is rolled back.
* **Advanced Queries**: Go beyond simple equality with operators for "greater than" (`__gt`), "less than" (`__lt`), "not equal" (`__ne`), and more.
* **Schema Enforcement**: Optionally enforce data types on a per-column basis for robust data integrity.
* **Data Persistence**: Save your entire database to a file and load it back into memory with a single command.

---

## 💾 Installation

```
pip install ...
```

```python
import Pynex
```

*(A pip package is planned for the future).*

---

## Quickstart


```python
import Pynex

# Recommended for type hints, but not required.
Database, Table, Transaction = Pynex.Database, Pynex.Table, Pynex.Transaction


# 1. Create a database and a table
db:Database = Pynex.Database()
users:Table = db.table('users')

# 2. Insert some data
users.insert(id=1, name='Alice', age=30, city='New York')
users.insert(id=2, name='Bob', age=25, city='Los Angeles')
users.insert(id=3, name='Charlie', age=35, city='New York')

print(f"Total users: {len(users)}")
# Output: Total users: 3

# 3. Find data
# Find all users in New York
ny_users = users.find(city='New York')
print(f"NY Users: {[user['name'] for user in ny_users]}")
# Output: NY Users: ['Alice', 'Charlie']

# Use advanced queries to find users older than 28
older_users = users.find(age__gt=28)
print(f"Older Users: {[user['name'] for user in older_users]}")
# Output: Older Users: ['Alice', 'Charlie']

# 4. Create an index for faster lookups
users.create_index('city')
# Queries using the 'city' column will now be much faster.

# 5. Update and Delete data
users.update(query={'name': 'Bob'}, new_values={'age': 26})
users.delete(id=3)

print(f"All users after changes: {users.get_all()}")
# Output: All users after changes: [{'id': 1, 'name': 'Alice', 'age': 30, 'city': 'New York'}, {'id': 2, 'name': 'Bob', 'age': 26, 'city': 'Los Angeles'}]

# 6. Save your database to a file
db.save("my_app.db", verbose=True)
# Output: Database saved to : 'my_app.db'

# 7. Load it back later
new_db = Database.load("my_app.db")
print(new_db['users'])
# Output: Table(name='users', columns=['id', 'name', 'age', 'city'], rows=2)
```

---

## Reference

### `Database` Class

#### `db.table(name, schema=None)`
Creates a new table or returns an existing one.
* `name` (str): The name of the table.
* `schema` (dict, optional): A dictionary mapping column names to types (e.g., `{'id': int, 'price': float}`) to enforce data integrity.

#### `db.save(filename, verbose=False)`
Saves the entire database object to a binary file using pickle.

#### `Database.load(filename, verbose=False)`
A static method to load a database from a file.

#### `db.transaction()`
Returns a context manager for atomic operations. All operations within the `with` block are committed upon successful exit. If an exception occurs, all changes are rolled back.

```python
with db.transaction():
    db['users'].update(...)
    db['users'].insert(...)
    # These are only saved if no errors occur.
```

### `Table` Class

#### `table.insert(**kwargs)`
Inserts a new row. Each keyword argument represents a column and its value.

#### `table.find(**kwargs)`
Finds all rows matching **all** of the given criteria (`AND` logic).
* **Equality**: `table.find(name='Alice')`
* **Advanced Operators**: Append `__` and an operator to the column name.
    * `age__gt`: Greater than
    * `age__lt`: Less than
    * `age__gte`: Greater than or equal to
    * `age__lte`: Less than or equal to
    * `city__ne`: Not equal

#### `table.find_or(*queries)`
Finds all rows matching **any** of the given query dictionaries (`OR` logic).
```python
# Find users who are younger than 30 OR live in New York
table.find_or({'age__lt': 30}, {'city': 'New York'})
```

#### `table.update(query, new_values)`
Finds rows matching the `query` dictionary and updates them with the values from the `new_values` dictionary.

#### `table.delete(**kwargs)`
Finds rows matching the criteria and "soft-deletes" them. The data is hidden from queries but not yet removed from the file.

#### `table.create_index(column)`
Creates a hash index on a column to make equality-based lookups (`find(column='value')`) significantly faster.

#### `table.compact()`
Permanently removes all soft-deleted rows from the table to reclaim space. This is a disk-intensive operation and should be run periodically.

## 📜 License

This project is licensed under the MIT License.

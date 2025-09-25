"""
Main PynexDB module
  Pydb: Database Class
  PyTable: Table Class
"""
from collections import defaultdict as __defdict__
import pickle as __pickle__

__all__ = ['Pydb', 'PyTable']

class PyTable:
    """Database.Table Object class. Takes name as arguement."""
    def __init__(self, name):
        self.name = name
        self._data = __defdict__(list)
        self._rows = 0
    def __str__(self): return f"Table(name='{self.name}', columns={list(self._data.keys())}, rows={self._rows})"
    def __repr__(self): return self.__str__()
    def __len__(self): return self._rows
    def _get_row(self, index):
        """Returns a single row as dict."""
        if index >= self._rows: raise IndexError("Row index out of range.")
        return {key: self._data[key][index] for key in self._data}

    def insert(self, **kwargs):
        """Inserts a new row of data into the table. 
        Example: table.insert(id=1, name='John', age=30)"""
        # Ensure all existing columns are accounted for in the new entry
        for key in self._data.keys(): if key not in kwargs: kwargs[key] = None
        for key, value in kwargs.items():  #  Add new columns if they don't exist
            # Pad new column with None for existing rows
            if key not in self._data: self._data[key] = [None] * self._rows
            self._data[key].append(value)
        self._rows += 1
        return self._rows - 1

    def find(self, **kwargs):
        """Finds rows that match the given criteria. 
        Returns a list of matching rows (as Dict). 
        Example: table.find(name='John', age=30)"""
        if not kwargs: return [self._get_row(i) for i in range(self._rows)]
        results = []
        # Get the first query condition to start the filtering
        field, value = next(iter(kwargs.items()))
        try: indices = [i for i, v in enumerate(self._data[field]) if v == value]
        except KeyError: return []
        # If more than one query condition, filter down the results
        if len(kwargs) > 1:
            for index in indices:
                row = self._get_row(index)
                if all(row.get(k) == v for k, v in kwargs.items()): results.append(row)
        else: results = [self._get_row(i) for i in indices]
        return results

    def get_all(self):
        """Returns all rows in the table as a list of dictionaries."""
        return [self._get_row(i) for i in range(self._rows)]


class Pydb:
	'''Main Database object class.'''
    def __init__(self): self._tables = {}
    def __getitem__(self, key): return self._tables.get(key)
    def __setitem__(self, key, value):
        if not isinstance(value, PyTable): raise TypeError("Value must be a Table instance.")
        if key != value.name: raise ValueError("Table name must match the key.")
        self._tables[key] = value
    def __str__(self): return f"Database(tables={list(self._tables.keys())})"

    def table(self, name):
        """Creates and returns a new table, or returns an existing one."""
        if name not in self._tables: self._tables[name] = PyTable(name)
        return self._tables[name]

    def save(self, filename, verbose=False):
        """Saves database to file -> Bytes"""
        with open(filename, 'wb') as f: __pickle__.dump(self._tables, f)
        if verbose: print(f"Database saved to : '{filename}'\n")

    def load(self, filename, verbose=False):
        """Loads database from file."""
        with open(filename, 'rb') as f: self._tables = __pickle__.load(f)
        if verbose: print(f"Database loaded from : '{filename}'\n")

    @property
    def tables(self): return list(self._tables.keys())

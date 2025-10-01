"""
Main PynexDB module
  Database()
  Table()
  Transaction()
"""
from collections import defaultdict
import pickle
import numpy as np
import copy
from typing import Dict, Any, List, Set, Optional


__all__ = ['Database', 'Table', 'Transaction', 'OPERATORS']

OPERATORS = {
    'gt': lambda a, b: a > b,
    'lt': lambda a, b: a < b,
    'gte': lambda a, b: a >= b,
    'lte': lambda a, b: a <= b,
    'ne': lambda a, b: a != b,
}

class Table:
    def __init__(self, name: str, schema: Optional[Dict[str, type]] = None):
        self.name = name
        self._data: Dict[str, List[Any]] = defaultdict(list)
        self._rows: int = 0
        self._indexes: Dict[str, Dict[Any, Set[int]]] = {}
        self._deleted: Set[int] = set()
        self._schema: Optional[Dict[str, type]] = schema
    
    def __str__(self) -> str:
        schema_info = f", schema_enforced={bool(self._schema)}" if self._schema else ""
        return f"Table(name='{self.name}', columns={list(self._data.keys())}, rows={len(self)}{schema_info})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return self._rows - len(self._deleted)
    
    def _get_row(self, index: int) -> Dict[str, Any]:
        if index >= self._rows or index in self._deleted:
            raise IndexError("Row index out of range or row has been deleted.")
        return {key: self._data[key][index] for key in self._data}
    
    def insert(self, **kwargs) -> int:
        if self._schema:
            for col, expected_type in self._schema.items():
                if col in kwargs and not isinstance(kwargs[col], expected_type):
                    raise TypeError(f"Column '{col}' expected type {expected_type.__name__}, but got {type(kwargs[col]).__name__}.")

            for col in self._schema:
                if col not in kwargs:
                    kwargs[col] = None

        new_row_index = self._rows
        
        all_cols = set(self._data.keys()) | set(kwargs.keys())
        for key in all_cols:
            value = kwargs.get(key)
            if key not in self._data:
                self._data[key] = [None] * self._rows
            self._data[key].append(value)
            
            if key in self._indexes:
                self._indexes[key][value].add(new_row_index)
                
        self._rows += 1
        return new_row_index

    def create_index(self, column: str):
        if column not in self._data:
            raise ValueError(f"Column '{column}' does not exist.")
        if column in self._indexes:
            print(f"Index on '{column}' already exists.")
            return

        index = defaultdict(set)
        for i, value in enumerate(self._data[column]):
            if i not in self._deleted:
                index[value].add(i)
        self._indexes[column] = index
        print(f"Index created for column: '{column}'")

    def find(self, **kwargs) -> List[Dict[str, Any]]:
        if not kwargs:
            return self.get_all()

        equality_kwargs = {k: v for k, v in kwargs.items() if '__' not in k}
        operator_kwargs = {k: v for k, v in kwargs.items() if '__' in k}
        
        indexed_cols = self._indexes.keys() & equality_kwargs.keys()
        
        if not indexed_cols:
            candidate_indices = set(range(self._rows)) - self._deleted
        else:
            best_col = indexed_cols.pop()
            value = equality_kwargs[best_col]
            candidate_indices = self._indexes[best_col].get(value, set())
            for col in indexed_cols:
                value = equality_kwargs[col]
                candidate_indices &= self._indexes[col].get(value, set())

        non_indexed_cols = equality_kwargs.keys() - self._indexes.keys()
        if non_indexed_cols:
            candidate_indices = {
                idx for idx in candidate_indices 
                if all(self._data[col][idx] == equality_kwargs[col] for col in non_indexed_cols)
            }

        if operator_kwargs:
            final_indices = set()
            for index in candidate_indices:
                match = True
                for key, value in operator_kwargs.items():
                    col, op_str = key.split('__')
                    op_func = OPERATORS.get(op_str)
                    if not op_func or col not in self._data or not op_func(self._data[col][index], value):
                        match = False
                        break
                if match:
                    final_indices.add(index)
        else:
            final_indices = candidate_indices

        active_indices = final_indices - self._deleted
        return [self._get_row(i) for i in sorted(list(active_indices))]

    def find_or(self, *queries: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Finds rows that match ANY of the given query dictionaries (OR logic)."""
        if not queries:
            return []

        total_indices = set()
        for query in queries:
            matched_rows = self.find(**query)
            for row in matched_rows:
                 idx = self._data['id'].index(row['id'])
                 total_indices.add(idx)

        active_indices = total_indices - self._deleted
        return [self._get_row(i) for i in sorted(list(active_indices))]


    def update(self, query: Dict[str, Any], new_values: Dict[str, Any]) -> int:
        if not new_values or not isinstance(new_values, dict):
            raise ValueError("new_values must be a non-empty dictionary.")

        rows_to_update = self.find(**query)
        indices_to_update = [self._data['id'].index(r['id']) for r in rows_to_update]

        for index in indices_to_update:
            for col, new_val in new_values.items():
                if self._schema and col in self._schema and not isinstance(new_val, self._schema[col]):
                    raise TypeError(f"Column '{col}' expected type {self._schema[col].__name__}, but got {type(new_val).__name__}.")
                
                if col in self._indexes:
                    old_val = self._data[col][index]
                    self._indexes[col][old_val].discard(index)
                    if not self._indexes[col][old_val]:
                        del self._indexes[col][old_val]
                    self._indexes[col][new_val].add(index)

                self._data[col][index] = new_val
        return len(indices_to_update)

    def delete(self, **kwargs) -> int:
        if not kwargs:
            raise ValueError("Delete requires at least one condition to prevent accidental mass deletion.")
        
        rows_to_delete = self.find(**kwargs)
        indices_to_delete = {self._data['id'].index(r['id']) for r in rows_to_delete}
        self._deleted.update(indices_to_delete)
        return len(indices_to_delete)

    def get_all(self) -> List[Dict[str, Any]]:
        return [self._get_row(i) for i in range(self._rows) if i not in self._deleted]

    def compact(self) -> None:
        """Permanently removes soft-deleted rows and rebuilds the table and its indexes."""
        if not self._deleted:
            print("No rows to compact.")
            return

        print(f"Compacting table... removing {len(self._deleted)} deleted rows.")
        new_data = defaultdict(list)
        new_rows = 0

        index_map = {}
        for i in range(self._rows):
            if i not in self._deleted:
                index_map[i] = new_rows
                new_rows += 1

        for col, values in self._data.items():
            new_data[col] = [values[i] for i in range(self._rows) if i not in self._deleted]
            
        self._data = new_data
        self._rows = new_rows
        self._deleted.clear()
        
        # Rebuild all indexes
        old_indexes = list(self._indexes.keys())
        self._indexes.clear()
        for col in old_indexes:
            self.create_index(col)
        print("Compaction complete.")


class Database:
    def __init__(self):
        self._tables: Dict[str, Table] = {}

    def __getitem__(self, key: str) -> Optional[Table]:
        return self._tables.get(key)

    def __str__(self) -> str:
        return f"Database(tables={list(self._tables.keys())})"

    def table(self, name: str, schema: Optional[Dict[str, type]] = None) -> Table:
        """Creates and returns a new table, or returns an existing one. Can enforce a schema."""
        if name not in self._tables:
            self._tables[name] = Table(name, schema=schema)
        return self._tables[name]

    def transaction(self):
        """Provides a transactional context. Operations are committed on success or rolled back on error."""
        return Transaction(self)
        
    def save(self, filename: str, verbose: bool = False):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        if verbose: print(f"Database saved to : '{filename}'\n")

    @staticmethod
    def load(filename: str, verbose: bool = False) -> 'Database':
        with open(filename, 'rb') as f:
            db = pickle.load(f)
        if verbose: print(f"Database loaded from : '{filename}'\n")
        return db

    @property
    def tables(self) -> List[str]:
        return list(self._tables.keys())


class Transaction:
    def __init__(self, db: Database):
        self._db = db
        self._db_copy = None

    def __enter__(self):
        self._db_copy = copy.deepcopy(self._db._tables)
        self._db._tables = self._db_copy
        return self._db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Transaction failed: {exc_val}. Rolling back.")
        else:
            print("Transaction committed successfully.")


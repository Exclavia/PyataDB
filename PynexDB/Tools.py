import os as __os__
import json as __json__
from dataclasses import dataclass as __dataclass__
from PynexDB import Pynex as __pnx__

__db__, __tb__ = __pnx__.PyDb, __pnx__.PyTb

__all__ = ['ItemCount', 'dbJSON']

@__dataclass__
class ItemCount:
    """ItemCount(PyDb) -> Returns Database table count & Table entry count"""
    database: __db__
    __tables__: int = 0

    def db_stats(self) -> str:
        """db_stats() return:str -> Tables in database: 'Table count' """
        # Set self.__tables__ to 0, then add table count
        self.__tables__ = (self.__tables__ - self.__tables__) + len(self.database.tables)
        return f"\nTables in database: {self.__tables__}\n"

    def table_stats(self, table: __tb__) -> str:
        """table_stats(Table) return:str -> Table: 'Table Name' - Entries: 'Entry count for given table' """
        return f"\nTable: {table.name} - Entries: {len(table.get_all())}\n"

    def __repr__(self) -> str:
        _entries, _keys = [], []
        db__tables__ = self.database.tables
        # Separate out table(s) and table keys
        for tb in db__tables__:
            _tb: __tb__ = self.database[tb]
            tb_dict = { tb: {'entries': len(_tb.get_all())} }
            _keys.append(tb)
            _entries.append(tb_dict)
        _str = self.db_stats() + '\n'
        # Parse entry counts and table.keys -> Format string -> Concat _str
        for entry, key in zip(_entries, _keys): _str = _str + f"Table: '{key}' - Entries: {entry[key]['entries']}\n"
        return _str



class dbJSON:
    """dbJSON.convert('Database file') -> Convert Database file to JSON file"""

    def convert(DB_File:str):
        if __os__.path.exists(DB_File):
            db = __pnx__.PyDb()
            db.load(DB_File)
            filename = __os__.path.basename(DB_File)
            new_file = filename.replace('.db', '.json')
            new_path = DB_File.replace(filename, new_file)
            for x in db.tables:
                tb_list:list = db[x].get_all()
                tb_list.insert(0, db[x].name)
                with open(new_path, 'a') as f:
                    __json__.dump(tb_list, f, indent=2)
            print(f'{filename} converted to json: {new_path}')
        else: print('Either file does not exists, or non-full filepath inputted')


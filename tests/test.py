import __sys__
__sys__.path.append('../')
import PyataDB as Pyata

### Path to database file
_DBFILE = 'databases/example_db.db'

### Set database, table -> Datbase & Table objects for type declaration
Database, Table = Pyata.Pydb, Pyata.PyTable

### Creates new table
def _new_table(_db: Database, tb_name: str) -> Table: return _db.table(tb_name)
### Get Table length/count for easier ID incrementing
def _get_length(_table: Table) -> int: return len(_table)
### Quick number increment
def _incr_id(prev_id: int) -> int: return prev_id + 1
### Temporary quick-add function for new table entries
def _add(_db: Database, _table: Table, next_id: int, _name: str, _email: str, _status: str) -> int:
	_table.insert(user_id=next_id, name=_name, email=_email, status=_status)
	print(f"New entry added to '{_table}'\nSaving to file.")
	_db.save(_DBFILE)
	print("Reloading database...")
	_db.load(_DBFILE, True)
	_id = next_id
	return _id

### Returns found entries based on 'user_id'
def _find_from_id(_table: Table, _id: int) -> Table: return _table.find(user_id=_id)
### Returns found entries based on 'name'
def _find_from_id(_table: Table, _name: str) -> Table: return _table.find(name=_name)

if __name__ == "__main__":
  db: Database = Pyata.Pydb()
  db.load(_DBFILE)
  users: Table = db['users']
  i = _get_length(users)
  next_i = _incr_id(i)
  i = _add(db, users, next_i, _name='Name', _email='mail@example.com', _status='active')
  ### Iterate through and print [Key:Values]
  for x in range(0, i):
  	n = x + 1
  	_find = _find_from_id(users, n)
  	usr_id, name_ = _find['user_id'], _find['name']
  	email_, status_ = _find['email'], _find['status']
  	print(f'User ID: {usr_id}/nName: {name_}/nEmail: {email_}/nStatus: {status_}')
  
  ### Return list of tables within database
  #print(f"Current tables: {db.tables}")
  ### Find all 'active' users
  #active_users = user_table.find(status='active')
  #print(f"\nActive users: {active_users}")
  ### Verify loaded data
  #print(f"Users from loaded DB: {user_table.get_all()}")

# Quickstart Guide / Example

### The full [quickstart_example.py](../bin/quickstart_example.py) for this guide
This example/guide shows the user how to easily store data for later loading, as well as how to easily retrieve the data and parse it. 

First let's set a filepath for the database file that will be created, initialize a new database, and create a new table. For the example we will be storing products/items for a store.


We will also be saving our database in the current working directory:
```python
db_file = 'quickstart_example.db'
```


I recommend declaring two variables pointing to the actual Pydb and PyTable objects for easier type delcaration and to be able to see type hints.
```python
Database, Table = Pynex.PyDb, Pynex.PyTb
```
Just a recommendation, not required.


Let's initialize a new database, and then can create a new table, which we will call 'products':
```python
  db:Database = Pynex.PyDb()
  products:Table = db.table('products')
```

Since PynexDB supports dynamic table fields, if we happen to forget to add a field that we wanted to store, it can be added to the table at a later time.


For now we will just do some common product/item data found in stores:
  - item_sku (Essentially a unique ID)
  - item_name
  - item_category
  - item_price

> [!NOTE]
> I personally would not recommend using PynexDB for storing heavily and frequntly accessed data. It has yet to be tested, and it's whole purpose was to be small, lightweight, able to be embedded, and fairly easy to use.


Let's go ahead and add some products using the fields (keys) we specificed above. Beforehand, you will notice I have an ```if not os.path.exists``` statement to check for whether or not the database file for this guide/example was alreadt created and to skip data insertion if that's the case. If your database file doesn't seem to work, seems empty or is corrupted, just go ahead and delete it and run the example again, and it should insert and recreate the database save.
```python
if not __os__.path.exists(db_file):
### Key=Value order when adding does not matter
  	products.insert(item_sku=1020, name='Computer Mouse', category='Peripherals', price='$25')
  	products.insert(item_sku=1040, name='Computer Keyboard', category='Peripherals', price='$30')
  	products.insert(item_sku=1060, name='Computer Monitor', category='Peripherals', price='$100')
  	products.insert(item_sku=1080, name='Gaming Headset', category='Peripherals', price='$30')

  	products.insert(item_sku=1110, name='Nokia Flip Phone', category='Cell Phones', price='$50')
  	products.insert(item_sku=1130, name='Samsung Galaxy A16', category='Cell Phones', price='$99')
  	products.insert(item_sku=1150, name='Google Pixel 7a', category='Cell Phones', price='$250')
  	products.insert(item_sku=1170, name='iPhone 14', category='Cell Phones', price='$500')

  	products.insert(item_sku=1200, name='24in TV', category='Televisions', price='$80')
  	products.insert(item_sku=1220, name='36in TV', category='Televisions', price='$160')
  	products.insert(item_sku=1240, name='48in TV', category='Televisions', price='$220')
  	products.insert(item_sku=1260, name='55in TV', category='Televisions', price='$350')
```

That looks good. Now to save it all we have to do is call the database save method, pointing to the database file we set earlier. You may notice the verbose option is set to True, by default it's False. When enabled it just prints a confirmation message when the file saves. Decent option for small debugging purposes.
```python
    db.save(filename=db_file, verbose=True)
```
Once the file has been created and saved, you can actually remove all of the previous code were we added the items, however the if statement should automatically skip running it again if the database file exists. If you do decide to just delete the code, I recommend running the database load method, and double check that the file save succesfully, and all data was entered properly.

```python
  db.load(filename=db_file, verbose=True)
```
When loading/reloading the database from file, you will have to re-declare the set Table variable (products) because the newest 'data' the db object has is whatever is loaded.

```python
  products: Table = db['products']
```

While we are here, let's check our data is correct using the Table class .get_all() method
```python
  print(products.get_all())
```
Proper output:
```
>>> Database saved to : 'store_retrieve_example.db'
>>> Database loaded from : 'store_retrieve_example.db'
>>> [{'item_sku': 1020, 'name': 'Computer Mouse',
  |-> 'category': 'Peripherals', 'price': '$25'},
  |-> {'item_sku': 1040, 'name': 'Computer Keyboard',
  |-> 'category': 'Peripherals', 'price': '$30'}...*
```
* I cut off the third one to save space.

Now one of the features of PynexDB is the ability to find entries based on their specific key.

For example, if we wanted a list of all the stores cell phones, we could filter based on item category, if we wanted a specific item, we could filter by name because all the product names happen to be unique, however this is not always the case. For that purpose we also store the items SKU (Stock Keeping Unit), which will be unique for every item in a store.

We can also filter more than one given criteria, for example if we wanted to find all $30 items within the 'Peripherals' category, we can do that:
```python
filter_items = products.find(category='Peripherals', price='$30')
print(filter_items)
```

Two items should've came back based on the categories and prices we set earlier: Category = Peripherals, Price = $30, which should be the 'Computer Keyboard' and 'Gaming Headset'

The .find() method works for any of the table fields. If you happened to check the type() of the returned items, or just noticed it based on what was printed, the data is returned as a list, so we should be able to easily iterate through it and separate out individual values.

```python
  for item in filter_items:
  	_sku = item['item_sku']
  	_name = item['name']
  	_cat = item['category']
  	_price = item['price']
  	print(f"Item SKU: {_sku}\nItem: {_name}")
  	print(f"Category: {_cat}\nPrice: {_price}")
```

Expected/Correct output:
```
>>> Database loaded from : 'store_retrieve_example.db'

>>> Item SKU: 1040
>>> Item: Computer Keyboard
>>> Category: Peripherals
>>> Price: $30

>>> Item SKU: 1080
>>> Item: Gaming Headset
>>> Category: Peripherals
>>> Price: $30

[Program finished]
```

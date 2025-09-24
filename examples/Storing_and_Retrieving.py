import os as __os__
import sys as __sys__
__sys__.path.append('../')
import PyataDB as Pyata


# This example shows the user how to easily store data for later loading,
# as well as how to easily retrieve the data and parse it.
# First let's initialize a new database, and create a new table. 
# For the example we will be storing products/items for a store.
# We will also be saving our database in the current working directory:
db_file = 'store_retrieve_example.db'

# For Type delcaration / Type hints
# This is recommended, but not required.
Database, Table = Pyata.Pydb, Pyata.PyTable

if __name__ == "__main__":
  # Initialize database -> db
  db:Database = Pyata.Pydb()

  # Create new table named 'products' -> products
  products:Table = db.table('products')

  # Since PyataDB supports dynamic table fields,
  # if we happen to forget to add a field we wanted to store,
  # it can be added to the table later.
  # For now we will just do some common product/item data found in stores:
  # - item_sku (Essentially a unique ID)
  # - item_name
  # - item_category
  # - item_price

  # I personally would not recommend using PyataDB for storing something like the item_amount_in_stock,
  # PyataDB hasn't been tested on commonly heavily accessed values that frequently change.
  # So we will just be storing information about the products.
  # If statement checks to see if database file was alreadt created and saved,
  # if so, the following table insertions won't run.
  # If something messed up, just delete the database file, and try again, then they should run.

  if not __os__.path.exists(db_file):
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

    # That looks good. Now to save it all we have to do is call the database save method,
    # pointing to our database file we set earlier
    db.save(filename=db_file, verbose=True)

  # You might have noticed I set the verbose argument to True, this is by default off,
  # when set to True it just prints out a confirmation method confirming the Database[Table(s)] have been saved, and where to.
  # Once the file has been created and saved, you can actually remove all of the previous code were we added the items,
  # however I would recommend first loading and checking the file first. Which we will do now:
  db.load(filename=db_file, verbose=True)

  # Also by loading the file despite just creating/saving it means when we call table methods for retrieving the data,
  # we will be using the most up-to-date version.
  # Lets quickly verify our loaded data using:
  print(products.get_all())

  # If everything was done as shown above, you should be presented with three print messages.
  # One from saving the file, one from loading, and one showing all of the data inside the table we just created:

  # >>> Database saved to : 'store_retrieve_example.db'
  # >>> Database loaded from : 'store_retrieve_example.db'
  # >>> [{'item_sku': 1020, 'name': 'Computer Mouse', 'category': 'Peripherals', 'price': '$25'},
  # |>> {'item_sku': 1040, 'name': 'Computer Keyboard', 'category': 'Peripherals', 'price': '$30'}...
  ### ** I cut off the third one to save space.

  # Now one of the features of PyataDB is the ability to find entries based on their specific key. For example, if we wanted a list of all the stores cell phones,
  # we could search based on item category, if we wanted a specific item, we could search the name in this case because all the product names happen to be unique,
  # however this is not always the case.
  # For that purpose we also store the items SKU (Stock Keeping Unit), which will be unique for every item in a store.
  # We can also filter more than one given criteria, for example if we wanted to find all $30 items within the 'Pheripherals' category, we can do that:
  
  products: Table = db['products'] # Since we reloaded the database from the file, we have to re-declare our products variable, otherwise it will come back blank.
  filter_items = products.find(category='Peripherals', price='$30')
  print(filter_items)

  # Two items should've came back based on the categories and prices we set earlier: Category = Peripherals, Price = $30, which should be the 'Computer Keyboard' and 'Gaming Headset'
  # The .find() method works for any of the table fields.
  # If you happened to check the type() of the returned items, or just noticed it based on what was printed, the data is returned as a list,
  #  so we should be able to easily iterate through it and separate out individual values.

  for item in filter_items:
  	_sku = item['item_sku']
  	_name = item['name']
  	_cat = item['category']
  	_price = item['price']
  	print(f"Item SKU: {_sku}\nItem: {_name}")
  	print(f"Category: {_cat}\nPrice: {_price}")

      #
  	  #   Database loaded from : 'store_retrieve_example.db'
      #
	  #   Item SKU: 1040
	  #   Item: Computer Keyboard
	  #   Category: Peripherals
	  #   Price: $30
      #
  	  #   Item SKU: 1080
      #   Item: Gaming Headset
	  #   Category: Peripherals
	  #   Price: $30
      #
	  #   [Program finished]
      #

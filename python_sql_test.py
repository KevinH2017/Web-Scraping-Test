import sqlite3

# Establishes a connection and cursor for sql database
connection = sqlite3.connect("./app10/data.db")
cursor = connection.cursor()

# Query data
cursor.execute("SELECT * FROM events WHERE date='2088.10.15'")
row = cursor.fetchall()         # Gets sql data from cursor.execute(), row is a list of tuples
print(row)

# Query data from certain columns
cursor.execute("SELECT band, date FROM events WHERE date='2088.10.15'")         # Returns the band and date values where date='2088.10.15
row = cursor.fetchall()
print(row)

# Insert new rows
# Make sure no program / process has the database opened anywhere
new_rows = [('Cats', 'Cat City', '2088.10.17'), ('Hens', 'Hen City', '2088.10.17')]
cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)            # Inserts new_rows to database
connection.commit()                # Commits the changes to the database
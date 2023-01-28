import sqlite3

def show_tables_and_data(db_name):
    # Connect to the database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Get all table names in the database
    cursor.execute("SELECT name from sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:")
    for table in tables:
        print(table[0])

    # Get all data in each table
    for table in tables:
        table_name = table[0]
        cursor.execute("SELECT * FROM %s" % table_name)
        data = cursor.fetchall()
        print("\nData in table '%s':" % table_name)
        for row in data:
            print(row)

    # Close the connection
    cursor.close()
    conn.close()

# Example usage
show_tables_and_data("genome_database.sqlite")

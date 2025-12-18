import sqlite3
from datetime import datetime, timedelta

PATH = "../data/flaschen_database.db"
# Connect to the SQLite database


conn = sqlite3.connect(PATH)
cursor = conn.cursor()

data = cursor.execute('''
    SELECT * from Flasche;
    
''')

fetch_result = cursor.fetchall()

for fid_rid_data_error in fetch_result:
    print(f" Flasche: {fid_rid_data_error[0]}, Rezept : {fid_rid_data_error[1]}, Datum: {fid_rid_data_error[2]}, Fehler : {fid_rid_data_error[3]}")

def update_has_error(flaschen_id, has_error):
    try:
        cursor.execute("UPDATE Flasche SET has_error = ? WHERE Flaschen_ID = ?", (has_error, flaschen_id))
        conn.commit()
        print(f"Updated has_error for Flaschen_ID {flaschen_id} to {has_error}.")
    except Exception as e:
        conn.rollback()
        print(f"Error occurred while updating has_error for Flaschen_ID {flaschen_id}: {e}")


# Example usage: Update has_error for Flaschen_ID 1 to True
update_has_error(1, True)

# Close the connection
conn.close()
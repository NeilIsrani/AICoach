from database import get_db_connection

try:
    connection = get_db_connection()
    print("Successfully connected to the database!")
    connection.close()
except Exception as e:
    print(f"Connection failed: {e}") 
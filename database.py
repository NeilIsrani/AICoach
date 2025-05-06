import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            consume_results=True  # Add this to automatically consume results
        )
        return connection
    except Error as e:
        raise Exception(f"Database connection error: {e}")

def execute_query(query, params=None):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        connection.commit()
        return results
    except Error as e:
        connection.rollback()
        raise Exception(f"Query execution error: {e}")
    finally:
        cursor.close()
        connection.close()

def call_stored_procedure(procedure_name, params=None):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        if params:
            cursor.callproc(procedure_name, params)
        else:
            cursor.callproc(procedure_name)
        results = []
        for result in cursor.stored_results():
            results.extend(result.fetchall())
        connection.commit()
        return results
    except Error as e:
        connection.rollback()
        raise Exception(f"Stored procedure error: {e}")
    finally:
        cursor.close()
        connection.close() 
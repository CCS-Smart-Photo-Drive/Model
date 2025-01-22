import mysql.connector
import numpy as np
from mysql.connector import Error

def connect_to_database():
   
    try:
        connection = mysql.connector.connect(
            host='host',
            user='username',
            password='password',
            database='db'
        )
        if connection.is_connected():
            print("Connected to database")
            return connection
    except Error as e:
        print(f"Error while connecting to database: {e}")
        return None
    
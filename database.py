import os
from dotenv import load_dotenv
import psycopg2

# Grabbing Evironment variables
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Function to create database
def createTable():
    
    try:
        # Connect to Database
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()

        # Excute SQL Statement to create table
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS users ("
            "discord_id INTEGER NOT NULL,"
            "currency INTEGER NOT NULL)"
            )

        # Close communication to Database
        cursor.close()

        # Commit Changes
        connection.commit()

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

    # Close Connection
    finally:
        if connection is not None:
            connection.close()

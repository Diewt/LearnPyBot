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
            "discord_id BIGINT NOT NULL,"
            "currency BIGINT NOT NULL)"
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

def registerUser(userID):
    try:
        # Connect to Database
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()

        sql = 'SELECT discord_id FROM users WHERE discord_id =' + str(userID) 

        # Flag to check if user already exists in database
        existflag = None

        # Excute SQL Statement to create table
        cursor.execute(sql)
        if cursor.fetchone() is not None:
            # User already exists
            existflag = True
            print('user is in database')
        else:
            # User does not exist
            existflag = False
            sql = 'INSERT INTO users (discord_id, currency) VALUES(%s, %s)'
            cursor.execute(sql, (userID, 0))
            
            print('user is not in database')

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

    return existflag
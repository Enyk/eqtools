import mysql.connector
from mysql.connector import Error
import pandas as pd
import configparser
import getpass

config = configparser.ConfigParser()
config.read("eqdb.ini")
db_user_tmp = config.get("db_vars", "db_user")
db_pass_tmp = config.get("db_vars", "db_pass")
db_host = config.get("db_vars", "db_host")
db_port = config.get("db_vars", "db_port")
db_name = config.get("db_vars", "db_name")

if db_user_tmp == "":
    db_user = input("Enter database user name: ")
else:
    db_user = db_user_tmp

if db_pass_tmp == "":
    db_pass = getpass("Enter database password: ")
else:
    db_pass = db_pass_tmp

def create_server_connection(db_host, db_user, db_pass):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            passwd=db_pass,
            database=db_name
        )
        print("Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


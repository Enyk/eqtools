import mysql.connector
from mysql.connector import Error
import pandas as pd
import configparser
import getpass
import string

##########################################################

def create_server_connection(host, port, user, passwd, name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            database=name
        )
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

##########################################################

## Read config file from eqdb.ini
config = configparser.ConfigParser()
config.read("eqdb.ini")
db_user_tmp = config.get("db_vars", "db_user")
db_pass_tmp = config.get("db_vars", "db_pass")
db_host_tmp = config.get("db_vars", "db_host")
db_port_tmp = config.get("db_vars", "db_port")
db_name_tmp = config.get("db_vars", "db_name")

# If connection information is blank, error out.
if db_host_tmp == "":
    print(f"Error: no db_host defined in config file.")
    exit()
else:
    db_host = db_host_tmp
if db_port_tmp == "":
    print(f"Error: no db_port defined in config file.")
    exit()
else:
    db_port = db_port_tmp
if db_name_tmp == "":
    print(f"Error: no db_name defined in config file.")
    exit()
else:
    db_name = db_name_tmp

## If user or password is blank in the config file, prompt for them.
if db_user_tmp == "":
    db_user = input("Enter database user name: ")
else:
    db_user = db_user_tmp
if db_pass_tmp == "":
    db_pass = getpass.getpass("Enter database password: ")
else:
    db_pass = db_pass_tmp


# Create the connection to the SQL database.
connection = create_server_connection(db_host, db_port, db_user, db_pass, db_name)

# Ask for the faction name to be searched for.
# Replace * with % for the query string.
# Format the string correctly for the submission.
faction_name_input = input("Enter faction name (Wildcards allowed): ")
faction_name = faction_name_input.replace('*','%')
query_string = "SELECT name, base, see_illusion, min_cap, max_cap from faction_list where NAME like \"{}\"".format(faction_name)

# Send the query, store the results in results.
results = read_query(connection, query_string)

# Iterate over results and display the pieces we asked for in a readable format.
# Change the see_illusion return into a Yes/No answer instead of a 0/1.
for (fname, fbase, fsi, fmin, fmax) in results:
    if fsi == 1:
        fsi_answer = "Yes"
    else:
        fsi_answer = "No"
    print("---------------------------------------------------------")
    print("Faction Name: ".ljust(40),fname)
    print("Base faction value: ".ljust(40),fbase)
    print("Does this faction see illusion?: ".ljust(40),fsi_answer)
    print("Faction minimum value: ".ljust(40),fmin)
    print("Faction maximum value: ".ljust(40),fmax)

# All done. Exit.
exit()

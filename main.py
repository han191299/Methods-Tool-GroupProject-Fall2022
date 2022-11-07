import mysql.connector
import sys

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="methods"
    )

    print("Successful connection.")

except:
    print("Failed connection.")
    sys.exit()



cursor = connection.cursor()


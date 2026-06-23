import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="magasin",
        port=3306
    )

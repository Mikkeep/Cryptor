import sqlite3
from constants import *
from sqlite3 import Error, IntegrityError


def read_used_lang(db_name):
    data = ""
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute("""SELECT LANGUAGE FROM LANG""")
        data = cur.fetchone()
        data = data[0]
        conn.close()
    except Error as e:
        used_lang = "English"
        print("Could not read used language from db")
    return data


def create_db_table(db_name):
    connection = sqlite3.connect(db_name)
    cur = connection.cursor()
    try:
        cur.execute(table_lang)
    except IntegrityError as e:
        print("table already exists")
    cur.execute(insert_to_lang)
    connection.commit()
    connection.close()
    print("Database created succesfully")


def check_db(db_name):
    """
    Check existing database
    """
    connection = None
    try:
        connection = sqlite3.connect(db_name)
    except Error as e:
        print("Database does not exist")
    finally:
        if connection:
            cur = connection.cursor()
            try:
                cur.execute("SELECT * from LANG;")
            except sqlite3.OperationalError as e:
                print("Database does not exist, creating a new one")
                create_db_table(db_name)
                connection.close()


def write_used_lang(db_name, language):
    connection = None
    cur = None
    try:
        connection = sqlite3.connect(db_name)
        cur = connection.cursor()
    except Error as e:
        print(e)
    finally:
        sql_command = """ UPDATE LANG
                            SET Language = ?
        """
        cur.execute(sql_command, language)
        print(f"Changed used language to {language}")
        connection.commit()
        connection.close()

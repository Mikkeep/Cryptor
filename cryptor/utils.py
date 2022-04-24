import sqlite3
from constants import *
from sqlite3 import Error, IntegrityError


def read_used_lang(db_name):
    data = ""
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(read_lang)
        data = cur.fetchone()
        data = data[0]
        conn.close()
    except Error as e:
        data = "English"
        print("Could not read used language from db")
    return data


def insert_to_db(db_name, sql_command):
    connection = sqlite3.connect(db_name)
    cur = connection.cursor()
    try:
        cur.execute(sql_command)
        connection.commit()
        connection.close()
    except IntegrityError as e:
        print("Cant insert data")
        return
    print("Data inserted succesfully")


def create_db_table(db_name, sql_command):
    connection = sqlite3.connect(db_name)
    cur = connection.cursor()
    try:
        cur.execute(sql_command)
        connection.commit()
        connection.close()
    except IntegrityError as e:
        print("table already exists")


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
                cur.execute(read_from_lang)
                connection.close()
            except sqlite3.OperationalError as e:
                print("Database does not exist, creating a new one")
                create_db_table(db_name, table_lang)
                create_db_table(db_name, table_mode)
                create_db_table(db_name, table_encrypt)
                insert_to_db(db_name, insert_to_lang)
                insert_to_db(db_name, insert_to_mode)
                insert_to_db(db_name, insert_to_encrypt)
                connection.close()


def check_dark_mode(db_name):
    """
    Check whetever user has selected to use dark mode
    """
    data = ""
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(read_mode)
        data = cur.fetchone()
        data = data[0]
        conn.close()
    except Error as e:
        data = "False"
        print("Could not read used mode from db")
    return data


def write_used_mode(db_name, mode):
    # False is used for Non-darkmode
    # True is for darkmode
    connection = None
    cur = None
    try:
        connection = sqlite3.connect(db_name)
        cur = connection.cursor()
    except Error as e:
        print(e)
    finally:
        sql_command = """ UPDATE MODE
                            SET Darkmode = ?
        """
        cur.execute(sql_command, mode)
        print(f"Changed darkmode to {mode}")
        connection.commit()
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


def write_encryption_defaults(db_name, defaults):
    connection = None
    cur = None
    try:
        connection = sqlite3.connect(db_name)
        cur = connection.cursor()
    except Error as e:
        print(e)
    finally:
        sql_command = """ UPDATE ENCRYPTION
                            SET Hash = ? ,
                                Algorithm = ? ,
                                Salt = ? ,
                                Key = ?
        """
        cur.execute(sql_command, defaults)
        print("Saved default values")
        connection.commit()
        connection.close()


def check_encryption_defaults(db_name):
    """
    Check whetever user has submitted default values for encryption
    """
    data = ""
    defaults = {
        "default_hash": "",
        "default_algo": "",
        "default_salt": "",
        "default_key": "",
    }
    try:
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute(read_encryption)
        data = cur.fetchone()
        defaults["default_hash"] = data[0]
        defaults["default_algo"] = data[1]
        defaults["default_salt"] = data[2]
        defaults["default_key"] = data[3]
        conn.close()
    except Error as e:
        print("Could not read default values from db")
    return defaults

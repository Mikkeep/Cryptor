db_location = "cryptor.db"
inprogresslist = []
USED_LANG = "languages/current_lang.txt"
LANG_LOCATION = "../languages/"
IMG_LOCATION = "../images/"
CURRENT_LANG = ""

table_lang = """ CREATE TABLE LANG (
            Language VARCHAR(255) NOT NULL
        ); """

insert_to_lang = """ INSERT INTO LANG VALUES (
                    'English'
        ); """

read_from_lang = """SELECT * FROM LANG;"""

read_lang = """SELECT LANGUAGE FROM LANG;"""

table_mode = """ CREATE TABLE MODE (
                Darkmode BOOLEAN NOT NULL
        ); """

insert_to_mode = """ INSERT INTO MODE VALUES (
                        'False'
        ); """

read_from_mode = """SELECT * FROM MODE;"""

read_mode = """SELECT DARKMODE FROM MODE;"""
db_location = "cryptor.db"
inprogresslist = []
USED_LANG = "languages/current_lang.txt"
CURRENT_LANG = ""

table_lang = """ CREATE TABLE LANG (
            Language VARCHAR(255) NOT NULL
        ); """

insert_to_lang = """ INSERT INTO LANG VALUES (
                    'English'
        ); """

read_from_lang = """SELECT * FROM LANG"""

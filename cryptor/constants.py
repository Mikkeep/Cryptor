db_location = "cryptor.db"
inprogresslist = []
USED_LANG = "languages/current_lang.txt"
LANG_LOCATION = "../languages/"
IMG_LOCATION = "../images/"
CURRENT_LANG = ""
ENC_ALGORITHMS = ["SHA-256", "SHA-512", "SHA3-512", "MD5"]
ENC_ALGORITHMS_FILES = ["AES", "RSA", "Chacha"]

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

table_encrypt = """ CREATE TABLE ENCRYPTION (
                        Hash VARCHAR(100),
                        Algorithm VARCHAR(100),
                        Salt VARCHAR(255),
                        Key VARCHAR(4096)
                        ); """

insert_to_encrypt = """ INSERT INTO ENCRYPTION VALUES (
                                '',
                                '',
                                '',
                                ''
                                ); """

read_encryption = """SELECT * FROM ENCRYPTION;"""

ENC_TAB_PRESSED_QSS = "QPushButton#encrypt_tab_btn { background-color: #408cfb; border-style: inset;} "
ENC_TAB_DEPRESSED_QSS = "QPushButton#encrypt_tab_btn { background-color: #84b5fd; border-style: outset;} QPushButton#encrypt_tab_btn::hover {background-color: #99c1fd;}"

DEC_TAB_PRESSED_QSS = "QPushButton#decrypt_tab_btn { background-color: #408cfb; border-style: inset;}"
DEC_TAB_DEPRESSED_QSS = "QPushButton#decrypt_tab_btn { background-color: #84b5fd; border-style: outset;} QPushButton#decrypt_tab_btn::hover {background-color: #99c1fd;}"

SETTINGS_PRESSED_QSS = "QPushButton#settings_tab_btn { background-color: #408cfb; border-style: inset;}"
SETTINGS_DEPRESSED_QSS = "QPushButton#settings_tab_btn { background-color: #84b5fd; border-style: outset;} QPushButton#settings_tab_btn::hover {background-color: #99c1fd;}"

ENC_TEXT_PRESSED_QSS = "QPushButton#btn_enc_t { background-color: #408cfb; border-style: inset;}"
ENC_TEXT_DEPRESSED_QSS = "QPushButton#btn_enc_t { background-color: #84b5fd; border-style: outset;} QPushButton#btn_enc_t::hover {background-color: #99c1fd;}"

ENC_FILE_PRESSED_QSS = "QPushButton#btn_enc_f { background-color: #408cfb; border-style: inset;}"
ENC_FILE_DEPRESSED_QSS = "QPushButton#btn_enc_f { background-color: #84b5fd; border-style: outset;} QPushButton#btn_enc_f::hover {background-color: #99c1fd;}"

DEC_TEXT_PRESSED_QSS = "QPushButton#btn_dec_t { background-color: #408cfb; border-style: inset;}"
DEC_TEXT_DEPRESSED_QSS = "QPushButton#btn_dec_t { background-color: #84b5fd; border-style: outset;} QPushButton#btn_dec_t::hover {background-color: #99c1fd;}"

DEC_FILE_PRESSED_QSS = "QPushButton#btn_dec_f { background-color: #408cfb; border-style: inset;}"
DEC_FILE_DEPRESSED_QSS = "QPushButton#btn_dec_f { background-color: #84b5fd; border-style: outset;} QPushButton#btn_dec_f::hover {background-color: #99c1fd;}"


DARK_ENC_TAB_PRESSED_QSS = "QPushButton#encrypt_tab_btn { background-color: #0e6277; border-style: inset;} "
DARK_ENC_TAB_DEPRESSED_QSS = "QPushButton#encrypt_tab_btn { background-color: #064858; border-style: outset;} QPushButton#encrypt_tab_btn::hover {background-color: #174E5C;}"

DARK_DEC_TAB_PRESSED_QSS = "QPushButton#decrypt_tab_btn { background-color: #0e6277; border-style: inset;}"
DARK_DEC_TAB_DEPRESSED_QSS = "QPushButton#decrypt_tab_btn { background-color: #064858; border-style: outset;} QPushButton#decrypt_tab_btn::hover {background-color: #174E5C;}"

DARK_SETTINGS_PRESSED_QSS = "QPushButton#settings_tab_btn { background-color: #0e6277; border-style: inset;}"
DARK_SETTINGS_DEPRESSED_QSS = "QPushButton#settings_tab_btn { background-color: #064858; border-style: outset;} QPushButton#settings_tab_btn::hover {background-color: #174E5C;}"

DARK_ENC_TEXT_PRESSED_QSS = "QPushButton#btn_enc_t { background-color: #0e6277; border-style: inset;}"
DARK_ENC_TEXT_DEPRESSED_QSS = "QPushButton#btn_enc_t { background-color: #064858; border-style: outset;} QPushButton#btn_enc_t::hover {background-color: #174E5C;}"

DARK_ENC_FILE_PRESSED_QSS = "QPushButton#btn_enc_f { background-color: #0e6277; border-style: inset;}"
DARK_ENC_FILE_DEPRESSED_QSS = "QPushButton#btn_enc_f { background-color: #064858; border-style: outset;} QPushButton#btn_enc_f::hover {background-color: #174E5C;}"

DARK_DEC_TEXT_PRESSED_QSS = "QPushButton#btn_dec_t { background-color: #0e6277; border-style: inset;}"
DARK_DEC_TEXT_DEPRESSED_QSS = "QPushButton#btn_dec_t { background-color: #064858; border-style: outset;} QPushButton#btn_dec_t::hover {background-color: #174E5C;}"

DARK_DEC_FILE_PRESSED_QSS = "QPushButton#btn_dec_f { background-color: #0e6277; border-style: inset;}"
DARK_DEC_FILE_DEPRESSED_QSS = "QPushButton#btn_dec_f { background-color: #064858; border-style: outset;} QPushButton#btn_dec_f::hover {background-color: #174E5C;}"

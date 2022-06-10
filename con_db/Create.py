from con_db.Connect import Connect
import data.sql_tables as sql
import data.text as txt
import time


class Create(Connect):
    """ Class for create all tables in PostgreSQL """
    def __init__(self):
        with open('../data/user_data.txt') as file:
            reader = file.read()

        if not reader:
            self._ask_data(text=txt.PASSWORD_TEXT, data_len=3)
            print("[INFO] Don't forget to write down your password!")
            self._ask_data(text=txt.QUESTION_TEXT, data_len=4)
            self._ask_data(text=txt.ANSWER_TEXT, data_len=1)

            self._create_all_tables()
        elif reader.count('\n') == 3:
            if input(txt.DROP_TABLES_TEXT).lower() == 'i fully agree to the deletion of all my tables and the data ' \
                                                      'within them':
                with open('../data/user_data.txt') as file:
                    password = file.readline()
                    question = file.readline()
                    answer = file.readline()
                while True:
                    pass_text = input(txt.ACCEPT_DEL_TEXT)
                    if str(pass_text) == str(password).replace('\n', ''):
                        print('[INFO] Tables will be deleted after 5...', end='')
                        count_1 = 4
                        time.sleep(1)
                        while count_1 != 0:
                            count_2 = 3
                            print(str(count_1), end='')
                            while count_2 != 0:
                                print('.', end='')
                                count_2 -= 1
                                time.sleep(0.334)
                            count_1 -= 1
                        print('0')

                        self._delete_all_tables()
                        print('[INFO] Tables were deleted successfully!')
                        exit(0)

                    elif str(pass_text).lower() == 'reset':
                        self._reset_password(question=str(question), answer=str(answer))
                        break

                    else:
                        print('[INFO] Password is incorrect, please try again!')

        else:
            self._clear_txt()

    def _delete_all_tables(self):
        """ This function delete all PostgreSQL's tables """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql.DROP_CARDS_REPORT)
            cursor.execute(sql.DROP_MESSAGES)
            cursor.execute(sql.DROP_ADMIN_PANEL)
            cursor.execute(sql.DROP_CARDS_TRUE)

        self._close_connection()

    def _create_all_tables(self):
        """ This function create all PostgreSQL's tables """
        self._connect()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(sql.TABLESPACE_PG_GLOBAL)
                cursor.execute(sql.TABLESPACE_PG_DEFAULT)
                cursor.execute(sql.SEQUENCE_VK_ID_SEQ)
                cursor.execute(sql.SEQUENCE_VK_ID_SEQ)
                cursor.execute(sql.SCHEMA_PUBLIC)
                cursor.execute(sql.LOGIN_WRITE_SERVER_FILES)
                cursor.execute(sql.LOGIN_WRITE_ALL_DATA)
                cursor.execute(sql.LOGIN_WRITE_ALL_DATA)
                cursor.execute(sql.LOGIN_PUFFY)
                cursor.execute(sql.LOGIN_POSTGRES)
                cursor.execute(sql.TABLE_MESSAGES)
                cursor.execute(sql.TABLE_CARDS_REPORT)
                cursor.execute(sql.LOGIN_PG_STAT_SCAN_TABLES)
                cursor.execute(sql.LOGIN_PG_SIGNAL_BACKEND)
                cursor.execute(sql.LOGIN_PG_READ_SERVER_FILES)
                cursor.execute(sql.LOGIN_PG_READ_ALL_STATS)
                cursor.execute(sql.LOGIN_PG_READ_ALL_SETTINGS)
                cursor.execute(sql.LOGIN_PG_READ_ALL_DATA)
                cursor.execute(sql.LOGIN_PG_MONITOR)
                cursor.execute(sql.LOGIN_PG_EXECUTE_SERVER_PROGRAM)
                cursor.execute(sql.LOGIN_PG_DATABASE_OWNER)
                cursor.execute(sql.LOGIN_CARDS)
                cursor.execute(sql.LANGUAGE_PLGSQL)
                cursor.execute(sql.EXTENSION_PLPGSQL)
                cursor.execute(sql.DATABASE_CARDS)

                cursor.execute(sql.TABLE_ADMIN_PANEL)
                cursor.execute(sql.TABLE_MESSAGES)
                cursor.execute(sql.TABLE_CARDS_TRUE)
                cursor.execute(sql.TABLE_CARDS_REPORT)
            except Exception as ex:
                print('[INFO] Most likely the database already exists, or something is broken.\nThe code: ', ex)

        self._close_connection()

    def _ask_data(self, text: str, data_len: int):
        """ There we will ask user about some data """
        while True:
            if self._check_data(data=input(text), data_len=data_len):
                break

    def _reset_password(self, question: str, answer: str):
        while True:
            if str(input(txt.SECURITY_KEY_TEXT + question.replace("\n", "") + '?: ')).lower() == \
                    str(answer).replace("\n", "").lower():
                self._clear_txt()
                break

            else:
                print('[INFO] Access denied!')

    @staticmethod
    def _check_data(data: str, data_len: int):
        if len(data) > data_len and data != 'Reset' and data.find('\n') < 0:
            with open('../data/user_data.txt', 'a') as file:
                file.write(data + '\n')
            return True
        else:
            print('[INFO] Data is too short or unavailable value!')
            return False

    @staticmethod
    def _clear_txt():
        with open('../data/user_data.txt', 'w') as file:
            file.write('')
        Create()

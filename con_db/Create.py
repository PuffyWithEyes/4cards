from con_db.Connect import Connect
import data.sql_tables as sql
import data.text as txt
import os
from dotenv import load_dotenv


class Create(Connect):
    """ Class for create all tables in PostgreSQL """
    def __init__(self):
        with open('../data/power.txt') as file:
            reader = file.read()

        if not reader:
            load_dotenv('../con_db/.env')
            # with open('../data/power.txt', 'w') as file:
            #     file.write('0')

            self._ask_data(text=txt.PASSWORD_TEXT, data_len=3, env_key='PASSWORD_APP')
            print("[INFO] Don't forget to write down your password!")

            self._ask_data(text=txt.QUESTION_TEXT, data_len=4, env_key='QUESTION_APP')

            self._ask_data(text=txt.ANSWER_TEXT, data_len=1, env_key='ANSWER_APP')

            # self._create_all_tables()
        else:
            input(txt.DROP_TABLES_TEXT)

    def _create_all_tables(self):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql.ADMIN_PANEL)
            cursor.execute(sql.JSON)
            cursor.execute(sql.MESSAGES)
            cursor.execute(sql.CARDS_TRUE)
            cursor.execute(sql.CARDS_REPORT)

        self._close_connection()

    def _ask_data(self, text: str, data_len: int, env_key: str):
        while True:
            if self._check_data(data=input(text), data_len=data_len, env_key=env_key):
                break

    @staticmethod
    def _check_data(data: str, data_len: int, env_key: str):
        if len(data) > data_len:
            os.environ[env_key] = data
            return True
        else:
            print('[INFO] Data is too short!')
            return False

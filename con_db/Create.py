from con_db.Connect import Connect
import data.sql_tables as sql
import data.text as txt


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

            # self._create_all_tables()
        else:
            if input(txt.DROP_TABLES_TEXT) == 'I fully agree to the deletion of all my tables and the data within them':
                with open('../data/user_data.txt') as file:
                    password = file.readline()
                    question = file.readline()
                    answer = file.readline()
                while True:
                    if input(txt.ACCEPT_DEL_TEXT) == password:
                        pass


    def _delete_all_tables(self):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql.DROP_CARDS_REPORT)
            cursor.execute(sql.DROP_MESSAGES)
            cursor.execute(sql.DROP_ADMIN_PANEL)
            cursor.execute(sql.DROP_JSON)
            cursor.execute(sql.DROP_CARDS_TRUE)

        self._close_connection()

    def _create_all_tables(self):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(sql.ADMIN_PANEL)
            cursor.execute(sql.JSON)
            cursor.execute(sql.MESSAGES)
            cursor.execute(sql.CARDS_TRUE)
            cursor.execute(sql.CARDS_REPORT)

        self._close_connection()

    def _ask_data(self, text: str, data_len: int):
        while True:
            if self._check_data(data=input(text), data_len=data_len):
                break

    @staticmethod
    def _check_data(data: str, data_len: int):
        if len(data) > data_len and data != 'Reset' and data.find('\n') < 0:
            with open('../data/user_data.txt', 'a') as file:
                file.write(data + '\n')
            return True
        else:
            print('[INFO] Data is too short or unavailable value!')
            return False

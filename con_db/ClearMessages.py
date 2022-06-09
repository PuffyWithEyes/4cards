from con_db.Connect import Connect
import threading
import time


class ClearMessages(Connect):
    def __init__(self):
        threading.Thread(target=self._clear_data_db).start()

    def _clear_data_db(self):
        """ Function for delete temp messages of users """
        while True:
            self._connect()
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """DELETE FROM messages;"""
                )

            self._close_connection()
            time.sleep(86400)

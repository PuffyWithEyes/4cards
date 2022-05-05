import time
import threading
from con_db.Connect import Connect


class ClearMessages(Connect):
    def __init__(self):
        threading.Thread(target=self._clear_data).start()

    def _clear_data(self):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                """DELETE FROM messages;"""
            )
            cursor.execute(
                """DELETE FROM json;"""
            )

        self._close_connection()
        time.sleep(86400)

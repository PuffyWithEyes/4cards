import psycopg2
import bot.config as cfg
from con_db.exceptions import ConnectionException


class Connect:
    """ Class for connecting to db """
    def _connect(self):
        """ Function for connect to db """
        try:
            self.connection = psycopg2.connect(  # Connect to db
                host=cfg.HOST,
                user=cfg.USER,
                password=cfg.PASSWORD,
                database=cfg.DB_NAME,
                port=cfg.PORT
            )

            self.connection.autocommit = True  # Save changes to db checkbox

        except (ConnectionRefusedError, ConnectionError, ConnectionAbortedError) as ex:
            self._close_connection()
            raise ConnectionException(ex)

    def _close_connection(self):
        """ Function for close connection """
        if self.connection:
            self.connection.close()

    @staticmethod
    def _check_none(mean):
        """ Check mean for None """
        if mean:  # If mean = None, return False, else True
            return True
        else:
            return False

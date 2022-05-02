from con_db.Connect import Connect


class FindUser(Connect):
    def find_matches(self, mean, column: str):
        """ Function for find matches in column 'column' """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(  # Check for matches
                f"""SELECT {column} FROM cards_true WHERE {column}='{mean}';"""
            )
            find = self._check_none(cursor.fetchone())

            cursor.execute(  # Check for matches
                f"""SELECT id FROM cards_true WHERE {column}='{mean}';"""
            )
            user_id = cursor.fetchone()

            self._close_connection()
            return [find, user_id]


class AddUser(FindUser):
    def add_where(self, value, doc, column: str):
        self._connect()
        with self.connection.cursor() as cursor:
            if not doc:
                cursor.execute(
                    f"""INSERT INTO cards_report ({column}) VALUES ('{value}');"""
                )
            else:
                cursor.execute(
                    f"""INSERT INTO cards_report ({column}, docers) VALUES ('{value}', {doc});"""
                )

        self._close_connection()

    def _add_share_tg(self, share):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO cards_true (share_vk) VALUES ('{share}');"""
            )

        self._close_connection()

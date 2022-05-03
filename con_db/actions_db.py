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
    def add_info(self, value, column: str):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO cards_report ({column}) VALUES ('{value}');"""
            )

        self._close_connection()

    def add_where(self, value, where_value, where: str, column: str):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO cards_report ({column}) VALUES ({value}) WHERE {where}='{where_value}';'"""
            )

        self._close_connection()

    def add_two(self, first_value, second_value, first_column: str, second_column: str):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO cards_report ({first_column}, {second_column}) VALUES ('{first_value}', 
                '{second_value}');"""
            )

        self._close_connection()

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

    def find_matches_where_one(self, data, find_column: str, table: str, where_column: str, flag: bool):
        """ Function for find matches in 1 column """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT {find_column} FROM {table} WHERE {where_column}='{data}';"""
            )
            if flag:
                data_db = cursor.fetchone()
            else:
                data_db = cursor.fetchall()

        self._close_connection()
        return data_db

    def find_matches_where_two(self, data, find_column_one: str, find_column_two: str, table: str, where_column: str,
                               flag: bool):
        """ Function for find matches in 2 column """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT ({find_column_one}, {find_column_two}) FROM {table} WHERE {where_column}='{data}';"""
            )
            if flag:
                data_db = cursor.fetchone()
            else:
                data_db = cursor.fetchall()

        self._close_connection()
        return data_db

    def find_what_one(self, where: str, table: str, flag: bool):
        """ Find all data from some table """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT {where} FROM {table};"""
            )
            if flag:
                data_db = cursor.fetchone()
            else:
                data_db = cursor.fetchall()

        self._close_connection()
        return data_db


class AddUser(Connect):
    def add_info(self, value, column: str, table: str):
        """ Function for add info in table to 1 column """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {table} ({column}) VALUES ('{value}');"""
            )

        self._close_connection()

    def add_two(self, first_value, second_value, first_column: str, second_column: str, table: str):
        """ Function for add info in table to 2 columns """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {table} ({first_column}, {second_column}) VALUES ('{first_value}', '{second_value}');"""
            )

        self._close_connection()

    def add_three(self, first_value, second_value, third_value, first_column: str, second_column: str,
                  third_column: str, table: str):
        """ Function for add info in table to 3 columns """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {table} ({first_column}, {second_column}, {third_column}) VALUES ('{first_value}', 
'{second_value}', '{third_value}');"""
            )

        self._close_connection()

    def add_all(self, first_data, second_data, third_data, fourth_data, fifth_data, sixth_data, seventh_data,
                eighth_data, table: str, first_column: str, second_column: str, third_column: str, fourth_column: str,
                fifth_column: str, sixth_column: str, seventh_column: str, eighth_column: str):
        """ Insert all data """
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO {table} ({first_column}, {second_column}, {third_column}, {fourth_column}, 
{fifth_column}, {sixth_column}, {seventh_column}, {eighth_column}) VALUES ({first_data}, {second_data}, 
{third_data}, {fourth_data}, {fifth_data}, {sixth_data}, {seventh_data}, {eighth_data});"""
            )

        self._close_connection()


class DeleteInfo(Connect):
    def delete_where(self, data, table: str, column: str):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""DELETE FROM {table} WHERE {column}='{data}';"""
            )

        self._close_connection()


class UpdateInfo(Connect):
    def update_where(self, data_what, data_where, table_what: str, table_where: str, table: str):
        self._connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"""UPDATE {table} SET {table_what}='{data_what}' WHERE {table_where}='{data_where}';"""
            )

        self._close_connection()

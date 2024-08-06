import psycopg2
from psycopg2 import sql


class PostgresConnection:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = self.connect()
        self.cursor = self.connection.cursor()

    def connect(self):
        try:
            connection = psycopg2.connect(
                database=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )

            return connection
        except Exception as e:
            raise ValueError(f"Error in database connection: {str(e)}")

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_many(self, table, files):
        try:

            columns: tuple = tuple(files[0].keys())
            all_values: list = [tuple(file.values()) for file in files]

            SAVE_QUERY_WITHOUT_PRIMARY_KEY: str = """
                     INSERT INTO {tableName} {columns} VALUES {values}
                """

            query: str = SAVE_QUERY_WITHOUT_PRIMARY_KEY.format(tableName=table,
                                                               columns=str(columns).replace("'", '"'),
                                                               values=', '.join(map(str, all_values)))

            if ' group,' in query or ' group ' in query:
                query = query.replace(" group", '"group"')

            if ' when,' in query or ' when ' in query:
                query = query.replace(" when", '"when"')

            query = query.replace("None", "null")

            self.cursor.execute(query=query)
            self.connection.commit()
            return True

        except Exception as err:
            raise Exception(err)

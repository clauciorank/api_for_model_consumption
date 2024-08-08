import psycopg2
from psycopg2 import sql

class PostgresConnection:
    def __init__(self, dbname, user, password, host, port):
        # Initialize database connection parameters
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # Establish the connection and create a cursor
        self.connection = self.connect()
        self.cursor = self.connection.cursor()

    def connect(self):
        try:
            # Attempt to connect to the PostgreSQL database
            connection = psycopg2.connect(
                database=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return connection
        except Exception as e:
            # Handle connection errors
            raise ValueError(f"Error in database connection: {str(e)}")

    def close(self):
        # Close the cursor and the database connection
        self.cursor.close()
        self.connection.close()

    def get_query(self, query):
        # Execute a query and return all results
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insert_many(self, table, files):
        try:
            # Prepare column names and values for insertion
            columns: tuple = tuple(files[0].keys())
            all_values: list = [tuple(file.values()) for file in files]

            # Prepare an SQL query for bulk insertion
            SAVE_QUERY_WITHOUT_PRIMARY_KEY: str = """
                INSERT INTO {tableName} {columns} VALUES {values}
            """

            query: str = SAVE_QUERY_WITHOUT_PRIMARY_KEY.format(
                tableName=table,
                columns=str(columns).replace("'", '"'),
                values=', '.join(map(str, all_values))
            )

            # Handle reserved keywords in column names
            if ' group,' in query or ' group ' in query:
                query = query.replace(" group", '"group"')

            if ' when,' in query or ' when ' in query:
                query = query.replace(" when", '"when"')

            # Replace None with null in the query
            query = query.replace("None", "null")

            # Execute the query and commit the transaction
            self.cursor.execute(query=query)
            self.connection.commit()
            return True

        except Exception as err:
            # Handle any errors during insertion
            raise Exception(err)

import psycopg

class Database:
    def __init__(self, host: str, port: int, dbname: str, user: str, password: str) -> None:
        self.connection = psycopg.connect(
            host=host, port=port, dbname=dbname, user=user, password=password
        )
        self.cursor = self.connection.cursor()

    def close_connection(self) -> None:
        self.cursor.close()
        self.connection.close()

    def get_cursor(self) -> psycopg.Cursor:
        return self.cursor
    
    def get_connection(self) -> psycopg.Connection:
        return self.connection
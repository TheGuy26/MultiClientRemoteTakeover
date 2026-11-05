import sqlite3

from httpx import request

from backend.commandRequest import CommandRequest
from backend.commandResponse import CommandResponse

class Database:
    name: str
    table_name: str
    connection: sqlite3.Connection

    def __init__(self, name: str):
        if len(name) <= 3 or name[-3:] != ".db":
            raise ValueError(f"'{name}' is not a valid database name.")

        self.name = name
        self.table_name = "requests"
        try:
            self.connection = sqlite3.connect(database=name)
        except sqlite3.Error as e:
            print("Database Connection Error - " + str(e))

        self.create_table() # Creates only if table doesn't exist

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY,
            temp_id INTEGER,
            uri TEXT NOT NULL,
            parameters TEXT,
            response_status_code INTEGER,
            response_body TEXT  
        )
        """
        self.send_query(query=query)

    def insert_request(self, request: CommandRequest, response: CommandResponse):
        query = (f"INSERT INTO {self.table_name} (temp_id, uri, parameters, response_status_code, response_body)"
                 f" VALUES (?, ?, ?, ?, ?)")
        self.send_query(query=query, parameters=(request.id, request.uri, str(request.parameters),
                                                 response.status_code, str(response.body)))

    def send_query(self, query: str, parameters: tuple | None = None) -> list[tuple] | None:
        try:
            with self.connection:
                if parameters:
                    rows = self.connection.execute(query, parameters).fetchall()
                else:
                    rows = self.connection.execute(query).fetchall()
                if rows:
                    return rows
        except sqlite3.Error as e:
            print("Database Connection Error - " + str(e))


def test():
    database = Database(name="test.db")
    request = CommandRequest(uri="test", parameters={"par1": "test"}, id=1)
    response = CommandResponse(request_id=1, status_code=1, body="ok")
    database.insert_request(request, response)

def main():
    test()

if __name__ == "__main__":
    main()
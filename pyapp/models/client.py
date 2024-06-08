import psycopg
from psycopg.rows import dict_row
import time
from models.entry import Entry


# Guest book client is a class intended to represent a client connection to the
# SQL database
# When this client is initialized it should connect to the database
# The client should offer methods that manipulate the database like viewing all
# entries
# and adding new entries


class GuestbookClient:
    # Initialize the guestbook client object by connecting to the database
    # The intention is that the user does not need to access a connection
    # directly
    def __init__(self, database, user, password, host, port):

        self._database = database
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._connection = self._connect()

        # Assume we have a connection otherwise unhandled exception
        self._initialize_table()

    # Connection with retry
    def _connect(self):
        retries = 0
        delay = 2
        while retries < 3:
            try:
                connection = psycopg.connect(
                    dbname=self._database,
                    user=self._user,
                    password=self._password,
                    host=self._host,
                    port=self._port
                )
                return connection
            except Exception as e:
                retries += 1
                if retries < 3:
                    time.sleep(delay)
                    # Backoff
                    delay *= 2
                else:
                    # At this point we raise an error so that the caller can
                    # handle it
                    raise Exception(
                        f"Error connecting to the database; \
                        rety attempts exhausted. Error: {e}")

    # A disconnect method to terminate an open database connection. Normally
    # this should be executed on graceful termination of the application
    def disconnect(self):
        if self._connection is not None:
            self._connection.close()
            print("Disconnected from the database")

    # This method is a wrapper for handling querys

    def execute_query(self, query, parameters=None):
        cursor = None
        try:
            cursor = self._connection.cursor(row_factory=dict_row)
            cursor.execute(query, parameters)
            self._connection.commit()

            # Determine if the query was a SELECT
            if cursor.description is not None:
                # Fetch the result for SELECT queries
                result = cursor.fetchall()
            else:
                # For non-SELECT queries, just return the row count
                result = cursor.rowcount

            return result
        except psycopg.ProgrammingError as pe:
            self._connection.rollback()
            raise Exception(
                f"ProgrammingError during query execution: {
                    query}. Parameters: {parameters}. Error: {pe}"
            )
        except psycopg.IntegrityError as ie:
            self._connection.rollback()
            raise Exception(
                f"IntegrityError during query execution: {
                    query}. Parameters: {parameters}. Error: {ie}"
            )
        except Exception as e:
            self._connection.rollback()
            raise Exception(
                f"General error during query execution: {
                    query}. Parameters: {parameters}. Error: {e}"
            )
        finally:
            if cursor is not None:
                cursor.close()

    # The first abstaction includes protection from sqlinjections when
    # inserting entries

    def insert_entry(self, entry: Entry):
        try:
            result = self.execute_query(
                "INSERT INTO \
                guestbook(firstname, lastname, message, entrytime) \
                    VALUES (%s, %s, %s, %s)",
                (entry.firstname,
                 entry.lastname,
                 entry.message,
                 entry.entrytime))
            return result
        except Exception as e:
            raise Exception(
                f"Insertion error for entry with the following parameters: \
                Message: \"{entry.message}\", \
                Entrytime: \"{entry.entrytime}\". Error: {e}")

    # The second abstraction to list all entries
    def fetch_all_entries(self):
        try:
            result = self.execute_query("SELECT * FROM guestbook")
            return result
        except Exception as e:
            raise Exception(
                f"Select error when fetching all entries. Error: {e}")

    # Helper function to initialize the guestbook table
    def _initialize_table(self):
        try:
            result = self.execute_query(
                "CREATE TABLE IF NOT EXISTS guestbook( \
                firstname varchar(100), \
                lastname varchar(100), \
                message varchar(280), \
                entrytime timestamptz  \
                )")
            return result
        except Exception as e:
            raise Exception(
                f"Initialization error while creating guestbook table.\
                Error: {e}")

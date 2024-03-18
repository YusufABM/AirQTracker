""" This module encapsulates the SQLite3 operations for sensor data."""
import datetime
import sqlite3
import math


class SensorDataSQLite3db:
    """Encapsulates the SQLite3 operations for sensor data."""

    _DB_TABLE_NAME = "sensor_data"

    _DB_CREATE_SQL = f"""
    CREATE TABLE IF NOT EXISTS {_DB_TABLE_NAME}
       (id INTEGER PRIMARY KEY AUTOINCREMENT,
        eCO2_value INTEGER,
        TVOC_value INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
       )
    """

    _DB_INSERT_SQL = f"""
    INSERT INTO {_DB_TABLE_NAME} (eCO2_value, TVOC_value, timestamp) VALUES (?, ?, ?)
    """

    _DB_SELECT_MIN_MAX_LATEST_SQL = f"""
    SELECT MIN(eCO2_value), MAX(eCO2_value), MIN(TVOC_value), MAX(TVOC_value),
           eCO2_value, TVOC_value
    FROM {_DB_TABLE_NAME}
    """

    _DB_SELECT_ALL_SQL = f"""
    SELECT * FROM {_DB_TABLE_NAME} ORDER BY timestamp DESC LIMIT ? OFFSET ?
    """

    _DB_COUNT_SQL = f"""
    SELECT COUNT(*) FROM {_DB_TABLE_NAME}
    """

    def __init__(self, db_name: str) -> None:
        """Initializes the database

        Args:
            db_name (str): the full path to the database file
        """
        self._db_name = db_name
        self._conn = sqlite3.connect(db_name)  # Connection opened here
        self.cursor = self._conn.cursor()
        self.cursor.execute(self._DB_CREATE_SQL)
        self._conn.commit()

    def insert_data(self, payload):
        """Insert sensor data into the database.
        >>> db = SensorDataSQLite3db('test.db')
        >>> db.insert_data({'eCO2': 400, 'TVOC': 0, 'timestamp': '2022-01-01T00:00:00'})  # doctest: +SKIP
        """

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute(self._DB_INSERT_SQL,
                            (payload['eCO2'], payload['TVOC'], timestamp))
        self._conn.commit()

    def get_min_max_latest(self) -> dict:
        """
        Retrieves the minimum, maximum, and latest eCO2 and TVOC values.

        >>> db = SensorDataSQLite3db('test.db')
        >>> db.get_min_max_latest()  # doctest: +SKIP
        {'eCO2': {'min': 400, 'max': 500, 'latest': 450}, 'TVOC': {'min': 0, 'max': 10, 'latest': 5}}
        """

        self.cursor.execute(self._DB_SELECT_MIN_MAX_LATEST_SQL)
        min_ec02, max_ec02, min_tvoc, max_tvoc, latest_ec02, latest_tvoc = self.cursor.fetchone()
        return {
            'eCO2': {'min': min_ec02, 'max': max_ec02, 'latest': latest_ec02},
            'TVOC': {'min': min_tvoc, 'max': max_tvoc, 'latest': latest_tvoc}
        }

    def get_all_data(self, start, end) -> list:
        """
        Retrieves sensor data, latest first, with pagination.
        >>> db = SensorDataSQLite3db('test.db')
        >>> db.get_all_data(0, 20)  # doctest: +SKIP
        # ...
        """
        self.cursor.execute(self._DB_SELECT_ALL_SQL, (end - start, start)
                            )  # Replace placeholders with start and end
        return self.cursor.fetchall()

    def close(self) -> None:
        """Closes the connection to the database."""
        self._conn.commit()
        self._conn.close()

    def get_total_pages(self, items_per_page=20) -> int:
        """
        Retrieves the total number of pages for the sensor data.
        """
        self.cursor.execute(self._DB_COUNT_SQL)
        total_items = self.cursor.fetchone()[0]
        total_pages = math.ceil(total_items / items_per_page)
        return total_pages


# Run the doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

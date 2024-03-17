""" This module encapsulates the SQLite3 operations for sensor data."""
import datetime
import sqlite3


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
    INSERT INTO {_DB_TABLE_NAME} (eCO2_value, TVOC_value) VALUES (?, ?)
    """

    _DB_SELECT_MIN_MAX_LATEST_SQL = f"""
    SELECT MIN(eCO2_value), MAX(eCO2_value), MIN(TVOC_value), MAX(TVOC_value),
           eCO2_value, TVOC_value
    FROM {_DB_TABLE_NAME}
    """

    _DB_SELECT_ALL_SQL = f"""
    SELECT * FROM {_DB_TABLE_NAME} ORDER BY timestamp DESC
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
        """Insert sensor data into the database."""
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.cursor.execute(self._DB_INSERT_SQL,
                            (payload['eCO2'], payload['TVOC'], timestamp))
        self._conn.commit()

    def get_min_max_latest(self) -> dict:
        """Retrieves min, max, and latest values for eCO2 and TVOC."""
        self.cursor.execute(self._DB_SELECT_MIN_MAX_LATEST_SQL)
        min_ec02, max_ec02, min_tvoc, max_tvoc, latest_ec02, latest_tvoc = self.cursor.fetchone()
        return {
            'eCO2': {'min': min_ec02, 'max': max_ec02, 'latest': latest_ec02},
            'TVOC': {'min': min_tvoc, 'max': max_tvoc, 'latest': latest_tvoc}
        }

    def get_all_data(self) -> list:
        """Retrieves all sensor data, latest first."""
        self.cursor.execute(self._DB_SELECT_ALL_SQL)
        return self.cursor.fetchall()

    def close(self) -> None:
        """Closes the connection to the database."""
        self._conn.commit()
        self._conn.close()


# Run the doctests
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

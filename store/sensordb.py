import datetime
import json
import sqlite3


class Database:
    """
    A class to interact with the SQLite database
    """
    def __init__(self, db_name='mqtt_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """
        Create a table in the database to store sensor data.
        """
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    eCO2_value INTEGER,
                    TVOC_value INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
                    )''')
        self.conn.commit()

    def insert_data(self, payload):
        """
        Insert sensor data into the database.
        """
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.cursor.execute("INSERT INTO sensor_data (eCO2_value, TVOC_value, timestamp) VALUES (?, ?, ?)",
                            (payload['eCO2_value'], payload['TVOC_value'], timestamp))
        self.conn.commit()

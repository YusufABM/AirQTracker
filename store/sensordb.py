import datetime
import json
import sqlite3

class Database:
    def __init__(self, db_name='mqtt_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def insert_data(self, payload):
      timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      topic = 'sensor_data'
      qos = 1
      self.cursor.execute("INSERT INTO mqtt_data (timestamp, topic, payload, qos) VALUES (?, ?, ?, ?)", (timestamp, topic, json.dumps(payload), qos))
      self.conn.commit()

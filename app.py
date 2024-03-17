"""Main file for the sensor data application."""
import os.path
from flask import Flask, render_template, jsonify, g, Response
from store.sensordb import SensorDataSQLite3db

app = Flask(__name__)

app.secret_key = 'Netcompany123'
app.config['SECRET_KEY'] = 'Netcompany123'

@app.route('/')
def main() -> str:
    """Main route for the application"""
    return render_template('index.html')

@app.route('/store/sensor')  # Removed methods=['GET'] as it's the default
def get_index_data() -> Response:
    """Get min, max, and latest sensor data"""
    db = get_db()
    data = db.get_min_max_latest()
    return jsonify(data)

def get_db() -> SensorDataSQLite3db:
    """Returns the database object"""
    if "db_instance" not in g:
        root_dir = os.path.abspath(os.path.dirname(__file__))
        sqlite3_db = os.path.join(root_dir, "store/mqtt_data.db")
        g.db_instance = SensorDataSQLite3db(sqlite3_db)
    return g.db_instance

@app.teardown_appcontext
def close_db_connection(exception):
    """Close the database connection"""
    db_instance = g.pop('db_instance', None)

    if db_instance is not None:
        db_instance.close()

if __name__ == '__main__':
    app.run(debug=True)

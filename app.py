"""Main file for the sensor data application."""
import os.path
from flask import Flask, render_template, jsonify, g, Response, request
from store.sensordb import SensorDataSQLite3db
import math

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

@app.route('/store/sensor/all', methods=['GET', 'POST'])
def get_all_sensor_data():
    """Get all sensor data with pagination"""
    page = request.args.get('page', default=1, type=int)
    print(f"Page: {page}")
    db = get_db()
    per_page = 20
    total_pages = db.get_total_pages()

    # Ensure total_pages is correctly representing the total number of pages
    max_page = total_pages
    print(f"Max Page: {max_page}")

    # Ensure page number is within valid range (1 to max_page)
    page = min(max(page, 1), max_page)  # Clamp page number between 1 and max_page
    print(f"Clamped Page: {page}")
    start = (page - 1) * per_page
    end = start + per_page
    print(f"Start: {start}, End: {end}")
    data = db.get_all_data(start,end)  # Assuming data is a list of sensor data objects
    paginated_data = data[start:end]
    print(f"Paginated Data: {paginated_data}")
    return jsonify({'data': data, 'total_pages': total_pages})

@app.route('/datapage')
def datapage():
    """Route to display all sensor data"""

    return render_template('datapage.html')

@app.teardown_appcontext
def close_db_connection(exception):
    """Close the database connection"""
    db_instance = g.pop('db_instance', None)

    if db_instance is not None:
        db_instance.close()

    if exception is not None:
        print(f"Exception: {exception}")

if __name__ == '__main__':
    app.run(debug=True)

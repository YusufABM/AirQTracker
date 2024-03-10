"""This is the main file for the application."""
from flask import Flask, render_template
app = Flask(__name__)

app.secret_key = 'Netcompany123'
app.config['SECRET_KEY'] = 'Netcompany123'


@app.route('/')
def main():
    """Main route for the application"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

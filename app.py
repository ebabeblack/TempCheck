import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from helpers import get_weather
from datetime import datetime

app = Flask(__name__)
DATABASE = 'tempcheck.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        outfit = request.form.get('outfit')
        feeling = request.form.get('feeling')
        weather = request.form.get('weather')
        lat = request.form.get('latitude')
        lon = request.form.get('longitude')
        
        # Get current weather data
        current_weather = get_weather(lat, lon)
        timestamp = current_weather['time']
        temp = current_weather['temperature_2m']
        humidity = current_weather['relative_humidity_2m']
        cloud = current_weather['cloud_cover']
        wind = current_weather['wind_speed_10m']
        
        # Insert the form data into the database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO entries (clo, lat, lon, feeling, timestamp, temp, humidity, cloud, wind)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (outfit, lat, lon, feeling, timestamp, temp, humidity, cloud, wind))
        conn.commit()
        conn.close()
        
        return redirect(url_for('home'))
    return render_template('form.html')

@app.route('/map')
def map():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT lat, lon, feeling, temp, humidity, timestamp FROM entries')
    entries = cursor.fetchall()
    conn.close()
    
    markers = [{'lat': entry['lat'], 'lon': entry['lon'], 'popup': f"Time: {datetime.utcfromtimestamp(int(entry['timestamp']))}, Feeling: {entry['feeling']}, Temp: {round(entry['temp'], 1)}°F, Humidity: {round(entry['humidity'], 2)}%"} for entry in entries]
    
    return render_template('map.html', markers=markers)


if __name__ == '__main__':
    app.run(debug=True)
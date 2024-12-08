import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from helpers import get_weather, feeling_to_color
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'dev'  # Add this line. In production, use a secure random key
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
        # Get form data
        outfit = request.form.get('outfit')
        feeling = request.form.get('feeling')
        lat = request.form.get('latitude')
        lon = request.form.get('longitude')
        
        # Validate outfit (1-5)
        try:
            outfit = int(outfit)
            if not 1 <= outfit <= 5:
                flash('Outfit value must be between 1 and 5')
                return redirect(url_for('form'))
        except (TypeError, ValueError):
            flash('Invalid outfit input')
            return redirect(url_for('form'))
            
        # Validate feeling (1-5)
        try:
            feeling = int(feeling)
            if not 1 <= feeling <= 5:
                flash('Feeling value must be between 1 and 5')
                return redirect(url_for('form'))
        except (TypeError, ValueError):
            flash('Invalid feeling input')
            return redirect(url_for('form'))

        # Validate latitude (-90 to 90)
        try:
            lat = float(lat)
            if not -90 <= lat <= 90:
                flash('Invalid Location')
                return redirect(url_for('form'))
        except (TypeError, ValueError):
            flash('Invalid Location')
            return redirect(url_for('form'))

        # Validate longitude (-180 to 180)
        try:
            lon = float(lon)
            if not -180 <= lon <= 180:
                flash('Invalid Loaction')
                return redirect(url_for('form'))
        except (TypeError, ValueError):
            flash('Invalid Location')
            return redirect(url_for('form'))

        # If we get here, all validations passed
        # Get current weather data
        current_weather = get_weather(lat, lon)
        timestamp = current_weather['time']
        temp = current_weather['temperature_2m']
        humidity = current_weather['relative_humidity_2m']
        cloud = current_weather['cloud_cover']
        wind = current_weather['wind_speed_10m']

        # Insert into database
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO entries (clo, lat, lon, feeling, timestamp, temp, humidity, cloud, wind)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (outfit, lat, lon, feeling, timestamp, temp, humidity, cloud, wind))
        conn.commit()
        conn.close()

        return redirect(url_for('map'))

    return render_template('form.html', feeling_to_color=feeling_to_color)

@app.route('/map', methods=['GET', 'POST'])
def map():
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT lat, lon, feeling, temp, humidity, wind, timestamp FROM entries WHERE 1=1'
    params = []

    temp_min = request.form.get('temp_min') or ''
    temp_max = request.form.get('temp_max') or ''
    humidity_min = request.form.get('humidity_min') or ''
    humidity_max = request.form.get('humidity_max') or ''
    wind_min = request.form.get('wind_min') or ''
    wind_max = request.form.get('wind_max') or ''
    date = request.form.get('date') or ''
    time = request.form.get('time') or ''


    if temp_min:
        query += ' AND temp >= ?'
        params.append(temp_min)
    if temp_max:
        query += ' AND temp <= ?'
        params.append(temp_max)
    if humidity_min:
        query += ' AND humidity >= ?'
        params.append(humidity_min)
    if humidity_max:
        query += ' AND humidity <= ?'
        params.append(humidity_max)
    if wind_min:
        query += ' AND wind >= ?'
        params.append(wind_min)
    if wind_max:
        query += ' AND wind <= ?'
        params.append(wind_max)
    if date:
        query += ' AND DATE(timestamp) = ?'
        params.append(date)
    if time:
        query += ' AND TIME(timestamp) = ?'
        params.append(time)

    cursor.execute(query, params)
    entries = cursor.fetchall()
    conn.close()
    
    markers = [{'lat': entry['lat'], 'lon': entry['lon'], 'color': feeling_to_color(entry['feeling']), 'popup': f"Time: {datetime.utcfromtimestamp(int(entry['timestamp']))}, Feeling: {entry['feeling']}, Temp: {round(entry['temp'], 1)}°F, Humidity: {round(entry['humidity'], 2)}%, Wind: {round(entry['wind'], 1)} mph"} for entry in entries]
    
    return render_template('map.html', markers=markers, temp_min=temp_min, temp_max=temp_max, humidity_min=humidity_min, humidity_max=humidity_max, wind_min=wind_min, wind_max=wind_max)

if __name__ == '__main__':
    app.run(debug=True)
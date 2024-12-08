# TempCheck

## Overview
TempCheck is a web application that allows users to submit their feelings about the temperature and visualize the data on a map. The app collects data on how comfortable people are outside, which can be used to catalog hot and cold spots in a city.
I ran a small script to create fake data points to show how the Map might look after sometime online!
Enjoy. [Here's](https://youtu.be/mLNoaWzkfq0) the video summary.


## Features
- Submit data on clothing and temperature feelings.
- Visualize data on a map with markers indicating different feelings.
- Filter data based on temperature, humidity, wind speed.

## Prerequisites
- Python 3.x
- Flask
- SQLite3
- Leaflet.js

## Running the code
This was created using a venv python environment. 
To successfully run the file using codespace, run the following commands:

## Installation
1. **To create a vitrual environment:**
```sh
python -m venv venv
```
2. **Activate the virtual Environemnt**
<br>
On windows run:
```sh
venv\Scripts\activate
```
For mac:
```sh
source venv/bin/activate
```
3. **Install the required packages:**
```sh
pip install -r requirements.txt
```
## Running the application
1. **Run flask application:**
```sh
python app.py
```
2. **Navigate to browser link:**
3. **Submit Data:**
- Click on the "Form" link in the navigation bar.
- Fill out the form with your clothing and temperature feelings.
- Submit the form to add your data to the database.
4. **View Map:**
- Click on the "Map" link in the navigation bar.
- Use the filters to view specific data based on temperature, humidity, wind speed, date, and time.
- The map will display markers indicating different feelings.


## File structure
app.py: Main Flask application file.
<br>
helpers.py: Helper functions for the application.
<br>
templates/: Directory containing HTML templates.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;layout.html: Base layout template.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; home.html: Home page template.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;form.html: Form page template.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;map.html: Map page template.
<br>
static/: Directory containing static files.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    universal.css: CSS file for styling.
<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    pics/: Directory containing images.
<br>
tempcheck.db: SQLite database file.
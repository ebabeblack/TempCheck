# TempCheck - Technical Design Document

## Overview
TempCheck is built using a Flask web application with a SQLite database, relying on jinja and leaflet for visualiztion techniques.

## Key Components

### Database Design
The application uses SQLite3 for data storage, chosen for its simplicity and portability. The main table `entries` stores:
- `id`: Unique identifier (INTEGER PRIMARY KEY AUTOINCREMENT)
- `clo`: Clothing level (INTEGER)
- `lat/lon`: Geographic coordinates (TEXT)
- `feeling`: Temperature comfort level (INTEGER)
- `timestamp`: Time of entry (TEXT)
- Weather data:
  - `temp`: Temperature (REAL)
  - `humidity`: Humidity percentage (REAL)
  - `cloud`: Cloud cover (REAL)
  - `wind`: Wind speed (REAL)

### Frontend Implementation
The frontend utilizes several key technologies:
1. **Leaflet.js**: Chosen for its lightweight nature and extensive mapping capabilities. The map is centered on Cambridge, MA, with custom markers showing temperature comfort levels.
2. **Bootstrap**: Used for responsive design and consistent styling.
3. **Custom CSS**: Implemented in universal.css for specific styling needs. This structure was borrowed from a web tutorial at [How to Make a Web Map with Python’s Flask and Leaflet](https://medium.com/geekculture/how-to-make-a-web-map-with-pythons-flask-and-leaflet-9318c73c67c3) but modified for relevance across all the temaplates in an effort to centralize the css.

### Backend Components

#### app.py
The main application file handles:
- Route definitions
- Database connections
- Form processing
- Data visualization logic

Key design decisions:
- Use of `sqlite3.Row` factory for dictionary-like access to database rows
- Implementation of `feeling_to_color` function for visual representation of comfort levels
- Separation of concerns between route handlers and helper functions

#### helpers.py
Contains utility functions, notably:
- `get_weather`: Interfaces with the [Open-Meteo API](https://open-meteo.com/) for weather data
- Weather data processing functions
- Data validation helpers

## Technical Decisions

### API Integration
The Open-Meteo API was selected for weather data because:
1. No API key required
2. Free tier supports necessary functionality
3. Reliable and well-documented
4. Provides all required weather parameters
5. Provides estimates for weather conditions based on Lat/Long as opposed to from a specific weather station, freeing me from having to write a function to find nearest station

### Frontend Framework
Leaflet.js was chosen over alternatives like Google Maps because:
1. Open-source and free
2. Lightweight (38KB)
3. Mobile-friendly
4. Extensive documentation
5. Active community support

### Data Visualization
The color-coding system for temperature comfort uses a blue-yellow-red scale:
- Blue (1): Too cold
- Yellow (3): Comfortable
- Red (5): Too hot
This provides intuitive visual feedback and matches common temperature associations. Having an alpha on these points provides a 'dot-desnity' feel to the data visualization. Combined with filtering function this is designed so that as the map fills up, hot and cold spots will become visually apparent.

## Security Considerations
1. Input Validation: All form inputs are validated server-side
2. SQL Injection Prevention: Use of parameterized queries

## Performance Optimizations
1. Database indexing on frequently queried columns
2. Client-side caching of static assets
3. Efficient SQL queries using appropriate WHERE clauses
4. Minimal JavaScript dependencies

## Future Improvements
1. Interpolation of data analysis
2. Raster development
3. Mobile application interface

## Deployment Considerations
The application is designed for easy deployment:
1. Minimal dependencies
2. Environment variable configuration
3. Database backup capabilities
4. Error logging system

This design prioritizes simplicity, maintainability, and user experience while providing a solid foundation for future enhancements.
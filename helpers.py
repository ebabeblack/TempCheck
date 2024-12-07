import openmeteo_requests
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch"
    }
    responses = openmeteo.weather_api(url, params=params)
    
    # Process first location
    response = responses[0]
    
    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_weather = {
        "time": current.Time(),
        "temperature_2m": current.Variables(0).Value(),
        "relative_humidity_2m": current.Variables(1).Value(),
        "cloud_cover": current.Variables(2).Value(),
        "wind_speed_10m": current.Variables(3).Value()
    }
    
    return current_weather
from flask import Flask, render_template, request
import requests
from datetime import datetime
import os

app = Flask(__name__)

API_KEY = "144239d8630d197432665a9298897f8b"  # Replace with your actual API key
BASE_URL = "https://api.openweathermap.org/data/2.5"

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def get_weather_forecast(city):
    try:
        # Get 5-day forecast directly (no need for coordinates)
        forecast_url = f"{BASE_URL}/forecast?q={city}&appid={API_KEY}"
        print(f"Calling forecast API: {forecast_url}")  # Debug print
        
        response = requests.get(forecast_url)
        
        if response.status_code != 200:
            print(f"API Error: {response.status_code}")
            print(f"Error response: {response.text}")
            return None
            
        data = response.json()
        
        # Process forecast data
        processed_data = {
            'city': data['city']['name'],
            'country': data['city']['country'],
            'daily': []
        }
        
        # Get one forecast per day (the API returns data every 3 hours)
        days_processed = set()
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            
            # Only take the first forecast for each day
            if date not in days_processed:
                days_processed.add(date)
                processed_data['daily'].append({
                    'date': date,
                    'day_temp': kelvin_to_celsius(item['main']['temp']),
                    'night_temp': kelvin_to_celsius(item['main']['temp_min']),
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'].capitalize()
                })
                
                # Stop after 5 days
                if len(processed_data['daily']) >= 5:
                    break
        
        return processed_data
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = get_weather_forecast(city)
            if weather_data:
                return render_template('weather.html', data=weather_data)
            return render_template('index.html', error="Could not fetch weather data. Please try again.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

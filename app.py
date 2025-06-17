from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
API_KEY = os.getenv('WEATHERAPI_KEY')
BASE_URL = "http://api.weatherapi.com/v1/current.json"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = get_weather_data(city)
    return render_template('index.html', weather=weather_data)

def get_weather_data(city):
    params = {
        'key': API_KEY,
        'q': city,
        'lang': 'ru'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if 'error' in data:
            return {'error': data['error']['message']}
        
        current = data['current']
        location = data['location']
        
        weather_info = {
            'city': location['name'],
            'country': location['country'],
            'temperature': current['temp_c'],
            'feels_like': current['feelslike_c'],
            'description': current['condition']['text'],
            'icon': current['condition']['icon'],
            'humidity': current['humidity'],
            'wind_speed': current['wind_kph'],
            'pressure': current['pressure_mb'],
            'last_updated': current['last_updated']
        }
        return weather_info
        
    except requests.exceptions.RequestException as e:
        return {'error': f'Ошибка подключения: {str(e)}'}
    except KeyError as e:
        return {'error': f'Ошибка обработки данных: {str(e)}'}

if __name__ == '__main__':
    app.run(debug=True)
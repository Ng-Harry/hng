from django.http import JsonResponse
from django.views import View
import requests

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_geolocation(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    if response.status_code == 200:
        return response.json()
    return None

def get_weather(city):
    api_key = 'b17c9d252ef540d701e24012dd51d2aa'  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['main']['temp']
    return None

class HelloView(View):
    def get(self, request):
        visitor_name = request.GET.get('visitor_name', 'Harry')
        client_ip = get_client_ip(request)
        geolocation = get_geolocation(client_ip)

        if geolocation:
            city = geolocation.get('city', 'Unknown')
            temperature = get_weather(city) if city != 'Unknown' else "Unknown"
            location = city
        else:
            location = "Unknown"
            temperature = "Unknown"

        response_data = {
            "client_ip": client_ip,
            "location": location,
            "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
        }
        return JsonResponse(response_data)

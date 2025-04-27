from django.shortcuts import render, redirect
import requests
import re
from urllib.parse import urlencode
from decouple import config



api_key = config('API_KEY')

def extract_code(text):
    match = re.search(r'\(([^)]+)\)', text)
    return match.group(1) if match else text


def get_flight_roundwaydata(origin, destination, date,return_date, children, infants, adults, cabinclass):
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-roundtrip"

    querystring = {
        "fromEntityId": origin,
        "toEntityId": destination,
        "departDate": date,
        "returnDate": return_date,
        "market": "IN",
        "currency": "INR",
        "children": children or "0",
        "infants": infants or "0",
        "cabinClass": cabinclass or "ECONOMY",
        "adults": adults or "1"
    }

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data=response.json()
    
    
 
   # Print the full URL for debugging

    try:
        return data
    except Exception as e:
        print("Error parsing API response:", e)
        return None


def get_flight_onewaydata(origin, destination, date, children, infants, adults, cabinclass):
    url = "https://sky-scanner3.p.rapidapi.com/flights/search-one-way"

    querystring = {
        "fromEntityId": origin,
        "toEntityId": destination,
        "departDate": date,
        "market": "IN",
        "currency": "INR",
        "children": children or "0",
        "infants": infants or "0",
        "cabinClass": cabinclass or "ECONOMY",
        "adults": adults or "1"
    }

    headers = {
        "x-rapidapi-key": "0cc8713fa4mshb1dd3dc18be6669p131031jsnd9d445f87b0e",
        "x-rapidapi-host": "sky-scanner3.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data=response.json()
    

    try:
        return data
    except Exception as e:
        print("Error parsing API response:", e)
        return None



def index(request):
    if request.method == 'GET' and 'origin' in request.GET:
        query_string = urlencode(request.GET)  # Converts dict to URL-encoded string
        return redirect(f'/search/?{query_string}')
    return render(request, 'index.html')



def search_flights(request):
    flights_data = None
    origin = destination = date = return_date = cabinclass = trip_type = ""
    if request.GET.get('origin') and request.GET.get('destination') and request.GET.get('date'):
        origin = extract_code(request.GET.get('origin'))
        destination = extract_code(request.GET.get('destination'))
        date = request.GET.get('date')
        children = request.GET.get('children')
        infants = request.GET.get('infants')
        adults = request.GET.get('adults')
        cabinclass = request.GET.get('cabinclass')
        return_date = request.GET.get('return_date')
        trip_type = request.GET.get('trip_type')
        if trip_type == 'roundtrip':
            # Handle round trip logic here
            flights_data = get_flight_roundwaydata(origin, destination, date, return_date, children, infants, adults, cabinclass)
        elif trip_type == 'oneway':
            # Handle one way trip logic here
            flights_data = get_flight_onewaydata(origin, destination, date, children, infants, adults, cabinclass)
        

    return render(request, 'home.html', {'flights_data': flights_data,       
        "origin": origin,
        "destination": destination,
        "date": date,
        "return_date": return_date,
        "cabinclass": cabinclass,
        "trip_type": trip_type,})

def hotel_search(request):
    if request.method == 'GET' and 'origin' in request.GET:
        query_string = urlencode(request.GET)  # Converts dict to URL-encoded string
        return redirect(f'/hotel_search/?{query_string}')
    return render(request, 'hotel_search.html')

def package_search(request):
    if request.method == 'GET' and 'origin' in request.GET:
        query_string = urlencode(request.GET)  # Converts dict to URL-encoded string
        return redirect(f'/package_search/?{query_string}')
    return render(request, 'package_search.html')


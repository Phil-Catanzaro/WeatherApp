#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:55:08 2022

@author: phillipcatanzaro
"""

import requests
from bs4 import BeautifulSoup #importing Beautiful Soup to parse html document
import json #to do deal with json data
    
apiKey = "WglGPa98rTeev9F5D4W0DbYxyGu9tj24"
zip = "41073"

#get location ID
response = requests.get("http://dataservice.accuweather.com/locations/v1/postalcodes/search?apikey=" + apiKey + "&q=" + zip)
if (response.status_code == 200): #if we reached website without error
    
    dictionary = response.json()[0] # respoonse as JSON
    #reponse.json() gives us a list with a dictionary inside, so we have to specify [0] to get the first item of the list, the dictionary itself
    locationID = dictionary["Key"]
    print("Location ID:", locationID)
    
else:
    print("API Error.")
    
    
#get weather

response = requests.get("http://dataservice.accuweather.com/currentconditions/v1/" + locationID + "?apikey=" + apiKey)
if (response.status_code == 200): #if we reached website without error
    dictionary2 = response.json()[0] # respoonse as JSON
    #reponse.json() gives us a list with a dictionary inside, so we have to specify [0] to get the first item of the list, the dictionary itself
    #temperature = dictionary2.get("Temperature.Imperial.Value")
    temperature = dictionary2["Temperature"]["Imperial"]["Value"]
    description = dictionary2["WeatherText"].title() #title() capitalizes first letter of each word in string
    print(temperature, "\N{DEGREE SIGN}F", "and", description)
    #print(temperature + "degrees Farenheit")
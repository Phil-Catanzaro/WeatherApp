#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:55:08 2022

@author: phillipcatanzaro
"""

import requests
from bs4 import BeautifulSoup #importing Beautiful Soup to parse html document
import json #to do deal with json data
from uszipcode import SearchEngine #USZipcode pacakge for zipcode to city conversions
import nltk #edit distance metrix used to test for word similarity when sanitizing city outputs 

#sanitize city/zipcode input
def checkCityZip(city):
    engine = SearchEngine()
    if (city.isalpha()): #city check
        zipcodes = engine.by_city(city=city)
        
        #using edit distance to test for similarity in closest city and the search entry
        nearestCity = zipcodes[0].major_city
        distance = nltk.edit_distance(nearestCity, city) 

        #find shorter word
        if (len(city)<len(nearestCity)):
            comparisonlength = len(city) 
        else:
            comparisonlength = len(nearestCity)
        
        #checking if distance between words is greater than length of the smallest word
        if (distance > comparisonlength):
            return False
        else:
            return True
        
    else: #zipcode check
        zipcodes = engine.by_zipcode(city)
        if (zipcodes is None): #checking to see if no matches for zipcode
            return False
        else:
            return True

    
apiKey = "e1533dfe0d2449f9ac6210053222004"
cityOrZip = "London"
if (checkCityZip(cityOrZip) == True):
    
    
    print(cityOrZip)
    
    response = requests.get("https://api.weatherapi.com/v1/current.json?key="+ apiKey + "&q=" + cityOrZip + "&aqi=no")
    if (response.status_code == 200): #if we reached website without error
        dictionary = response.json() # respoonse as JSON
        temperature = dictionary["current"]["temp_f"]
        description = dictionary["current"]["condition"]["text"].title() #title() capitalizes first letter of each word in string
        print(temperature, "\N{DEGREE SIGN}F", "and", description)
    
    else:
        print("API Error.")
    
else:
    print("Invalid city name or zip code") 
    
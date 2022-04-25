#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:55:08 2022

@author: phillipcatanzaro
"""
from flask import Flask #importing Flask class
from flask import request

import requests
from bs4 import BeautifulSoup #importing Beautiful Soup to parse html document
import json #to do deal with json data
from uszipcode import SearchEngine #USZipcode pacakge for zipcode to city conversions
import nltk #edit distance metrix used to test for word similarity when sanitizing city outputs


app = Flask(__name__) #creating flask app


 
@app.route("/") #decorator that Flask uses to connect URL endpoints with code contained in functions
def index():
    city = request.args.get("city", "")
    return (
        """<form action="" method="get">
            <input type="text" name="city" />
            <input type="submit" value="Get Temperature" />
        </form>"""
        + city 
    )
    return "Weather App."
        
@app.route("/<city>") #occurs when someone adds city parameter to url

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
        
def getTemp(city):
    apiKey = "e1533dfe0d2449f9ac6210053222004"
    if (checkCityZip(cityOrZip) == True):
        response = requests.get("https://api.weatherapi.com/v1/current.json?key="+ apiKey + "&q=" + city + "&aqi=no")
        if (response.status_code == 200): #if we reached website without error
            dictionary = response.json() # respoonse as JSON
            temperature = dictionary["current"]["temp_f"]
            description = dictionary["current"]["condition"]["text"].title() #title() capitalizes first letter of each word in string
            return(str(temperature))        
        else:
            return "API Error"
    
    else:
        return "Invalid city name or zip code"

if __name__ == "__main__":
    cityOrZip = input("Enter City or Zip Code: ")
    print(getTemp(cityOrZip)[0], "\N{DEGREE SIGN}F", "and", getTemp(cityOrZip)[1])

    
    
#two lines below tell Python to start Flask development server when script is exeucted fromcommand line
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

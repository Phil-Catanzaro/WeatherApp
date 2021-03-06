#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 16:55:08 2022

@author: phillipcatanzaro
"""
from flask import Flask, render_template #importing Flask class and render_template for html templates
from flask import request

import requests
from bs4 import BeautifulSoup #importing Beautiful Soup to parse html document
import json #to do deal with json data
from uszipcode import SearchEngine #USZipcode pacakge for zipcode to city conversions
import nltk #edit distance metrix used to test for word similarity when sanitizing city outputs


app = Flask(__name__) #creating flask app
 
@app.route("/") #decorator that Flask uses to connect URL endpoints with code contained in functions
def weather_form():
    return render_template('home.html')


@app.route("/", methods=["POST"]) #occurs when city parameter is added to url
def weather_form_post():
    zipOrCity = request.form.get("city") #gets text from inputted form
    location = zipOrCity.capitalize() #nicely capitalized name for use in weather-form.html template
    zipOrCity = zipOrCity.strip() #stripping spaces from text
    
    apiKey = "e1533dfe0d2449f9ac6210053222004"
    if (checkCityZip(zipOrCity) == True):
        response = requests.get("https://api.weatherapi.com/v1/current.json?key="+ apiKey + "&q=" + zipOrCity + "&aqi=no")
        if (response.status_code == 200): #if we reached website without error
            dictionary = response.json() # respoonse as JSON
            city = dictionary["location"]["name"]
            region = dictionary["location"]["region"]
            temperature = dictionary["current"]["temp_f"]
            feelsLike = dictionary["current"]["feelslike_f"]
            description = dictionary["current"]["condition"]["text"].title() #title() capitalizes first letter of each word in string
            icon = dictionary["current"]["condition"]["icon"] 

            return render_template('weather-form.html', temperature = temperature, feelsLike = feelsLike, city = city, region = region, icon=icon)
        else:
            return "API Error"
    
    else:
        return render_template('invalid.html')
    "Invalid city name or zip code"
    

#issue with two named cities (Washington DC, Fort worth, Kansas city, etc..)
def checkCityZip(zipOrCity):
    engine = SearchEngine()
    
    if (zipOrCity == ""): #if nothing was inputted
        return False
    if ((zipOrCity[0]).isalpha()): #city check  
        #checking first word of city to see if its a zipcode or city
        print(zipOrCity)
        zipcodes = engine.by_city(city=zipOrCity)
        
        #using edit distance to test for similarity in closest city and the search entry
        try:
            nearestCity = zipcodes[0].major_city
            distance = nltk.edit_distance(nearestCity, zipOrCity) 
    
            #find shorter word
            if (len(zipOrCity)<len(nearestCity)):
                comparisonlength = len(zipOrCity) 
            else:
                comparisonlength = len(nearestCity)
            
            #checking if distance between words is greater than length of the smallest word
            if (distance > comparisonlength):
                return False
            else:
                return True
        except:
            return False
        
    else: #zipcode check
        zipcodes = engine.by_zipcode(zipOrCity)

        if (zipcodes is None): #checking to see if no matches for zipcode
            return False
        else:
            return True
    
#two lines below tell Python to start Flask development server when script is exeucted fromcommand line
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

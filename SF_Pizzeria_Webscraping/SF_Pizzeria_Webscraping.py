# %%
import pymongo
from pymongo import MongoClient
import requests
import re
import json
import http.client
import urllib.parse
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time

# %% [markdown]
# Search on yellowpages.com for the top 30 “Pizzeria” in San Francisco. Save the search result page to disk, “sf_pizzeria_search_page.htm”.

# %%
def DownloadPages():
    try:
        # Set the URL
        my_headers = {"user-agent": "Mozilla/5.0"}
        URL = "https://www.yellowpages.com/search?"

        # Specify search terms and location
        terms = {
            "search_terms": "Pizzeria",
            "geo_location_terms" : "San Francisco",
            "sort" : "default",
            "page" : "1"
        }

        # Use get to search
        res = requests.get(URL, 
                        params = terms,
                        headers = my_headers,
                        timeout = 15)

        time.sleep(10)

        with open("sf_pizzeria_search_page.htm", "w+", encoding = 'utf-8') as file:
            file.write(res.text)
    except:
        print("Problem with the connection...")

# %% [markdown]
# Opens the search result page and parses out all shop information (search rank, name, linked URL [this store’s YP URL], star rating If It Exists, number of reviews IIE, TripAdvisor rating IIE, number of TA reviews IIE, “$” signs IIE, years in business IIE, review IIE, and amenities IIE). And skip all “Ad” results.

# %%
def PizzaInfo():
    try:
        # Open the html
        HTMLFileToBeOpened = open("sf_pizzeria_search_page.htm", "r")
        contents = HTMLFileToBeOpened.read()
        soup = BeautifulSoup(contents, 'lxml')

        # Skip Ad result
        containers = soup.find_all("div", {"class" : "result"})

        # Search in each container
        for pizza in containers:
            title = pizza.find("h2", {"class" : "n"}).text
            if bool(re.findall(r'[0-9]+', title)):
                # Search Rank
                title = pizza.find("h2", {"class" : "n"}).text
                rank = re.findall(r'[0-9]+', title)[0]
                print(rank)
                # Name
                name = pizza.find("a", {"class" : "business-name"}).text
                print(name)
                # URL
                url = pizza.select_one("h2.n > a[href]")["href"]
                print(url)
                # star ratings
                if bool(pizza.find("a", {"class" : "rating hasExtraRating"})):
                    star_rating = pizza.select_one("a.rating div.result-rating")
                    print(star_rating.get("class")[1])
                # number of star ratings reviews
                    review = pizza.select_one("a.rating.hasExtraRating span.count").text
                    print(review)
                # TA ratings
                if bool(pizza.find("div", {"class" : "ratings"}).get("data-tripadvisor")):
                    TArating_raw = pizza.find("div", {"class" : "ratings"})["data-tripadvisor"]
                    TArating = json.loads(TArating_raw)["rating"]
                    print(TArating)
                # number of TA reviews
                    NTArating = json.loads(TArating_raw)["count"]
                    print(NTArating)
                # price
                if bool(pizza.find("div", {"class" : "price-range"})):
                    price = pizza.find("div", {"class" : "price-range"}).text
                    print(price)
                # years in business
                if bool(pizza.find("div", {"class" : "years-in-business"})):
                    yrs = pizza.find("div", {"class" : "number"}).text
                    print(yrs)
                # Text Reviews
                if bool(pizza.find("div", {"class" : "snippet"})):
                    text_review = pizza.find("div", {"class" : "snippet"}).text
                    print(text_review)
                # Amenities
                if bool(pizza.find("div", {"class" : "amenities-info"})):
                    amenities = pizza.find("div", {"class" : "amenities-info"}).text
                    print(amenities)
    except:
        print("Problem with the connection...")

# %% [markdown]
# Create a MongoDB collection called “sf_pizzerias” that stores all the extracted shop information, one document for each shop.

# %%
def MongoDB():
    try:
        # Connect to MongoDB server
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        # Access database and collection
        db = client["Pizza_Info"]
        collection = db["sf_pizzerias"]

        # Open the html
        HTMLFileToBeOpened = open("sf_pizzeria_search_page.htm", "r")
        contents = HTMLFileToBeOpened.read()
        soup = BeautifulSoup(contents, 'lxml')

        # Search in each container
        containers = soup.find_all("div", {"class" : "result"})
        list = []
        for pizza in containers:
            dict = {"Search Rank": [], "Name" : [], "URL" : [], "Star Rating" : [], "Number of reviews" : [], "TripAdvisor rating" : [], "Number of TripAdvisor rating" : [], "How expensive" : [], "Years in Business" : [], "Review" : [], "Amenities": []}
            title = pizza.find("h2", {"class" : "n"}).text
            # Skip Ad result
            if bool(re.findall(r'[0-9]+', title)):
                # Search Rank
                title = pizza.find("h2", {"class" : "n"}).text
                rank = re.findall(r'[0-9]+', title)[0]
                dict["Search Rank"] = rank
                # Name
                name = pizza.find("a", {"class" : "business-name"}).text
                dict["Name"] = name
                # URL
                url = pizza.select_one("h2.n > a[href]")["href"]
                dict["URL"] = url
                # star ratings
                if bool(pizza.find("a", {"class" : "rating hasExtraRating"})):
                    star_rating = pizza.select_one("a.rating div.result-rating")
                    dict["Star Rating"] = star_rating.get("class")[1]
                # number of star ratings reviews
                    review = pizza.select_one("a.rating.hasExtraRating span.count").text
                    dict["Number of reviews"] = review
                # TA ratings
                if bool(pizza.find("div", {"class" : "ratings"}).get("data-tripadvisor")):
                    TArating_raw = pizza.find("div", {"class" : "ratings"})["data-tripadvisor"]
                    TArating = json.loads(TArating_raw)["rating"]
                    dict["TripAdvisor rating"] = TArating
                # number of TA reviews
                    NTArating = json.loads(TArating_raw)["count"]
                    dict["Number of TripAdvisor rating"] = NTArating
                # price
                if bool(pizza.find("div", {"class" : "price-range"})):
                    price = pizza.find("div", {"class" : "price-range"}).text
                    dict["How expensive"] = price
                # years in business
                if bool(pizza.find("div", {"class" : "years-in-business"})):
                    yrs = pizza.find("div", {"class" : "number"}).text
                    dict["Years in Business"] = yrs
                # Text Reviews
                if bool(pizza.find("div", {"class" : "snippet"})):
                    text_review = pizza.find("div", {"class" : "snippet"}).text
                    dict["Review"] = text_review
                # Amenties
                if bool(pizza.find("div", {"class" : "amenities-info"})):
                    amenities = pizza.find("div", {"class" : "amenities-info"}).text
                    dict["Amenities"] = amenities
                list.append(dict)
                
        # Insert data to mongodb
        collection.insert_many(list)
    except:
        print("Problem with the connection...")

# %% [markdown]
# Reads all URLs stored in “sf_pizzerias” and download each shop page.  Store the page to disk, “sf_pizzerias_[Search Rank].htm” 

# %%
def ReadURL():
    try:
        # Connect to MongoDB server
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        # Access database and collection
        db = client["Pizza_Info"]
        collection = db["sf_pizzerias"]

        # Read the data
        url = collection.find({},{"_id" : 0, "URL":1, "Search Rank" : 1})

        # Base URL
        base = "https://www.yellowpages.com"

        # Iterate through URL list
        for i in url:
            # Go to the page
            res = requests.get(base + i["URL"], 
                        headers = {"user-agent": "Mozilla/5.0"},
                        timeout = 15)
            # Store the page
            with open("sf_pizzerias" + i["Search Rank"] + ".htm", "w+", encoding = 'utf-8') as file:
                file.write(res.text)
            time.sleep(5)

    except:
        print("Problem with the connection...")

# %% [markdown]
# Reads the 30 shop pages and parses each shop’s address, phone number, and website.

# %%
def PizzaMoreInfo():
    try:
        # Open html file 
        for i in range (1, 31):
            HTMLFileToBeOpened = open("sf_pizzerias" + str(i) + ".htm", "r")
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'lxml')
            # Address
            if bool(soup.find("span", {"class" : "address"})):
                address = soup.select_one("span.address").get_text(separator = ' ', strip = True)
                print(address)
            # Phone
            if bool(soup.find("a", {"class" : "phone dockable"})):
                phone = soup.find("a", {"class" : "phone dockable"}).text
                print(phone)
            # Website
            if bool(soup.find("a", {"class": "website-link dockable"})):
                web = soup.select_one("a.website-link.dockable")["href"]
                print(web)
    except:
        print("Problem with the connection...")

# %% [markdown]
# 9.  Modify the code to query each shop address’ geolocation on positionstack.com.  Update each shop document on the MongoDB collection “sf_pizzerias” to contain the shop’s address, phone number, website, and geolocation.

# %%
def GeoLocation():
    try:
        # Connect to MongoDB server
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        # Access database and collection
        db = client["Pizza_Info"]
        collection = db["sf_pizzerias"]

        # Create a list to store dictionaries
        list = []

        # Loop through each shop and store required information
        for i in range (1, 31):
            # Open html file
            with open("sf_pizzerias" + str(i) + ".htm", "r") as file:
                contents = file.read()
            soup = BeautifulSoup(contents, 'lxml')
            # Create a dictionary
            dict = {"Name" : "", "Address" : "",  "Latitude" : "", "Longitude" : "","Phone Number" : "", "Website" : ""}
            # Name
            name = soup.find("h1", {"class" : "dockable business-name"}).text
            dict["Name"] = name
            # Address
            if bool(soup.find("span", {"class" : "address"})):
                address = soup.select_one("span.address").get_text(separator = ' ', strip = True)
                dict["Address"] = address
                conn = http.client.HTTPConnection('api.positionstack.com')
                params = urllib.parse.urlencode({
                    'access_key': 'your_access_key',
                    'query': address,
                    'output': 'json',
                    'limit': 1,})
                conn.request('GET', '/v1/forward?{}'.format(params), headers={"User-Agent": "Mozilla/5.0"})
                res = conn.getresponse()
                data = res.read()
                json_data = json.loads(data)
                if json_data["data"]:
                    dict["Latitude"] = json_data["data"][0]["latitude"]
                    dict["Longitude"] = json_data["data"][0]["longitude"]
            # Phone
            if bool(soup.find("a", {"class" : "phone dockable"})):
                phone = soup.find("a", {"class" : "phone dockable"}).text
                dict["Phone Number"] = phone
            # Website
            if bool(soup.find("a", {"class": "website-link dockable"})):
                web = soup.select_one("a.website-link.dockable")["href"]
                dict["Website"] = web
            list.append(dict)
            time.sleep(5)

        # Update data to mongodb
        for info in list:
            collection.update_many({"Name" : info["Name"]}, {"$set" : info})
    except:
        print("Problem with the connection...")

# %%
if __name__ == '__main__':
	DownloadPages()
	PizzaInfo()
	MongoDB()
	ReadURL()
	PizzaMoreInfo()
	GeoLocation()

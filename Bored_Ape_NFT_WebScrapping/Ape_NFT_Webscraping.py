# %%
import pymongo
from pymongo import MongoClient
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# %% [markdown]
# Access all apes with “Solid gold” fur and sort them “Price high to low”, click on each of the top-8 most expensive Bored Apes, and store the resulting details page to disk, “bayc_[N].htm”.

# %%
def DownloadPages():
    try:
        driver = webdriver.Chrome(service=Service('chromedriver_mac64'))
        driver.implicitly_wait(10)
        driver.set_script_timeout(120)
        driver.set_page_load_timeout(10)

        # Get the web
        
        for i in range(0, 8):
            driver.get("https://opensea.io/collection/boredapeyachtclub?search%5BsortAscending%5D=false&search%5BstringTraits%5D%5B0%5D%5Bname%5D=Fur&search%5BstringTraits%5D%5B0%5D%5Bvalues%5D%5B0%5D=Solid%20Gold");
        # click
            time.sleep(15)
            item = driver.find_elements(By.CLASS_NAME, "sc-1f719d57-0.fKAlPV.Asset--anchor")[i]
            item.click()
            content = driver.page_source
            time.sleep(15)
            with open("bayc_" + str(i+1) + ".htm", "w+", encoding = 'utf-8') as file:
                file.write(content)
            time.sleep(15)

        driver.quit()
    except:
        print("Not enough sleep...")

# %% [markdown]
# Go through all 8 htm files and stores each ape’s number and all its attributes in a document inside a MongoDB collection called “bayc”.

# %%
def MongoDB():
    try:
        # connect to MongoDB server
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        # access database and collection
        db = client["monkeys_nft"]
        collection = db["bayc"]

        # Scrape and insert data to mongodb
        list = []

        for i in range(0, 8):
            # Create an attribute list to store different number of attributes
            attribute_list = []
            # Create a dictionary to store names and attributes
            dict = {"Name": [], "Attributes" : []}
            # Open html file
            HTMLFileToBeOpened = open("bayc_" + str(i+1) + ".htm", "r")
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'html.parser')
            # Scrape required information and store them
            name = soup.select("h1.sc-29427738-0.hKCSVX.item--title")
            dict["Name"] = name[0].text
            attributes_property = soup.select("div.sc-d6dd8af3-0.hkmmpQ.item--property div.Property--type")
            attributes_value = soup.select("div.sc-d6dd8af3-0.hkmmpQ.item--property div.Property--value")
            num_of_attributes = len(attributes_property)
            for i in range(0, num_of_attributes):
                attribute_list.append(attributes_property[i].text)
                attribute_list.append(attributes_value[i].text)
            dict["Attributes"] = attribute_list
            # Append each dictionary to a list
            list.append(dict)

        # Insert data to mongodb
        collection.insert_many(list)
    except:
        print("Problem with the connection...")

# %%
if __name__ == '__main__':
	DownloadPages()
	MongoDB()
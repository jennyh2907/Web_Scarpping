# %%
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import re
import pandas as pd

# %% [markdown]
# Connect to eBay, loads eBay's search result page containing sold "amazon gift card"
# Save the result to file

# %%
def AmzGiftCard():
	try:
		my_headers = {'User-Agent': 'Mozilla/5.0'}
		url = requests.get('https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&LH_Sold=1', headers=my_headers) 
		soup = BeautifulSoup(url.content) 
		with open("amazon_gift_card_01.htm", "w+", encoding = 'utf-8') as file:
			file.write(str(soup.prettify()))
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	AmzGiftCard()

# %% [markdown]
# Download the first 10 pages of search results

# %%
def AmzGiftCardDownload():
        try:
            my_headers = {'User-Agent': 'Mozilla/5.0'}
            for i in range(1, 11):
                 url= "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&LH_Sold=1&_pgn=" + str(i)
                 page = requests.get(url, headers=my_headers)
                 soup = BeautifulSoup(page.text, 'lxml')
            with open("amazon_gift_card_" + str(i) + ".htm", "w+", encoding = 'utf-8') as file:
                file.write(str(soup.prettify()))
            time.sleep(10)
        except:
             print("Problem with the connection...")

if __name__ == '__main__':
	AmzGiftCardDownload()

# %% [markdown]
# Loop through the downloaded pages, opens and parses them to a Python object

# %%
def ParseToObject():
    try:
        for i in range(1, 11):
            HTMLFileToBeOpened = open("amazon_gift_card_" + str(i) + ".htm", "r")
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'lxml')
    except:
        print("Problem with the connection...")

if __name__ == '__main__':
	ParseToObject()

# %% [markdown]
# Identify and print to screen the title, price, and shipping price of each item.

# %%
def ProductInfo():
    try:
        for i in range(1, 11):
            HTMLFileToBeOpened = open("amazon_gift_card_" + str(i) + ".htm", "r")
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'lxml')
            prod_info = soup.find("div", {"class" : "srp-river-results clearfix"})
            containers = prod_info.find_all("div", {"class" : "s-item__wrapper clearfix"})
            for container in containers:
                title = (container.find("div", {"class" : "s-item__title"})).text
                if "New Listing" in title:
                    title = title.replace("New Listing", "") 
                    print(title)
                else: 
                    print(title)
                price = (container.find("span", {"class" : "s-item__price"})).text
                print(price)
                if (container.find("span", {"class" : "s-item__shipping s-item__logisticsCost"})) is not None:
                    shipping = container.find("span", {"class" : "s-item__shipping s-item__logisticsCost"}).text
                    print(shipping)
                else:
                    print("Free shipping")
        time.sleep(10)
    except:
        print("Problem with the connection...")

if __name__ == '__main__':
	ProductInfo()

# %% [markdown]
# Using RegEx, identify and print to screen gift cards that sold above face value
# Compare a gift card’s value to its price + shipping (free shipping as 0).  If value < price + shipping, then a gift card sells above face value.

# %%
def AboveFaceValue():
    try:
        counter = 0
        counter2 = 0
        for i in range(1, 11):
            HTMLFileToBeOpened = open("amazon_gift_card_" + str(i) + ".htm", "r")
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'lxml')
            prod_info = soup.find("div", {"class" : "srp-river-results clearfix"})
            containers = prod_info.find_all("div", {"class" : "s-item__wrapper clearfix"})
            for container in containers:
                # Extract value in title
                title = (container.find("div", {"class" : "s-item__title"})).text
                dollar_value = re.findall(r'[0-9]+', title)
                title_value = [float(n) for n in dollar_value]
                if bool(title_value):
                    final_title_value = title_value[0] # First value in title
                    # print(final_title_value)
                else:
                    final_title_value = 0
                    # print(final_title_value)
         
                # Extract price
                price = (container.find("span", {"class" : "s-item__price"})).text
                num_price = [float(n) for n in re.findall(r'([0-9.]+)', price)]
                final_price = num_price[0]
                # print(final_price)

                # Extract shipping cost
                if (container.find("span", {"class" : "s-item__shipping s-item__logisticsCost"})) is not None:
                    shipping = container.find("span", {"class" : "s-item__shipping s-item__logisticsCost"}).text
                    if (shipping.strip() == "Free shipping"):
                        final_shipping = 0
                        # print(final_shipping)
                    else:
                        num_shipping = [float(n) for n in re.findall(r'([0-9.]+)', shipping)]
                        final_shipping = num_shipping[0]
                        # print(num_shipping[0])
                else:
                    final_shipping = 0
                    # print(final_shipping)

                # Sum price and shipping cost, compare value of cost
                if (final_price + final_shipping < final_title_value):
                    counter = counter + 1
                    if "New Listing" in title:
                        title = title.replace("New Listing", "") 
                    print(title.strip())
                else:
                    counter2 = counter2 + 1
        print(counter)
        print(counter2)
        print(counter/(counter+counter2))
    except:
        print("Problem with the connection...")

if __name__ == '__main__':
	AboveFaceValue()


# %% [markdown]
# Business Problem: What fraction of Amazon gift cards sells above face value? Why is this the case?
# About 50% of Amazon gift cards sells above face value. The most common reason for seller to assign a face value that is below price + shipping cost is to attract more careless customers to at least view or even buy their product. 

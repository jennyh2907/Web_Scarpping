# %%
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import re
import pandas as pd

# %% [markdown]
# 1. Use the URL identified above and write code that loads eBay's search result page containing sold "amazon gift card". Save the result to file. Give the file the filename "amazon_gift_card_01.htm".

# %%
def main():
	try:
		my_headers = {'User-Agent': 'Mozilla/5.0'}
		url = requests.get('https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&LH_Sold=1', headers=my_headers) 
		soup = BeautifulSoup(url.content) 
		with open("amazon_gift_card_01.htm", "w+", encoding = 'utf-8') as file:
			file.write(str(soup.prettify()))
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	main()

# %% [markdown]
# 2. Take your code in (a) and write a loop that will download the first 10 pages of search results. Save each of these pages to "amazon_gift_card_XX.htm" (XX = page number). IMPORTANT: each page request needs to be followed by a 10 second pause.  Please remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.

# %%
def main():
	try:
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
	main()

# %% [markdown]
# 3. Write code that loops through the pages you downloaded in (b), opens and parses them to a Python or Java xxxxsoup-object.

# %%
def main():
    try:
        for i in range(1, 11):
            HTMLFileToBeOpened = open("amazon_gift_card_" + str(i) + ".htm", "r")
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'lxml')
    except:
        print("Problem with the connection...")

if __name__ == '__main__':
	main()

# %% [markdown]
# 4. Using your code in (c) and your answer to 1 (g), identify and print to screen the title, price, and shipping price of each item.

# %%
def main():
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
	main()

# %% [markdown]
# 5. Using RegEx, identify and print to screen gift cards that sold above face value. e., use RegEx to extract the value of a gift card from its title when possible (doesn’t need to work on all titles, > 90% success rate if sufficient). Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  If value < price + shipping, then a gift card sells above face value.

# %%
def main():
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
	main()


# %% [markdown]
# 6.What fraction of Amazon gift cards sells above face value? Why do you think this is the case?


# %% [markdown]
# About 50% of Amazon gift cards sells above face value. The most common reason for seller to assign a face value that is below price + shipping cost is to attract more careless customers to at least view or even buy their product. 

# %% [markdown]
# Part 2.
# 
# Following the steps we discussed in class and write code that automatically logs into the website fctables.com.
# 
# Verify that you have successfully logged in:  use the cookies you received during log in and write code to access https://www.fctables.com/tipster/my_bets/ Links to an external site..  Check whether the word “Wolfsburg” appears on the page.  Don’t look for your username to confirm that you are logged in (it won’t work) and use this page’s content instead.

# %%
def main():
    try:
        
        URL = "https://www.fctables.com/user/login/"
        URL_bet = "https://www.fctables.com/tipster/my_bets/"
        session_requests = requests.session()
        res = session_requests.post(URL, 
                                data = {"login_username":"hcwhuang",
                                        "login_password":"hcwhuang29",
                                        "user_remeber":"1",
                                        "login_action":"1"},
                                    headers = dict(referer = "https://www.fctables.com/"),
                                timeout = 15)
        cookies = session_requests.cookies.get_dict()
        page2 = session_requests.get(URL_bet,  
                                      cookies=cookies)        
        doc2 = BeautifulSoup(page2.content, 'html.parser')
        
        # Check if Wolfsburg exists
        if 'Wolfsburg' in doc2.text:
            print ('Yes')
        else:
            print ('No')

    except Exception as ex:
        print('error: ' + str(ex))

if __name__ == '__main__':
    main()



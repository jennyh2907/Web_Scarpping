# %%
from bs4 import BeautifulSoup
import requests
import urllib.request
import time
import re
import pandas as pd

# %% [markdown]
# Connect to Barnes & Noble, loads the first page with 40 items per page of “B&N Top 100”.

# %%
my_headers = {'User-Agent': 'Mozilla/5.0'}
url = requests.get('https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1', headers=my_headers) 
soup = BeautifulSoup(url.content) 
print(soup.prettify()) 

# %% [markdown]
# Create a list of each book’s product page URL (his list should be of length 40)

# %%
url_list = []
def List_URL():
	try:
		url= "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1"
		my_headers = {'User-Agent': 'Mozilla/5.0'}
		landing_page = requests.get('https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1', headers=my_headers) 
		page = requests.get(url, headers=my_headers)
		# Create a beautifulsoup object 
		soup = BeautifulSoup(page.text, 'lxml')
		list_of_contents = soup.select("div.product-shelf-title h3.product-info-title > a[href]")
		# prints the HTML content to the screen (almost only text here
		# just need to replaces "&nbsp;" with " ")
		for link in list_of_contents:
			tags = soup.find_all("a")
			data = link.get('href')
			url_list.append(data)
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	List_URL()

print(url_list)

# %% [markdown]
# Write a loop that downloads each product page of the top 40 books in “B&N Top 100”

# %%
def prepend(list, str):
    str += '{0}'
    list = [str.format(i) for i in list]
    return(list)

url_list = prepend(url_list, "https://www.barnesandnoble.com")

print(url_list)

def PageDownload():
	try:
		for i in range(1, 41):
			url= url_list[i-1]
			page = requests.get(url, headers=my_headers)
			soup = BeautifulSoup(page.text, 'lxml')
			with open("bn_top100_" + str(i) + ".htm", "w+", encoding = 'utf-8') as file:
				file.write(str(soup.prettify()))
			time.sleep(5)
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	PageDownload()


# %% [markdown]
# Loop through the downloaded pages, opens and parses them 
# Access the “Overview” section of the page and print the first 100 characters of the overview text to screen.

# %%
chars = []
def Hundred_Char():
    try:
        for i in range(1, 41):
            chars = []
            url= url_list[i-1]
            HTMLFileToBeOpened = open("bn_top100_" + str(i) + ".htm", "r")
            contents = HTMLFileToBeOpened.read()
            soup = BeautifulSoup(contents, 'lxml')
            list_of_contents = soup.select("div.bs-content")
            for i in list_of_contents:
                split = re.findall(r'([A-Za-z0-9])', i.text)
                left_char = 100 - len(chars)
                find = len(split)
                for i in range(min(find, left_char)):
                    chars.append(split[i])
                if len(chars) == 100:
                    print(chars)
                    break
        time.sleep(5)
    except:
        print("Problem with the connection...")

if __name__ == '__main__':
	Hundred_Char()

print(chars)
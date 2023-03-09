# %%
from bs4 import BeautifulSoup
import requests
import re
import urllib.request

# %% [markdown]
# Access TigerDirect product page

# %%
my_headers = {'User-Agent': 'Mozilla/5.0'}
url = requests.get('https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390', headers=my_headers) 
soup = BeautifulSoup(url.content) 
print(soup.prettify()) 

# %% [markdown]
# Access the list price and current price

# %%
def ListAndCurrent():
	try:
		url= "https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390"
		my_headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(url, headers=my_headers)
		# Create a beautifulsoup object 
		soup = BeautifulSoup(page.text, 'lxml')
		# find <p> that immediately follows <div> of class "col-md-6.
		list_of_contents = soup.select("p.list-price span.sr-only")
		list_of_contents_2 = soup.select("p.final-price span.sr-only")
		# prints the HTML content to the screen (almost only text here
		# just need to replaces "&nbsp;" with " ")
		for i in list_of_contents:
			a = i.text
			print(i.text)
		
		for i in list_of_contents_2:
			b = i.text
			print(i.text)
		
		return a, b
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	ListAndCurrent()

# %% [markdown]
# Store the prices to strings

# %%
def convertTuple(tup):
    str = ''.join(tup)
    return str

str = convertTuple(ListAndCurrent())
print(str)

# %% [markdown]
# Use regex to convert the prices to thr format like "1234.56"

# %%
temp1 = re.sub(r"and ", ".", str)
temp2 = re.sub(r"[$,\r\n ]+", "", temp1)
temp3 = re.sub(r"[a-z]+", "\n", temp2)
print(temp3)

# %% [markdown]
# Print both list price and the current price to screen

# %%
print(temp3)
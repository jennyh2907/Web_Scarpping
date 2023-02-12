# %%
from bs4 import BeautifulSoup
import requests
import re
import urllib.request

# %% [markdown]
# 1. load https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390

# %%
my_headers = {'User-Agent': 'Mozilla/5.0'}
url = requests.get('https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390', headers=my_headers) 
soup = BeautifulSoup(url.content) 
print(soup.prettify()) 

# %% [markdown]
# 2. Use your browser's development tools to find a unique way to access its list price and its current price. What do you choose? Please remember, you can choose multiple selectors to get where you want to be. E.g., you may choose to select "span.class1 p.class2" to select the "p" of class "class2" inside of the "span" of class "class1".

# %%
def main():
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
	main()



# %% [markdown]
# 3. store the prices to strings.

# %%
def convertTuple(tup):
    str = ''.join(tup)
    return str

str = convertTuple(main())
print(str)

# %% [markdown]
# 4. Use Python's (or Java's) regex (!!) functionality to convert the prices to "1234.56" (no dollar sign, comma, just a "." separator for cents)

# %%
temp1 = re.sub(r"and ", ".", str)
temp2 = re.sub(r"[$,\r\n ]+", "", temp1)
temp3 = re.sub(r"[a-z]+", "\n", temp2)
print(temp3)

# %% [markdown]
# 5. print both, the list price and the current price to screen / terminal 

# %%
print(temp3)

# %% [markdown]
# 6. Write code that loads "https://www.usnews.com/"

# %%
my_headers = {'User-Agent': 'Mozilla/5.0'}
url = requests.get('https://www.usnews.com/', headers=my_headers) 
soup = BeautifulSoup(url.content) 
print(soup.prettify()) 

# %% [markdown]
# 7. "finds" its current "Top Stories" (do not hard-code it's URL!) (You may use your browser's dev tools to find a functioning way to access all the "Top Stories" and then implement the access to them in your code.)

# %%
def main():
	try:
		url= "https://www.usnews.com/"
		my_headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(url, headers=my_headers)
		# Create a beautifulsoup object
		soup = BeautifulSoup(page.text, 'lxml')
		# find <p> that immediately follows <div> of class "col-md-6.
		list_of_contents = soup.select("div.Box-w0dun1-0.ArmRestTopStories__Part-s0vo7p-1.erkdnc.biVKSR h3.Heading-sc-1w5xk2o-0.ContentBox__StoryHeading-sc-1egb8dt-3.MRvpF.fqJuKa.story-headline > a[href]")
		# list_of_contents_2 = soup.select("div.Box-w0dun1-0.MediaLink__Content-sc-4j1zsn-0.dWWnRo.cJCmtT p.Paragraph-sc-1iyax29-0.gHMBuC")
		# prints the HTML content to the screen (almost only text here
		# just need to replaces "&nbsp;" with " ")
		for i in list_of_contents:
			a = i.text
			print(i.text)
		
		# for i in list_of_contents_2:
		#	b = i.text
		#	print(i.text)
		
		return a
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	main()

# %% [markdown]
# 8. read + print the URL of the _second_ current top story to the screen (terminal)

# %%
url_list = []
def main():
	try:
		url= "https://www.usnews.com/"
		my_headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(url, headers=my_headers)
		# Create a beautifulsoup object
		soup = BeautifulSoup(page.text, 'lxml')
		# find <p> that immediately follows <div> of class "col-md-6.
		list_of_contents = soup.select("div.Box-w0dun1-0.ArmRestTopStories__Part-s0vo7p-1.erkdnc.biVKSR h3.Heading-sc-1w5xk2o-0.ContentBox__StoryHeading-sc-1egb8dt-3.MRvpF.fqJuKa.story-headline > a[href]")
		# prints the HTML content to the screen (almost only text here
		# just need to replaces "&nbsp;" with " ")
		for link in list_of_contents:
			tags = soup.find_all("a")
			data = link.get('href')
			url_list.append(data)
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	main()

print(url_list[1])

# %% [markdown]
# 9. load that page

# %%
my_headers = {'User-Agent': 'Mozilla/5.0'}
url = requests.get(url_list[1], headers=my_headers) 
soup = BeautifulSoup(url.content) 
print(soup.prettify()) 

# %% [markdown]
# 10. read + print the header as well as the first 3 sentences of the main body to the screen

# %%
sentences = []
def main():
	try:
		url= url_list[1]
		my_headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(url, headers=my_headers)
		# Create a beautifulsoup object
		soup = BeautifulSoup(page.text, 'lxml')
		# find <p> that immediately follows <div> of class "col-md-6.
		list_of_contents = soup.select("h1.Heading-sc-1w5xk2o-0.iQhOvV")
		list_of_contents_2 = soup.select("div.Box-w0dun1-0.article-body__ArticleBox-sc-138p7q2-2.dWWnRo.eYFKbH div.Raw-slyvem-0.bCYKCn")
		# prints the HTML content to the screen (almost only text here
		# just need to replaces "&nbsp;" with " ")
		for i in list_of_contents:
			a = i.text
			print(i.text)
		for i in list_of_contents_2:
			split = re.findall(r'(.+?[.!](?:0-9| |$))', i.text)
			left_sen = 3 - len(sentences)
			find = len(split)
			for i in range(min(find, left_sen)):
				sentences.append(split[i])
			if len(sentences) == 3:
				break
		return a
	except:
		print("Problem with the connection...")

if __name__ == '__main__':
	main()

print(sentences)



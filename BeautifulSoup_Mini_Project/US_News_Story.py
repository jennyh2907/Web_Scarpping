# %%
from bs4 import BeautifulSoup
import requests
import re
import urllib.request

# %% [markdown]
# Loads "https://www.usnews.com/"

# %%
my_headers = {'User-Agent': 'Mozilla/5.0'}
url = requests.get('https://www.usnews.com/', headers=my_headers) 
soup = BeautifulSoup(url.content) 
print(soup.prettify()) 

# %% [markdown]
# Find its current "Top Stories" 

# %%
def TopStory():
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
	TopStory()

# %% [markdown]
# Read + print the URL of the _second_ current top story to the screen

# %%
url_list = []
def SecondStory():
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
	SecondStory()

print(url_list[1])

# %% [markdown]
# Load that page

# %%
my_headers = {'User-Agent': 'Mozilla/5.0'}
url = requests.get(url_list[1], headers=my_headers) 
soup = BeautifulSoup(url.content) 
print(soup.prettify()) 

# %% [markdown]
# Read + print the header as well as the first 3 sentences of the main body to the screen

# %%
sentences = []
def TitleAndThreeLines():
	try:
		url= url_list[1]
		my_headers = {'User-Agent': 'Mozilla/5.0'}
		page = requests.get(url, headers=my_headers)
		# Create a beautifulsoup object
		soup = BeautifulSoup(page.text, 'lxml')
		# find <p> that immediately follows <div> of class "col-md-6.
		list_of_contents = soup.select("h1.Heading-sc-1w5xk2o-0.iQhOvV")
		list_of_contents_2 = soup.select("div.Box-w0dun1-0.article-body__ArticleBox-sc-138p7q2-2.dWWnRo.eYFKbH div.Raw-slyvem-0.bCYKCn")
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
	TitleAndThreeLines()

print(sentences)



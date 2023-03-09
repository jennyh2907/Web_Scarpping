# %%
from bs4 import BeautifulSoup
import requests
import time

# %% [markdown]
# Access https://www.planespotters.net/user/login. Read and store the cookies received.

# %%
# Access the page
URL = "https://www.planespotters.net/user/login"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'
my_headers = {"user-agent": user_agent}

# Request the session
session_requests = requests.session()
page1 = session_requests.get(URL, headers = my_headers)
doc1 = BeautifulSoup(page1.content, 'html.parser')

# Extract required hidden values
token = doc1.select("div.planespotters-form input[name=csrf]")[0];
csrf = token.get("value")
print("csrf:", csrf)
time.sleep(5)

# Request a session
get_cookie = session_requests.cookies.get_dict()
print("cookie:", get_cookie)


# %% [markdown]
# Make a post request using the cookies

# %%
time.sleep(5)
res = session_requests.post(URL, 
                        data = {"username" : "hcwhuang",
                                "password" : "hcwhuang29",
                                "csrf" : csrf},
                        headers = my_headers,
                        cookies = get_cookie,
                        timeout = 15)

post_cookie = session_requests.cookies.get_dict()
print("cookie:", post_cookie)

# %% [markdown]
# Get the cookies from the response of the post request

# %%
cookies_dict = str(get_cookie) + str(post_cookie)
print(cookies_dict)

# %% [markdown]
# Access the member profile and verify login status

# %%
url = 'https://www.planespotters.net/member/profile'
time.sleep(5)
page2 = session_requests.get(url, headers = my_headers, cookies = post_cookie)
doc2 = BeautifulSoup(page2.content,'html.parser')

# %% [markdown]
# Print profile page, all cookies and a boolean value to show the username is contained in the profile page

# %%
print(doc2)
print(cookies_dict)
print(bool(doc2.findAll(text = "hcwhuang")))



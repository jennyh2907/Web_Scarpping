# %%
from bs4 import BeautifulSoup
import requests
import time

# %% [markdown]
# 1. Access https://www.planespotters.net/user/login using a standard GET request. Read and store the cookies received in the response.  In addition, parse the response and read (and store to a string variable) the value of the hidden input field that will (most likely) be required in the login process.

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
# 2. Make a post request using the cookies from (1) as well as all required name-value-pairs (including your username and passwords).

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
# 3. Get the cookies from the response of the post request and add them to your cookies from (1).

# %%
cookies_dict = str(get_cookie) + str(post_cookie)
print(cookies_dict)

# %% [markdown]
# 4. Verifies that you are logged in by accessing the profile page https://www.planespotters.net/member/profile with the saved cookies.

# %%
url = 'https://www.planespotters.net/member/profile'
time.sleep(5)
page2 = session_requests.get(url, headers = my_headers, cookies = post_cookie)
doc2 = BeautifulSoup(page2.content,'html.parser')

# %% [markdown]
# 5. Then, print out the following at the end: The entire Jsoup/BeautifulSoup document of your profile page / All (combined) cookies from (3) / A boolean value to show your username is contained in the document in part (5)(a).

# %%
print(doc2)
print(cookies_dict)
print(bool(doc2.findAll(text = "hcwhuang")))



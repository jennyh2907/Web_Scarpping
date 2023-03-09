# %%
import pymysql
import warnings
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# %% [markdown]
# 1. Go to https://api.github.com and familiarize yourself with the API.

# %% [markdown]
# 2. Go to https://api.github.com/repos/apache/hadoop/contributors. This is the Apache Hadoop Github Repo's contributors’ endpoint. Extract the JSON corresponding to the first 100 contributors from this API. (Hint: the API request is a GET request and the variable name that handles the items per page is "per_page").  Write Java or Python code that does all this.

# %%
#  Connect to API 
url = "https://api.github.com/repos/apache/hadoop/contributors?per_page=100"
token = "your_token"
headers = {'Authorization': 'token ' + token}
response_API = requests.get(url, headers=headers)
print(response_API.status_code)

# Pull out the data
data = response_API.text
parse_100 = json.loads(data)
# print(parse_100)

# %% [markdown]
# 3. For each of the 100 contributors extracted in (2), write code that accesses their user information and extracts "login", "id", "location", "email", "hireable", "bio", "twitter_username", "public_repos", "public_gists", "followers", "following", "created_at" (and print those to screen)

# %%
# Create lists
index, login, id, location, email, hireable, bio, twitter, public_repo, public_gist, follower , following, created_at = ([] for i in range(13)) 

# Create a loop to save data and print
for i in range(0, 100):
    url_2 = parse_100[i]["url"]
    response_API_2 = requests.get(url_2, headers=headers)
    data2 = response_API_2.text
    parse_100_2 = json.loads(data2)
    index.append(i)
    login.append(parse_100_2["login"])
    id.append(parse_100_2["id"])
    location.append(parse_100_2["location"])
    email.append(parse_100_2["email"])
    hireable.append(parse_100_2["hireable"])
    bio.append(parse_100_2["bio"])
    twitter.append(parse_100_2["twitter_username"])
    public_repo.append(parse_100_2["public_repos"])
    public_gist.append(parse_100_2["public_gists"])
    follower.append(parse_100_2["followers"])
    following.append(parse_100_2["following"])
    created_at.append(parse_100_2["created_at"])
    print(i)
    print("login:", login[i])
    print("id:", id[i])
    print("location:", location[i])
    print("email:", email[i])
    print("hireable:", hireable[i])
    print("bio:", bio[i])
    print("twitter username:", twitter[i])
    print("public repo:", public_repo[i])
    print("public gist:", public_gist[i])
    print("followers:", follower[i])
    print("following:", following[i])
    print("created at:", created_at[i])

# %% [markdown]
# 4. Write code that creates an SQL database + table, and stores all the information obtained in (3) in it.  Please be cautious of the data type you choose for each column and briefly justify your decisions.  What do you choose as Primary Key and why?
# 
#     Since login, location, email, bio and twitter_username contain text and/or special characters, I define them as VARCHAR(255). As for the timestamp column created_at, I define it as DATETIME. For the rest of columns, I define them all as INT because they only contain numbers. And I choose id as a primary key as it looks like and unique identifier of each user as well as it allows for efficient indexing and faster search queries.

# %%
#ignore warnings
warnings.filterwarnings("ignore")
SQL_DB = "BAX422"

# Connect to server
conn = pymysql.connect(host='localhost', user = 'root', password = "", autocommit=True)
cursor = conn.cursor()

# Drop if exists
cursor.execute(f"DROP DATABASE IF EXISTS {SQL_DB}")

# Create database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {SQL_DB}")

# Close
cursor.close()
conn.close()

# Reconnect
conn = pymysql.connect(host='localhost', user = 'root', password = "", database = "BAX422", autocommit=True)
cursor = conn.cursor()

# Create table
cursor.execute("CREATE TABLE IF NOT EXISTS Github (login VARCHAR(255), id INT AUTO_INCREMENT PRIMARY KEY, location VARCHAR(255), email VARCHAR(255), hireable INT, bio VARCHAR(255), twitter_username VARCHAR(255), public_repo INT, public_gist INT, followers INT, following INT, created_at DATETIME)")

# Convert timestamp
created_at_2 = []
for i in range(0, 100):
    temp = datetime.fromisoformat(created_at[i].replace('Z', '+00:00'))
    created_at_2.append(temp.strftime("%Y-%m-%d %H:%M:%S"))

# Make sure the table is clear
cursor.execute("TRUNCATE TABLE Github")

# Insert data
for i in range(0, 100):
    cursor.execute("INSERT INTO Github (login, id, location, email, hireable, bio, twitter_username, public_repo, public_gist, followers, following, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(login[i], id[i], location[i], email[i], hireable[i], bio[i], twitter[i], public_repo[i], public_gist[i], follower[i], following[i], created_at_2[i]))

# %% [markdown]
# 5. Optimize your code in (4) to allow for quick look-ups of "login", "location", and "hireable".  What choices do you make and why?
# 
#     I decide to put a index on them. Without an index, the database would need to scan through every row in the table to find the data that matches the query. This can be very slow, especially for large tables. With an index, the database creates a separate data structure that maps the values in the indexed columns to the physical locations of the rows in the table. This data structure allows the database to quickly find the relevant rows that match the query by performing binary search.

# %%
# Check if index exist, if not then create index
cursor.execute("CREATE INDEX login_index ON Github (login);")
cursor.execute("CREATE INDEX location_index ON Github (location);")
cursor.execute("CREATE INDEX hireable_index ON Github (hireable);")




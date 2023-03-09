# %%
import pymongo
from pymongo import MongoClient

# %%
# connect to MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# access database and collection
db = client["samples_pokemon"]
collection = db["samples_pokemon"]

# %% [markdown]
# 1. (Let’s get things started …) Please write code (Python or Java) to query and print to screen all Pokémon character “name”s (and “_id” but not the entire document) with candy_count >= month + day of your birthday  (e.g., my birthday is 2/12 and I query candy_count >= 14 as 2+12 = 14).  (25% of points)   (Note:  the MongoDB operator for “>=” is “$gte”)

# %%
# Write the query
myquery=collection.find( {"candy_count" : {"$gte" : 36}}, {"_id" : 1, "name" : 1} )

# Print out
for x in myquery:
  print(x)

# %% [markdown]
# 2. (Let’s sprinkle in a little or …) Please write code (Python or Java) to query and print to screen all Pokémon character “name”s (and “_id” but not the entire document) with num = month or num = day of your birthday  (e.g., my birthday is 2/12 and I have to query num = 2 or num = 12).  (25% of points)

# %%
# Write the query
myquery = collection.find({"$or" : [{"num" : { "$eq" : "007"}}, {"num" : { "$eq" : "029"}}]}, {"_id" : 1, "name" : 1})

# Print out
for x in myquery:
  print(x)

# %% [markdown]
# 3. (And some RegEx as well …) Please write code (Python or Java) to query and print to screen all Crunchbase company “name”s (and “_id” but not the entire document) that have “text” in their “tag_list”.  (25% of points)

# %%
# Change a database
db = client["crunchbase"]
collection = db["crunchbase_database"]

# Write the query
myquery = collection.find({"tag_list" : {"$regex" : ".*text.*"}}, {"_id" : 1, "name" : 1})

# Print out
for x in myquery:
  print(x)

# %% [markdown]
# 4. (This is the final enemy. This question is equivalent of being in the final level of Super Mario facing Bowser)  Please write code (Python or Java) to query and print to screen all Crunchbase company “name”s and “twitter_username” (and “_id” but not the entire document) that (i) were founded between 2000 and 2010 (including 2000 and 2010), or (ii) email address is ending in “@gmail.com”.  (25% of points)

# %%
myquery = collection.find({"$or" : [{"founded_year" : {"$lt" : 2011, "$gt": 1999}}, {"email_address" : {"$regex" : ".*\@gmail.com"}}]}, {"_id" : 1, "name" : 1, "twitter_username" : 1})

# Print out
for x in myquery:
  print(x)




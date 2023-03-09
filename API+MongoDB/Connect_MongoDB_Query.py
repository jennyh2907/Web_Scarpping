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
# Write code to query and print to screen all Pokémon character “name”s and “_id” with candy_count >= month + day of my birthday

# %%
# Write the query
myquery=collection.find( {"candy_count" : {"$gte" : 36}}, {"_id" : 1, "name" : 1} )

# Print out
for x in myquery:
  print(x)

# %% [markdown]
# Write code to query and print to screen all Pokémon character “name”s and “_id” with num = month or num = day of my birthday 

# %%
# Write the query
myquery = collection.find({"$or" : [{"num" : { "$eq" : "007"}}, {"num" : { "$eq" : "029"}}]}, {"_id" : 1, "name" : 1})

# Print out
for x in myquery:
  print(x)

# %% [markdown]
# Write code to query and print to screen all Crunchbase company “name”s and “_id” that have “text” in their “tag_list”.

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
# Write code to query and print to screen all Crunchbase company “name”s and “twitter_username” and “_id” that 
# (i) were founded between 2000 and 2010 (including 2000 and 2010), 
# or (ii) email address is ending in “@gmail.com”.

# %%
myquery = collection.find({"$or" : [{"founded_year" : {"$lt" : 2011, "$gt": 1999}}, {"email_address" : {"$regex" : ".*\@gmail.com"}}]}, {"_id" : 1, "name" : 1, "twitter_username" : 1})

# Print out
for x in myquery:
  print(x)




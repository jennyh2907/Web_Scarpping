# %%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import time

# %% [markdown]
# Use Selenium, navigates to google.com
# Search for "askew" and  "google in 1998"

# %%
driver = webdriver.Chrome(service=Service('chromedriver_mac64'))
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)

# Start Google
driver.get("https://google.com");

# First search
search = driver.find_element(By.NAME, "q")
search.send_keys("askew")
time.sleep(1)
search.send_keys(Keys.RETURN) 
time.sleep(5) 

# Delete the text box
search = driver.find_element(By.NAME, "q")
search.send_keys(Keys.COMMAND + "a")
search.send_keys(Keys.DELETE)

# Second search
time.sleep(1)
search = driver.find_element(By.NAME, "q")
search.send_keys("google in 1998")
time.sleep(1)
search.send_keys(Keys.RETURN) # hit return after you enter search text
time.sleep(5) # sleep for 5 seconds so you can see the results

# Quit the driver
driver.quit()

# %% [markdown]
# Access bestbuy.com "Deal of the Day" 
# Read how much time is left for the Deal of the Day and prints the remaining time 
# Clicks on the Deal of the Day, its reviews, and saves the resulting HTML to local hard drive 

# %%
driver = webdriver.Chrome(service=Service('chromedriver_mac64'))
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)

# Start BestBuy.com
driver.get("https://www.bestbuy.com/");

# First click
time.sleep(2)
first = driver.find_element(By.XPATH, "//a[@data-lid='hdr_dotd']");
first.click()
time.sleep(2)

# Find remaining time
hours = driver.find_element(By.CLASS_NAME, "hours.cdnumber")
minutes = driver.find_element(By.CLASS_NAME, "minutes.cdnumber")
seconds = driver.find_element(By.CLASS_NAME, "seconds.cdnumber")
print("Remaining Time", hours.text, ":", minutes.text, ":", seconds.text)
time.sleep(2)

# Click on Deal of the day(product)
second = driver.find_element(By.XPATH, "//a[@data-track='[context:widgetType=featureV2,linkRegion=PrimaryMessage,linkPlacement=c1w2o1]']");
second.click()
time.sleep(10)

# Click on review
third = driver.find_element(By.CLASS_NAME, "v-m-right-xs")
third.click()
time.sleep(10)

# Save the resulting html to hardrive
content = driver.page_source

# write the page content
with open("bestbuy_deal_of_the_day.htm", "w+", encoding = 'utf-8') as file:
    file.write(content)
time.sleep(2)

# Quit the driver
driver.quit()



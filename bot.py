from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from random import randint
from random import choice
from random import random
import csv
from datetime import date
import json


def send_keys_slow(elem, text):
    for character in text:
        delay = random()
        elem.send_keys(character)
        time.sleep(delay)
    return 0


search_words = []

with open("search_words.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        search_words.append(row[0])

login_credentials = {"username": "your-name@email.com",
                     "password": "your!password.is§save_in:here"}

settings = {"max_searches": 60, "search_delay": {
    "min_delay": 10, "max_delay": 20}}

with open('settings.json') as json_file:
    data = json.load(json_file)
    login_credentials = data["login_credentials"]
    settings = data["settings"]

driver = webdriver.Chrome()

# Logging in
print("Logging into Microsoft account.")
driver.get("https://login.live.com")

email_box = driver.find_element_by_name("loginfmt")
confirm_btn = driver.find_element_by_id("idSIButton9")

time.sleep(randint(3, 5))

email_box.clear()
send_keys_slow(email_box, login_credentials["username"])
confirm_btn.click()

time.sleep(randint(5, 8))

password_box = driver.find_element_by_name("passwd")
confirm_btn = driver.find_element_by_id("idSIButton9")
check_box = driver.find_element_by_name("KMSI")
password_box.clear()
send_keys_slow(password_box, login_credentials["password"])
check_box.click()
confirm_btn.click()

print("Done.")
time.sleep(randint(3, 5))

# Search
last_day = None
while True:
    if not last_day == date.today():
        print("\nStarting search routine (Date: %s)::" % str(date.today()))
        for x in range(1, settings["max_searches"]):
            search_word = choice(search_words)
            search_delay = randint(
                settings["search_delay"]["min_delay"], settings["search_delay"]["max_delay"])

            print("  > Searching: \"%s\" (Search %i out of %i | ~%i Seconds until next search)" % (
                search_word, x, settings["max_searches"], search_delay))

            driver.get("https://www.bing.com")

            time.sleep(randint(3, 5))

            search_bar = driver.find_element_by_name("q")
            search_bar.click()
            send_keys_slow(search_bar, search_word)
            time.sleep(1)
            search_bar.send_keys(Keys.RETURN)

            time.sleep(randint(3, 5))
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(randint(3, 5))
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(search_delay)

        last_day = date.today()
        print("\nDaily search routine over.")
    else:
        time.sleep(120)

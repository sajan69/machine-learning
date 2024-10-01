from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
import os
import json


CHROME_DRIVER_PATH = Service(executable_path=r"C:\Users\Acer\Desktop\Projects\machine-learning\web_bot\chromedriver.exe")
#open the brave browser
OPTIONS = webdriver.ChromeOptions()
#open in brave browser
OPTIONS.binary_location = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
#disable the notifications
OPTIONS.add_argument("--disable-gpu")
OPTIONS.add_argument("--no-sandbox")
OPTIONS.add_argument("--disable-dev-shm-usage")

DRIVER = webdriver.Chrome(service=CHROME_DRIVER_PATH, options=OPTIONS)

COUNTRIES = ["USA"]

def open_google():
    DRIVER.get("https://www.google.com")
    time.sleep(2)
    #change the language to english
    # DRIVER.find_element(By.XPATH, value="//a[@href='https://www.google.com/setprefs?sig=0_9ultBiulvBMfcMixOhfEQ_rmBDY%3D&hl=en&source=homepage&sa=X&ved=0ahUKEwjb6pLtm-2IAxVMRWwGHQh2CfUQ2ZgBCBU']").click()

    time.sleep(2)

def search_country(country):
    search_box = DRIVER.find_element(By.NAME, "q")

    #print the capital city of the country
    # capital_city = DRIVER.find_element(By.XPATH, value=f"//div[@class='BNeawe iBp4i AP7Wnd']")  # Find the capital city of the country
    # print(f"{country}: {capital_city.text}")
    search_box.clear()  # Clear the search box before entering new text
    search_box.send_keys(f"{country} capital city")
    # press enter
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Wait for the search results to load




    time.sleep(2)





def main():
    open_google()
    for country in COUNTRIES:
        search_country(country)
    print("Press any key to exit...")
    input()  # Wait for user input


    
    if DRIVER is not None:
        DRIVER.quit()




if __name__ == "__main__":
    main()
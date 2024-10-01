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

def login():
    with open("config.json") as configFile:
        credentials = json.load(configFile)
        email_value = credentials["email"]
        password_value = credentials["password"]
        time.sleep(2)
        #click the login button
        DRIVER.find_element(By.XPATH, value="//a[@href='https://id.atlassian.com/login?application=trello&continue=https%3A%2F%2Ftrello.com%2Fauth%2Fatlassian%2Fcallback%3Fdisplay%3DeyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%253D%253D&display=eyJ2ZXJpZmljYXRpb25TdHJhdGVneSI6InNvZnQifQ%3D%3D']").click()
        time.sleep(2)
        #enter the email but first clear the field
        email_field = DRIVER.find_element(By.CSS_SELECTOR, value="input[name='username']")
        email_field.clear()
        #enter the email from the config
        email_field.send_keys(email_value)
        #click the login button
        DRIVER.find_element(By.CSS_SELECTOR, value="button[id='login-submit']").click()
        time.sleep(2)
        #enter the password
        password_field = DRIVER.find_element(By.CSS_SELECTOR, value="input[id='password']")
        #clear the password field
        password_field.clear()
        #enter the password from the config file
        password_field.send_keys(password_value)
        #click the login button
        DRIVER.find_element(By.CSS_SELECTOR, value="button[id='login-submit']").click()
        time.sleep(2)
        
        #if the link to enabale or disable the two factor authentication is present then click 
        # if  DRIVER.find_element(By.CSS_SELECTOR, value="button[id='mfa-promote-dismiss']"):
        #     print("Two factor authentication is enabled")
        #     DRIVER.find_element(By.CSS_SELECTOR, value="button[id='mfa-promote-dismiss']").click()
        #     time.sleep(2)
        # else:
        #    pass
        # time.sleep(2)
        
def navigate_to_board():
    #now to choose the board
    DRIVER.find_element(By.CSS_SELECTOR, value="div[title='test']").click()
    time.sleep(2)

def add_card():
    #click the add card button
    DRIVER.find_element(By.XPATH, value="//textarea[@aria-label='To Do']/ancestor::div/descendant::div[@class='IapUGb_Cq2VzSr']/child::button").click()
    time.sleep(2)

task_name = "test task"

def add_task(task_name):
    #enter the task name
    task_field = DRIVER.find_element(By.CSS_SELECTOR, value="textarea[placeholder='Enter a name for this card…']")
    #clear the task field
    task_field.clear()
    task_field.send_keys(task_name)
    #click the add card button
    DRIVER.find_element(By.CSS_SELECTOR, value="button[data-testid='list-card-composer-add-card-button']").click()

    time.sleep(2)

def screenshotPage():
    #take a screenshot of the page
    time.sleep(2)
    date_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    fpath = os.path.join(os.getcwd(), "screenshots", f"trello_{date_string}.png")
    DRIVER.get_screenshot_as_file(fpath)
    print(f"Screenshot saved at {fpath}")




def main():
    try:
        DRIVER.get("https://trello.com")
        login()
        navigate_to_board()
        add_card()
        add_task(task_name)
        screenshotPage()
        input("Press Enter after you have logged in")
        DRIVER.close()
        #if user closes the browser themselves then close the driver
        if DRIVER:
            DRIVER.quit()



    except Exception as e:
        print(e)
        DRIVER.close()

if __name__ == "__main__":
    main()
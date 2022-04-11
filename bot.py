import time
from datetime import datetime

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

THRESHOLD = "2022-07-12 15:00"  # Edit the timestamp if you want


def send_message(message):
    bot_token = ""  # Enter Bot token from telegram app
    chat_id = ""  # Enter Chat ID of telegram bot
    send_message_url = (
        "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}".format(
            bot_token, chat_id, message
        )
    )
    response = requests.get(send_message_url)


def get_driver():
    geoAllowed = webdriver.FirefoxOptions()
    geoAllowed.headless = True
    geoAllowed.add_argument(
        "--screenshot test.jpg https://fp.trafikverket.se/Boka/#/licence"
    )
    geoAllowed.set_preference("geo.prompt.testing", True)
    geoAllowed.set_preference("geo.prompt.testing.allow", True)
    geoAllowed.set_preference(
        "geo.provider.network.url",
        'data:application/json,{"location": {"lat": 57.76675745688461, "lng": 11.883161620545224}, "accuracy": 100.0}',
    )
    return webdriver.Firefox(options=geoAllowed)


def main():    
    driver = get_driver()
    driver.get("https://fp.trafikverket.se/Boka/#/licence")
    # Sleep to let elements load
    timeout = 20
    try:
        element_present = EC.presence_of_element_located(
            (By.ID, "social-security-number-input")
        )
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        driver.save_screenshot("test.png")
        print("Timed out waiting for page to load for SSN")

    social_security = "199507174713"
    ssn_element = driver.find_element(By.ID, value="social-security-number-input")
    ssn_element.send_keys(social_security)
    ssn_element.send_keys(Keys.RETURN)
    try:
        element_present = EC.presence_of_element_located(
            (By.ID, "examination-type-select")
        )
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        driver.save_screenshot("test.png")
        print("Timed out waiting for page to load for examination type")

    exam_type_element = driver.find_element(By.ID, value="examination-type-select")
    exam_type = "Körprov"  # Driving Test ;)
    exam_type_element.send_keys(exam_type, Keys.ARROW_DOWN, Keys.ENTER)
    exam_type_element.send_keys(Keys.RETURN)

    try:
        element_present = EC.presence_of_element_located((By.ID, "vehicle-select"))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        driver.save_screenshot("test.png")
        print("Timed out waiting for page to load for vehicle select")

    vehicle_type_element = driver.find_element(By.ID, value="vehicle-select")
    vehicle_type = "Automatbil"  # Automat!! ;)
    vehicle_type_element.send_keys(vehicle_type, Keys.ARROW_DOWN, Keys.ENTER)
    vehicle_type_element.send_keys(Keys.RETURN)

    try:
        element_present = EC.presence_of_element_located(
            (
                By.XPATH,
                "/html/body/div[2]/section[5]/div[2]/div[14]/div[1]/div/div/div[1]/div/div[2]/strong",
            )
        )
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        driver.save_screenshot("test.png")
        print("Timed out waiting for page to load for Available Dates")

    date_str = driver.find_element(
        By.XPATH,
        value="/html/body/div[2]/section[5]/div[2]/div[14]/div[1]/div/div/div[1]/div/div[2]/strong",
    ).text
    message = "Next Available Time for Driving Test is on: {}".format(date_str)
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    print(message)
    print(100 * "--")
    if date < datetime.strptime(THRESHOLD, "%Y-%m-%d %H:%M"):
        print("Sending a message")
        send_message(message)
    driver.close()


if __name__ == "__main__":
    i = 0
    sleep_time_seconds = 5
    while True:
        i += 1
        try:
            print("Iteration =: ", i)
            main()
        except:
            print("Failed to load website")
        print("Going to sleep for {} seconds.....".format(sleep_time_seconds))
        time.sleep(sleep_time_seconds)

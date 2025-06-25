from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
load_dotenv()

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")


def get_li_at_cookie(username, password):
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")

    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    time.sleep(5)

    cookies = driver.get_cookies()
    driver.quit()

    for cookie in cookies:
        if cookie['name'] == 'li_at':
            return cookie['value']

    return None


if __name__ == "__main__":
    email = LINKEDIN_EMAIL
    password = LINKEDIN_PASSWORD
    li_at_cookie = get_li_at_cookie(email, password)
    if li_at_cookie:
        with open("li_at.txt", "w") as f:
            f.write(li_at_cookie)
        print("li_at cookie saved!")
    else:
        print("li_at cookie not found.")

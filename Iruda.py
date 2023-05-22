from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re, time


"""
Selenium 크롤링 할 때, 현재 창에서 크롤링하는 방법(Debugging Mode)
https://melonicedlatte.com/2023/01/01/193400.html
MacOS 명령어
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=55426 --user-data-dir=ChromeProfile
"""
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome("chromedriver", options=options)

driver.get("https://nutty.chat/channels")

driver.implicitly_wait(2)

# Join chatroom
driver.find_element(By.XPATH, "/html/body/main/div[4]/div/div/div[1]/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div[1]/div/div/div[1]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div[1]").click()

driver.implicitly_wait(3)

messages = []

while True:
    try:
        # Get the last text (REPLACE CLASS NAMES of yours)
        xpath = "//div[@class='css-1rynq56 r-ubezar r-16dba41 r-oam9g7 r-1aittka r-cqee49']"
        luda_texts = driver.find_elements(By.XPATH, f"{xpath}")

        # Retrieve last 5 messages we missed
        for i, luda_text in enumerate(reversed(luda_texts[:5])):
            luda_text = luda_text.text.strip()

            if luda_text:
                if not luda_text in messages:
                    messages.append(luda_text)
                    print(f"🙆🏻‍♀️이루다: {luda_text}")


        input_box = driver.find_element(By.XPATH, "/html/body/main/div[4]/div/div/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div[2]/textarea")

        time.sleep(1)
        input_box.send_keys("너는 언제 자?") # Cannot send emojis in Chrome
        time.sleep(1)
        input_box.send_keys(Keys.ENTER)

    except Exception as e:
        print(e)
    finally:
        time.sleep(10)
    break

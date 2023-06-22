from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import os
import time
from pathlib import Path
from friend import friends
from selenium.webdriver.common.keys import Keys
from ai import *
from clean_text import *





class SnapDriver:

    def __init__(self, 
                 store_session=True, 
                 user_data=False, 
                 phone_number:  str="phone number", 
                 password: str="password",
                 headless=False):
        self.bot_info = {
            "phone_number": phone_number,
            "password": password
        }

        options = uc.ChromeOptions()

        # saves session data to a folder called chrome_data
        if store_session:
            if not user_data:
                user_data = f"{Path().absolute()}/chrome_data"
            if not os.path.isdir(user_data):
                os.mkdir(str(user_data))
            Path(f"{user_data}").touch()
            options.add_argument(f"--user-data-dir={user_data}")
            print(f"data saved to:\n{user_data}")


        options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
        #options.add_argument("--disable-extensions")
        #options.add_argument('--disable-applicatigvon-cache')
        #options.add_argument('--disable-gpu')
        #options.add_argument("--no-sandbox")
        #options.add_argument("--disable-setuid-sandbox")
        #options.add_argument("--disable-dev-shm-usage")
        if headless: options.add_argument("--headless")
        print("Starting browser")

        self.browser = uc.Chrome(options=options)

        self.browser.get("https://web.snapchat.com/")
        time.sleep(3)
        print(self.browser.current_url, " is open")


    def __del__(self):
        print("Closing browser")
        self.browser.quit()


    def login_page(self):
        app_page = self.check_home_page()
        if not app_page:
            print("Logging in")
            while self.browser.title != "Log In | Snapchat":
                time.sleep(5)
            try:
                xpath = '/html/body/div/div/div/div[3]/article/div/div[3]/form/div[1]/div/a'
                use_num = self.browser.find_element(By.XPATH, xpath)
                use_num.click()
            except:
                print("Error use nem element not found")
            try:
                xpath = '/html/body/div/div/div/div[3]/article/div/div[3]/form/div[1]/div[2]/div/input'
                login_name = self.browser.find_element(By.XPATH, xpath)
                login_name.send_keys(self.bot_info["phone_number"])
            except:
                print("Error login element not found")
            try:
                xpath = "//button[@type='submit']"
                next = self.browser.find_element(By.XPATH, xpath)
                next.click()
            except:
                print("Error next element not found")
            

            while self.browser.title != "Accounts • Snapchat":
                time.sleep(1)
            try:
                password = self.browser.find_element(By.XPATH, '//input[@name="password"]')
                password.send_keys(self.bot_info["password"])
                click_login = self.browser.find_element(By.XPATH, '//button[@type="submit"]')
                click_login.click()
            except:
                print("Error password element not found")
        print("Logged in")
        time.sleep(5)
        click = self.browser.find_element(By.XPATH, '//button[@type="button"]')
        click.send_keys(Keys.ENTER)


    def check_home_page(self):
        print("Checking home page")
        correct_page = []
        for i in range(100):
            correct_page.append(f"({i}) Snapchat")
        print(self.browser.title)
        i = 0
        while  True:
            for page in correct_page:
                if self.browser.title == page or self.browser.title == "Snapchat":
                    print("Home page found")
                    return True
                if i == 99:
                    print(self.browser.current_url)
                    print("Error: Could not find home page")
                    return False
                i += 1


    def get_frens(self):
        self.check_home_page()
        loading = "Getting chats_id......"
        for i in loading:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")
        friends_list = []

        xpath_test = '//*[@role="button"]'
        chat_id = self.browser.find_elements(By.XPATH, xpath_test)
        for id in chat_id:
            current_id = id.get_attribute("aria-labelledby")
            try:
                current_name = self.browser.find_element(By.ID, f"title-{clean_id(current_id)}").text
            except:
                current_name = "No name found"
            current_status = self.browser.find_element(By.ID, f"status-{clean_id(current_id)}").text
            friend = friends(id=(clean_id(f"{current_id}")), name=(current_name), status=(current_status))
            friends_list.append(friend)
        for fren in friends_list:
            console_output = f"{fren.name} - {fren.status} - {fren.id}"
            for i in console_output:
                print(i, end="", flush=True)
                time.sleep(0.01)
            print("")
        return friends_list


    def GetFrenChats(self, fren):
        console_output = f"{fren.name} - {fren.status} - {fren.id}"
        for i in console_output:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("")

        if not self.check_home_page():
            print("Error: Could not find home page")
            time.sleep(100)
            
        fren_tab = self.browser.find_element(By.XPATH, f'//*[@aria-labelledby="title-{fren.id} comma1 status-{fren.id}"]')
        fren_tab.click()
        time.sleep(5)
        chats_head = self.browser.find_element(By.TAG_NAME, "ul")
        chats = chats_head.find_elements(By.TAG_NAME, "li")
        c = chats[0].find_element(By.XPATH, f'//*[@id="cv-{fren.id}"]')
        return c

    def SendChat(self, fren, response):
        fren_tab = self.browser.find_element(By.XPATH, f'//*[@aria-labelledby="title-{fren.id} comma1 status-{fren.id}"]')
        time.sleep(3)
        print("response:", response)
        textbox = self.browser.find_element(By.XPATH, '//*[@role="textbox"]')
        textbox.send_keys(response)
        textbox.send_keys(Keys.RETURN)
        fren_tab.click()
        time.sleep(3)


    def message_new_chats(self, fren_data):
        for index in range(len(fren_data)):
            if fren_data[index].status == "New Chat":
                fren = fren_data[index]
                c = self.GetFrenChats(fren)
                response = SnapGF(c, fren.name, self.browser)
                self.SendChat(fren, response)
                index += 1


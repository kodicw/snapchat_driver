from driver import SnapDriver
from time import sleep
from selenium.webdriver.common.by import By
import os

phone = os.environ.get("phone")
password = os.environ.get("password")

if not phone or not password:
    print("Please set phone number and password as environment variables")
    exit()

snapchat = SnapDriver(phone_number= phone,
                      password= password,
                      headless=False,
                      )

snapchat.login_page()
while True:
    fren_data = snapchat.get_frens()
    snapchat.message_new_chats(fren_data)

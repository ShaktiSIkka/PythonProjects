import webbrowser
import os
import time
from selenium import webdriver
link = input("Enter URL to buzz:-> ")
#
# sleep_time = input("Enter Video length (example 7:27 for 7 mins and 27 secs):-> ")
# timeArray = sleep_time.split(":")
# mins = int(timeArray[0])
# secs = int(timeArray[1])
# browser = webbrowser.open_new(url)
# sleep_time = (mins*60) + secs
# time.sleep(sleep_time)
path = "C:\\Users\\shakt\\Downloads\\geckodriver-v0.29.1-win64"
driver = webdriver.Firefox(path)
driver.get(url=link)
from os import link
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import DesiredCapabilities
from bs4 import BeautifulSoup #pip install beautifulsoup4
import PySimpleGUI as sg
import tkinter as tk
from tkinter import ttk
import sv_ttk
import csv
from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox
import csv
from datetime import datetime
import requests
from selenium.webdriver.chrome.service import Service
# packages copied from project Parium

# create runtime window
options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")
options.add_argument("--allow-mixed-content")

# chrome web driver location, if installed someplace else, can be changed, use relative location
executablePathWebDriverChrome = '.\chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=executablePathWebDriverChrome)
driver.implicitly_wait(10)

# find translation
filename = "Dopamina3.txt"
with open(filename, "r+", encoding='UTF-8') as file:
    for line in file:
        print(line.rstrip())
        word = line.rstrip()
        link = "https://www.spanishdict.com/translate/"+word
        print(link)
        try:
            gender = ""
            driver.get(link)
            try:
                translation = driver.find_element("id", "quickdef1-es").text
            except:
                translation = driver.find_element("id", "quickdef1-en").text
            try:
                type = driver.find_element("xpath", '//*[@id="dictionary-neodict-es"]/div/div[2]/div[1]/a').text
            except:
                type = driver.find_element("xpath", '//*[@id="dictionary-neodict-en"]/div/div[2]/div[1]/a').text
            if "NOUN" in type:
                if translation.startswith("la" or "las"):
                    gender = "f"
                if translation.startswith("el" or "los"):
                    gender = "m"
                if "FEMININE" in type:
                    gender = "f"
                    word = "la " + word
                if "MASCULINE" in type:
                    gender = "m"
                    word = "el " + word
                type = "N"
                print(translation, type, gender)
            if "VERB" in type:
                type = "V"
                print(translation, type)
            if "ADJECTIVE" in type:
                type = "Adj"
            if "INTERJECTION" in type:
                type = "Conj"
            string = word + ";" + translation + ";" + type + ";" + gender
            with open("output.txt", "a", encoding='UTF-8') as file2:
                file2.seek(0)
                file2.write(string)
                file2.write("\n")
                file2.close()
        except:
            print("error")






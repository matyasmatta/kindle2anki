# packages copied from project Parium, not all necessary
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
import time
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # create runtime window
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--allow-mixed-content")

    # since v0.0.2 no longer necessary to pass in chromedrive location, now it will install on its own! (about 8 MiB so no worries)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)

    # main loop
    ## file that you want to process, use relative location
    filename = "test.txt"
    ## debug tool
    successful_runs = 0
    failed_runs = 0
    total_runs = 0

    ## open file, use UTF-8 encoding
    with open(filename, "r+", encoding='UTF-8') as file:
        for line in file:
            print(line.rstrip())
            word = line.rstrip()
            link = "https://www.spanishdict.com/translate/"+word
            print(link)
            try:
                ### set variables
                gender = ""

                ### open link
                driver.get(link)

                ### try to locate elements
                try:
                    translation = driver.find_element("id", "quickdef1-es").text
                except:
                    translation = driver.find_element("id", "quickdef1-en").text
                try:
                    type = driver.find_element("xpath", '//*[@id="dictionary-neodict-es"]/div/div[2]/div[1]/a').text
                except:
                    type = driver.find_element("xpath", '//*[@id="dictionary-neodict-en"]/div/div[2]/div[1]/a').text

                ### process data
                if "NOUN" in type:
                    #### formatted for Anki Duolingo Format, i.e. with articles
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
                    #### fix for words that work with both genders
                    if word.startswith("el la"):
                        word = "el/la " + word[6:]
                    type = "N"
                ### make sure to use " VERB" due to adverbs conflicting!
                if " VERB" in type:
                    type = "V"
                if "ADJECTIVE" in type:
                    #### adjectives are formatted into Anki Duolingo Format, i.e. inflected for both genders
                    type = "Adj"
                    if word.endswith("ado"):
                        word = word + ", " + word[:-3] + "ada"
                    elif word.endswith("ada"):
                        word = word[:-3] + "ado" + ", " + word
                if "INTERJECTION" in type:
                    type = "Conj"
                if "PREPOSITION" in type:
                    type = "Prep"
                if "ADVERB" in type:
                    type = "Adv"

                string = word + ";" + translation + ";" + type + ";" + gender
                with open("output.txt", "a", encoding='UTF-8') as file2:
                    file2.seek(0)
                    file2.write(string)
                    file2.write("\n")
                    file2.close()
                    successful_runs += 1
            except:
                failed_runs += 1
    total_runs = successful_runs + failed_runs
    success_rate = (successful_runs/total_runs)*100
    print(success_rate, "%")

# classic python import check
if __name__ == '__main__':
    main()




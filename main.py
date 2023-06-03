## Version 0.1.2 - alpha, see notes at GitHub (MMatty#8137)
# libraries and presets
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfile, askopenfilename
import sv_ttk
from os import link
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup 
import PySimpleGUI as sg
from tkinter import messagebox
from datetime import datetime
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from selenium.webdriver.common.by import By
import re
from wiktionaryparser import WiktionaryParser
import json
from PyDictionary import PyDictionary
from googletrans import Translator
from deep_translator import GoogleTranslator
from deep_translator import PonsTranslator
import wiktionary_german
from unidecode import unidecode
import pandas as pd
import csv

# gui set-up
class App(ttk.Frame):
    global accentButton_text
    accentButton_text = "Submit"
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        # Make the app responsive
        for index in (0, 1, 2):
            self.columnconfigure(index=index, weight=1)
            self.rowconfigure(index=index, weight=1)

        # Create widgets
        self.setup_widgets()

    def setup_widgets(self):
        # Create a Frame for input widgets
        self.widgets_frame = ttk.Frame(self, padding=(15, 0, 0, 0))
        self.widgets_frame.grid(
            row=0, column=1, padx=10, pady=(10, 10), sticky="nsew", rowspan=3
        )
        self.widgets_frame.columnconfigure(index=0, weight=1)

        # Accentbutton
        def openfile():
            global filepath
            filepath = askopenfilename()
        self.button = ttk.Button(
            self.widgets_frame, 
            text="Choose file", 
            command=openfile

        )
        self.button.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # Submitbutton
        def submitFilePath():
            german()
            accentButton_text = "Processing"
        self.accentbutton = ttk.Button(self.widgets_frame, text=accentButton_text, command=submitFilePath, style="Accent.TButton")
        self.accentbutton.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

        # Sizegrip
        self.sizegrip = ttk.Sizegrip(self)
        self.sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))
def gui():
    root = tk.Tk()
    root.title("Kindle to Anki")

    sv_ttk.set_theme("dark")

    app = App(root)
    app.pack(fill="both", expand=True)

    root.update_idletasks()  # Make sure every screen redrawing is done

    width, height = root.winfo_width(), root.winfo_height()
    x = int((root.winfo_screenwidth() / 2) - (width / 2))
    y = int((root.winfo_screenheight() / 2) - (height / 2))

    # Set a minsize for the window, and place it in the middle
    root.minsize(width, height)
    root.geometry(f"+{x}+{y}")

    root.mainloop()

# main program
def spanish():
    # create runtime window
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--allow-mixed-content")

    # since v0.0.2 no longer necessary to pass in chromedrive location, now it will install on its own! (about 8 MiB so no worries)
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except:
        tk.messagebox.showerror(title="Chrome version incompatible", message="Your version of Chrome might not be up-to-date, please visit Chrome settings to update.", **options)

    driver.implicitly_wait(10)

    # main loop
    ## file that you want to process, use relative location
    filename = filepath
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
                        gender = "m/f"
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
    print(round(success_rate,1), "%")

def selenium_module():
    # create runtime window
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    options.add_argument("--allow-mixed-content")

    # since v0.0.2 no longer necessary to pass in chromedrive location, now it will install on its own! (about 8 MiB so no worries)
    try:
        global driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except:
        tk.messagebox.showerror(title="Chrome version incompatible", message="Your version of Chrome might not be up-to-date, please visit Chrome settings to update.", **options)
    driver.implicitly_wait(10)

def german():
    def unicode_conversion(word):
        word = word.encode("utf-8")
        return word
    with open(filepath, "r", errors='ignore', encoding="utf-16") as file:
        for line in file:
            try:
                print(line.rstrip())
                word_original = line.rstrip()
                word = unidecode(word_original)

                parser = WiktionaryParser()
                parsed = parser.fetch(word_original, 'german') 
                try:
                    parsed[0]['definitions'][0]['text'] == []
                    word, definition, wordtype, example, additionals, synonyms = wiktionary_german.get_data(word_original)
                    print(word, definition, wordtype, example, additionals, synonyms)
                    if example:
                        translator = Translator()
                        result = translator.translate(example, src='de', dest='en')
                        example_english = result.text
                    else:
                        example_english = ""

                    with open("output_de.txt", "a", encoding='utf-8', newline='') as f:
                        f.seek(0)
                        writer = csv.writer(f)
                        content = [word, definition, example, example_english, additionals, synonyms, wordtype]
                        writer.writerow(content)
                except:
                    Exception
            except:
                pass


# actual code
if __name__ == '__main__':
    gui()
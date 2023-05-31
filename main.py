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
import googletrans
from deep_translator import GoogleTranslator
from deep_translator import PonsTranslator

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
    def wiktionary(word):
        # Set driver for requests
        language_code = 'de'  # German language code
        url = f"https://{language_code}.wiktionary.org/w/api.php?action=query&titles={word}&prop=revisions&rvprop=content&format=json"
        response = requests.get(url)
        data = response.json()

        # Set variables
        gender = None
        preterite = None
        word_type = None
        participle = None
        auxiliary = None
        definitions = None

        # Translation/definition
        try:
            language_code = 'en'  # English language code
            url = f"https://{language_code}.wiktionary.org/w/api.php?action=query&titles={word}&prop=extracts&format=json"

            response = requests.get(url)
            data = response.json()


            if 'pages' in data['query']:
                page = next(iter(data['query']['pages'].values()), None)
                if page and 'extract' in page:
                    # Split the extract into individual definitions
                    raw_definitions = page['extract'].split("\n#")[1:]
                    for raw_def in raw_definitions:
                        # Clean up the definition text
                        cleaned_def = raw_def.strip("* :#")
                        definitions.append(cleaned_def)
        except:
            pass
        try:
            definitions = PonsTranslator(source='german', target='english').translate(word, return_all=True)
        except:
            pass
        try:
            definitions = GoogleTranslator(source='de', target='en').translate(word, return_all=True)
        except:
            pass

        # Wordtype
        language_code = 'de'  # German language code
        url = f"https://{language_code}.wiktionary.org/w/api.php?action=query&titles={word}&prop=revisions&rvprop=content&format=json"

        response = requests.get(url)
        data = response.json()
        try:
            if 'pages' in data['query']:
                page = next(iter(data['query']['pages'].values()), None)
                if page and 'revisions' in page:
                    content = page['revisions'][0]['*']
                    word_type_index = content.find('{{Wortart|')
                    if word_type_index != -1:
                        word_type_start = word_type_index + len('{{Wortart|')
                        word_type_end = content.find('|', word_type_start)
                        word_type = content[word_type_start:word_type_end]
                    
                    if word_type == "Substantiv":
                        gender_index = content.find('{{Deutsch Substantiv')
                        if gender_index != -1:
                            gender_start = content.find('|Genus=', gender_index)
                            if gender_start != -1:
                                gender_start += len('|Genus=')
                                gender_end = content.find('|', gender_start)
                                gender = content[gender_start:gender_end]

                        # Handle alternative template for gender
                        if not gender:
                            gender_index = content.find('{{Deutsch Substantiv')
                            if gender_index != -1:
                                gender_start = content.find('|Geschlecht=', gender_index)
                                if gender_start != -1:
                                    gender_start += len('|Geschlecht=')
                                    gender_end = content.find('|', gender_start)
                                    gender = content[gender_start:gender_end]
        except:
            pass
        try:
            # wordtype
            selenium_module()
            driver.get(f"https://de.wiktionary.org/wiki/{word}")
            word_type = driver.find_element(By.XPATH, '//*[@id="Substantiv,_m"]/a').text
        except:
            pass

        if word_type == "Verb":
            # preterite
            try:
                # Extract past tense for verbs
                past_tense_index = content.find('{{Deutsch Verb Konjugation|')
                if past_tense_index != -1:
                    past_tense_start = past_tense_index + len('{{Deutsch Verb Konjugation|')
                    past_tense_end = content.find('|', past_tense_start)
                    preterite = content[past_tense_start:past_tense_end]
            except:
                pass
            try:
                past_tense_match = re.search(r"{{Deutsch Verb Konjugation\|Präteritum=(.*?)\|", content)
                if past_tense_match:
                    preterite = past_tense_match.group(1)
            except:
                pass
            try:
                # Extract past tense for verbs
                past_tense_match = re.search(r"\{\{VORGÄNGER\|(.*?)\}\}", content)
                if past_tense_match:
                    preterite = past_tense_match.group(1)
            except:
                pass
            try:
                selenium_module()
                driver.get(f"https://de.wiktionary.org/wiki/{word}")
                preterite = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[5]/td[2]/a').text
                participle = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[10]/td[1]/a').text
                auxiliary = driver.find_element(By.XPATH, '//*[@id="mw-content-text"]/div[1]/table[2]/tbody/tr[10]/td[2]/a').text
            except:
                print("Selenium exception module failed")

        return definitions, word_type, gender, preterite, participle, auxiliary
    class legacy_wiktionary_selenium:
            def word_type(word):
                selenium_module()
                link = "https://en.wiktionary.org/wiki/" + word +"#German"
                driver.get(link)
                
                word_type_xpath = '//*[@id="Noun_2"]'
                word_type = driver.find_element(By.XPATH, word_type_xpath).text
                return word_type
            
            def noun(word):
                selenium_module()
                gender_xpath = "/html/body/div[3]/div[3]/div[5]/div[1]/p[4]/span[1]/abbr"
                try:
                    gender = driver.find_element(By.CLASS_NAME, "gender").text
                except:
                    gender = driver.find_element(By.XPATH, gender_xpath).text
                return gender
            
            def verb(word):
                selenium_module()
                try:
                    preterite = driver.find_element(By.CLASS_NAME, "Latn form-of lang-de 1//3|s|pret-form-of").text
                except:
                    preterite_xpath = '/html/body/div[3]/div[3]/div[5]/div[1]/p[2]/b[2]'
                    preterite = driver.find_element(By.XPATH, preterite_xpath).text

    with open(filepath, "r+", errors='ignore', encoding="utf8") as file:
        for line in file:
            print(line.rstrip())
            word = line.rstrip()
            definitions, word_type, gender, preterite, participle, auxiliary = wiktionary(word)
            print(definitions, word_type, gender, preterite, participle, auxiliary)


# actual code
if __name__ == '__main__':
    gui()
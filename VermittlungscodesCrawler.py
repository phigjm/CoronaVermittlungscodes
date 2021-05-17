# %% imports:
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import datetime
import time
import threading

import os
if os.name == 'nt':
    import winsound
else:
    from playsound import playsound
print(os.name)


# %% Config
parallel = 10 # Wie viel Browserinstanzen möchtest du verwenden? 10 Browserinstanzen bedeuten 10 Abfragen pro delayTime.
delayTime = 10*60 # Das ist die Minimal zugelassene Abfragezeit.
urlSite = "https://001-iz.impfterminservice.de/impftermine/service?plz=68163" # waehle hier die URL deines Corona Zentrums https://www.impfterminservice.de/impftermine  
chromedrivePath = r'./chromedriver.exe' # Make sure Chrome and the correckt chromedrive version is installed
checkRate = delayTime/parallel
print(f"Es wird in etwa alle {str(checkRate)} Sekunden geprueft.")


# %% Sound on success
def success():
    if os.name == 'nt':
        for i in range(15):
            duration = 500  # Millisekunden
            freq = 440  # Hz
            winsound.Beep(freq, duration)
            duration = 500  # milliseconds
            freq = 880  # Hz
            winsound.Beep(freq, duration)
    else:
        playsound("./warning.mp3")


# %% Multithreads

class SeleniumThreads(threading.Thread):
     threadNumber=0
     def __init__(self,threadNumber):
         super(SeleniumThreads, self).__init__()
         self.threadNumber=threadNumber

     def run(self):
         time.sleep(self.threadNumber*checkRate)
         options = Options()
         ua = UserAgent()
         userAgent = ua.random
         print(userAgent)
         print(f"waite {self.threadNumber*checkRate}")
         options.add_argument(f'user-agent={userAgent}')
         driver = webdriver.Chrome(chrome_options=options, executable_path=chromedrivePath)
         while True:
            driver.get(urlSite)
            time.sleep(5)
            while "Virtueller Warteraum des Impfterminservice" in driver.page_source:
                print("Thread: {self.threadNumber} is Waiting")
                time.sleep(delayTime-5)
            
            driver.execute_script('document.getElementsByName("vaccination-approval-checked")[1].click()')
            time.sleep(10) #Delay
            if not "wurden keine freien Termine in Ihrer Region gefunden" in driver.page_source:#Check if text Exits
                success()
            time.sleep(delayTime-15)
         

for i in range(parallel):
    SeleniumThreads(i).start()



import requests
import time
from bs4 import BeautifulSoup
from Passwort import Passwort
from pykeepass import PyKeePass
import Reading_Keyboard as Reading_Keyboard
from datetime import datetime

# This script performs web scraping and controls the input-emulation reader.
# It accepts input from a keyboard-emulating device (for example an RFID scanner), 
# looks up matching credentials in a local KeePass database, and automates the login and 
# verification process on the target website

def web_scraping(timeout=None):
    print("CPSZT_Test wird aufgerufen")
    print("Bitte Chip Scännen")
    tag = Reading_Keyboard.start_scan()
    print(f"Verwendeter Tag = {tag}")
    print("Daten werden geholt")

    kp = PyKeePass(r' # Here the file path to the KeePass database must be specified ', password=Passwort)

    entry = kp.find_entries(title=tag, first=True)   

#### KeePass fields explanation
# Fields are read from the KeePass entry here. If you store additional fields in KeePass 
# (for example Description or URL), create a variable and assign it from the entry, e.g. `URL = entry.url`.

    Benutzername = entry.username  
    Web_Passwort = entry.password



# URL placeholder for target site
# Here the URL of the target site must be specified unless you retrieve it from the KeePass entry beforehand (e.g., url = entry.url).
# Concise alternative
# Specify the target URL here, or assign it from the KeePass entry (e.g., url = entry.url).
# 

    URL  = ''


# This part of the script collects all input fields present on the page.
# Important: This script was only tested on a login page with a single login button and standard username/password fields.
# Also note: If you're not working with valid HTTPS certificates, the verify parameter must remain set to False — otherwise the request will fail.

    s = requests.Session()

    login_page = s.get(URL,  verify=False)
    soup = BeautifulSoup(login_page.text, 'html.parser')

    form_data = {}
    for input_tag in soup.find_all('input'):
        name = input_tag.get('name')
        value = input_tag.get('value', '')

        if name:
            form_data[name] = value

    form_data['username'] = Benutzername
    form_data['password'] = Web_Passwort




    r = s.post(f'{URL}', data=form_data, verify=False)

# Login verification logic
# This short section of the script checks whether the user is logged in by looking for elements or data that only appear on authenticated pages.


    soup = BeautifulSoup(r.text, 'html.parser')

    if soup.find(id='logout') is not None:
        print('Logged in successfully')
    else:
        print('failed')

    if Benutzername in r.text:
        print("Logged in successfully, name found")
    else:
        print("failed")




#Ab hier sucht das Script etwas auf der seite um zu verifizieren das er wirklich auf der seite ist


    response = requests.get(URL, verify=False)


    Note = BeautifulSoup(response.text, 'html.parser')
 
    zeilen = soup.select('# Replace the selector with the structure youre looking for (e.g., table rows, divs, spans)')[1:]

    for zeile in zeilen:
        zellen = zeile.find_all('# Adjust this if youre targeting different HTML structures — for example, <th> for headers or <div> for custom layouts.')
        if len(zellen) >= 2 and len(zellen) != None:
            #Name of this variable could be the thing you are Searching for = zellen[1].text.strip()
            if # Name of the Variable you definded in 100 must stand here:

                print(f"Note Gefunden: {# Name of the Variable you definded in 100 must stand here}")

jetzt = datetime.now()
Jetzt_Stunde = jetzt.hour



# Enables looped execution with a 60s timeout — useful for continuous scraping (e.g., weather data). Can be removed for single-run use.


while 5 <= Jetzt_Stunde or 21>= Jetzt_Stunde:
    web_scraping()
    print("In 60 sekunden wird es erneut gestartet")
    time.sleep(60)




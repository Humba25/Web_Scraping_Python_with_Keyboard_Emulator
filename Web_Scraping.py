import requests
import time
from bs4 import BeautifulSoup
from Passwort import Password
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

    kp = PyKeePass(r'', password=Password) # Here the file path to the KeePass database must be specified 

    entry = kp.find_entries(title=tag, first=True)   

#### KeePass fields explanation
# Fields are read from the KeePass entry here. If you store additional fields in KeePass 
# (for example Description or URL), create a variable and assign it from the entry, e.g. `URL = entry.url`.

    Username = entry.username  
    Web_Password = entry.password
    URL = entry.url




# URL  = ''              Here the URL of the target site must be specified unless you retrieve it from the KeePass entry beforehand (e.g., url = entry.url).

   


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

    form_data['username'] = Username
    form_data['password'] = Web_Password



    r = s.post(f'{URL}', data=form_data, verify=False)

# Login verification logic
# This short section of the script checks whether the user is logged in by looking for elements or data that only appear on authenticated pages.


    soup = BeautifulSoup(r.text, 'html.parser')

    if soup.find(id='logout') is not None or Username in r.text:
        print('Logged in successfully')
    else:
        print('failed')


    # --- Web scraping section (generic structure) ---

    response = s.get(URL, verify=False)
    page_soup = BeautifulSoup(response.text, 'html.parser')

    # Select the elements you want to scrape.
    # Example: rows in a table, div blocks, list items, etc.
    elements = page_soup.select('YOUR_CSS_SELECTOR_HERE')

    for element in elements:
        # Extract sub-elements inside each element
        sub_elements = element.find_all('YOUR_HTML_TAG_HERE')

        # Basic safety check
        if not sub_elements:
            continue

        # Example: extract text from the first or second cell
        extracted_value = sub_elements[0].get_text(strip=True)

        # Do something with the extracted value
        # (store it, compare it, print it, return it, etc.)
        print(extracted_value)



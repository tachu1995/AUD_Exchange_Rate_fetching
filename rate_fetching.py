# Import Required Libraries
import requests # Send HTTP Request to Server GET/POST
from bs4 import BeautifulSoup # Find Elements from Server Response, extracing data
from google.oauth2.service_account import Credentials # Work with Google API authentication 
from datetime import datetime # Work With Date and Time
from googleapiclient.discovery import build # Building Google API Services
import time # Use to perform delay, sleep

# Set Google Sheets API scopes and credentials 
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("google_key.json", scopes=scopes)

# Build the Google Sheets service to interact with the Sheets API (v4)
service = build('sheets', 'v4', credentials=creds)

# Define SheetID and Ranges
sheet_id = "1U_rd9VS7XT7VLMOq8eo41hbdahp0w9rFik438aW3uGE"
range_name = 'Sheet1!A1:C'


# Print row from the built sheet
# value_list = sheet.sheet1.row_values(1)


# Declare the address as constant
EZY_URL = "AAAAAAAAAAAAAAAAAAAAAAAAA"
HH_URL = "AAAAAAAAAAAAAAAAAAAAAAAAA"
TECHCOMBANK_URL = "AAAAAAAAAAAAAAAAAAAAAAAAA"
VIETCOMBANK_URL = "AAAAAAAAAAAAAAAAAAAAAAAAA"

# Define payload for POST request to HH API
payload = {"AAAAAAAAAAAAAAAAAAAAAAAAA"}


def rate_fetching():
    # Making requests to the sites using requests library 
    ezy_response = requests.get(EZY_URL)
    hh_response = requests.post(json=payload, url=HH_URL)
    tech_response = requests.get(TECHCOMBANK_URL)
    viet_response = requests.get(VIETCOMBANK_URL)

    
    # Parse the HTML content from the Vietcombank page
    soup = BeautifulSoup(viet_response.content, 'html.parser')

    # Find the <li> element with data-code="AUD"
    aud_element = soup.find('li', {'data-code': 'AUD'})

    tectcombank_rate = tech_response.json()["exchangeRate"]["data"][0]["askRateTM"]
    vietombank_rate = aud_element.get("data-sell-rate")
    hh_rate = hh_response.json()["rateValue"]
    ezy_rate = ezy_response.json()["rate"]

    # Get Date and tinme 
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Prepare the data to be insert into Google Sheet
    data = {
    "values": [
        [date, hh_rate, ezy_rate, tectcombank_rate, vietombank_rate]
    ]
    }
    
    # Attemp to append the data into a new row of the Google Sheet, if failed will try again right away
    try:
        result = service.spreadsheets().values().append(spreadsheetId=sheet_id, range=range_name, valueInputOption='USER_ENTERED', body=data).execute()
        print(result)
        # Sleep for 15 minutes between each call
        time.sleep(900)
    except:
        print("Error")
        
        
if __name__ == "__main__":
    while True:
        rate_fetching()
        

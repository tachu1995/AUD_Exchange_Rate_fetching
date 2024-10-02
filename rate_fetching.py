# Import Required Libraries
import requests # Send HTTP Request to Server GET/POST
from bs4 import BeautifulSoup # Find Elements from Server Response, extracing data
from google.oauth2.service_account import Credentials # Work with Google API authentication 
from datetime import datetime # Work With Date and Time
from googleapiclient.discovery import build # Building Google API Services
import time # Use to perform delay, sleep
from datetime import datetime, timedelta
import threading


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
payload = {"countryCode":"VNM","dmCode":"HOME","currencyCode":"VND"}

# Fetching Ezy Remit Aud-VND Rate
def ezy_aud_rate_fetching():
    try:
        rate = requests.get(EZY_URL)
        return rate.json()["rate"]
    except:
        return "N/A"
    
# Fetching HH AUD-VND Rate
def hh_aud_rate_fetching():
    try:
        rate = requests.post(json=payload, url=HH_URL)
        return rate.json()["rateValue"]
    except:
        return "N/A"
    
# Fetching Techcombank AUD-VND Rate
def tech_aud_rate_fetching():
    try:
        rate = requests.get(TECHCOMBANK_URL)
        return rate.json()["exchangeRate"]["data"][0]["askRateTM"]
    except:
        return "N/A"

# Fetching Vietcombank AUD-VND Rate
def viet_aud_rate_fetching():
    try:
        rate = requests.get(VIETCOMBANK_URL)
        # Parse the HTML content from the Vietcombank page
        soup = BeautifulSoup(rate.content, 'html.parser')
        # Find the <li> element with data-code="AUD"
        aud_element = soup.find('li', {'data-code': 'AUD'})
        return aud_element.get("data-sell-rate")
    except:
        return "N/A"

def rate_fetching():
    # Making requests to the sites using requests library 
    hh_rate = hh_aud_rate_fetching()
    ezy_rate = ezy_aud_rate_fetching()
    tectcombank_rate = tech_aud_rate_fetching()
    vietombank_rate = viet_aud_rate_fetching()
    
    # Get Date and tinme 
    date = datetime.now().strftime("%Y-%m-%d")
    date_hour = datetime.now().strftime("%H:%M")


        # Prepare the data to be insert into Google Sheet
    data = {
        "values": [
            [date, date_hour, hh_rate, ezy_rate, tectcombank_rate, vietombank_rate]
        ]
        }
        
    # Attemp to append the data into a new row of the Google Sheet, if failed will try again right away
    # print(data)
    try:
        result = service.spreadsheets().values().append(spreadsheetId=sheet_id, range=range_name, valueInputOption='USER_ENTERED', body=data).execute()
        # Calculate the time for the next call (5 minutes later)
        next_call_time = (datetime.now() + timedelta(minutes=15)).strftime("%H:%M")
        print(f"{date} {date_hour}: Append to Google Sheet Successfully, next call {next_call_time}")
        # print(result)
        # Sleep for 15 minutes between each call
        time.sleep(900)
    except:
        print("Error: Failed to Append to Google Sheet")
        
        

def stop_loop():
    input("Press Enter to stop...\n")
    global stop
    stop = True

        
if __name__ == "__main__":
    stop = False
    # Create a thread to listen for the stop command
    threading.Thread(target=stop_loop).start()

    while not stop:
        rate_fetching()
        
    print("Process stopped.")
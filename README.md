# Currency Exchange Rate Logger
# Overview
This script fetches currency exchange rates from multiple APIs and logs the data into a Google Sheet. It retrieves rates and updates the Google Sheet with the latest values. The script uses the requests library to make HTTP requests, BeautifulSoup for HTML parsing, and the Google Sheets API for data entry.

Due to privacy, I have removed the URLs. Please find this yourself, this information is public and can be found without much issue. 

# For Google Sheet API:
You Need to get your own API, it is free from Google. 

# Update Log:

Improved Error Handling:

Added try-except blocks to catch errors while fetching data from external sites and when appending data to the Google Sheet.
Added specific error messages to improve debugging ("Error: Failed to fetch data from sites" and "Error: Failed to Append to Google Sheet").
Console Logging:

Implemented a new log message to confirm successful appending of data to Google Sheets ("{date}: Append to Google Sheet Successfully.").
Date and Time Logging:

Now showing the exact date and time when data is fetched and appended to the Google Sheet.
Refactor for Clarity:

Updated print statements to provide clearer feedback in case of failure or success.

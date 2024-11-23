import subprocess
import requests
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from requests.exceptions import RequestException


# Settings
check_interval = 3600  # Check every hour (3600 seconds)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/<URL>/edit'  # Google Spreadsheet URL
alert_threshold = 0.05  # Set an arbitrary threshold for standard deviation (adjust as needed)
custom_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'  # Custom User-Agent


# Google Sheets Authentication
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client



# Function to check if domain is alive using 'nc' command
def check_domain_alive(domain):
    try:
        result = subprocess.run(['nc', '-zv', domain, '443'], capture_output=True, text=True, timeout=1)
        if 'succeeded' in result.stderr:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking domain {domain}: {e}")
        return False


# Function to get website content size (weight) and request speed
def get_website_info(url):
    start_time = time.time()
    response = requests.get(url)
    end_time = time.time()

    weight = len(response.content)  # Website weight in bytes
    speed = end_time - start_time  # Request time in seconds
    return weight, speed


# Function to save results to Google Sheets
def log_to_google_sheets(domain, weight, speed, sheet):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, domain, weight, speed]
    sheet.append_row(row)


# Authenticate and open the Google Sheet
client = authenticate_google_sheets()
result_sheet = client.open_by_url(spreadsheet_url).sheet1
domains_sheet = client.open_by_url(spreadsheet_url).worksheet("domains_to_check")

# Ensure the result sheet has the right headers (if running for the first time)
if result_sheet.row_count == 0:
    result_sheet.append_row(["time", "domain", "weight", "speed"])

# Get domains from the 'cammon_domains' sheet
domains = domains_sheet.col_values(1)  # Get all domains from the first column

# Main loop
while True:
    for domain in domains:
        if not domain.startswith('http'):
            domain = 'http://' + domain  # Add http if not present
        domain_name = domain.replace('http://', '').replace('https://', '')  # Clean domain for 'nc' check

        # Check if the domain is alive using netcat
        if not check_domain_alive(domain_name):
            print(f"Skipping {domain} as it is not responding on port 443.")
            continue  # Skip this domain if it's not alive

        try:
            # Get website weight and speed
            weight, speed = get_website_info(domain)

            # Log to Google Sheets
            log_to_google_sheets(domain, weight, speed, result_sheet)
            print(f"Logged {domain} - Weight: {weight} bytes, Speed: {speed:.2f} seconds")

        except RequestException as e:
            # Catch network-related errors and skip
            print(f"Skipping {domain} due to connection error: {e}")
            continue  # Skip this domain and move to the next

    # Wait for the next check
    time.sleep(check_interval)

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sublist3r
import time

def get_subdomains(domain):
    try:
        # Attempt to fetch subdomains
        subdomains = sublist3r.main(domain, 40, savefile=None, ports=None, silent=False, verbose=True, enable_bruteforce=False, engines=None)
        return subdomains
    except IndexError as e:
        print(f"Error fetching subdomains for {domain}: {e}")
        return []  # Return an empty list if there's an error




def main():
    # Use your credentials file here
    credentials_file = 'credentials.json'

    # Define the scope and authenticate
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)

    # Open the Google Spreadsheet
    spreadsheet_url = 'https://docs.google.com/spreadsheets/d/<URL>/edit'
    spreadsheet = client.open_by_url(spreadsheet_url)

    # Get the "common_domains" sheet
    common_domains_sheet = spreadsheet.worksheet('common_domains')
    domains = common_domains_sheet.col_values(1)  # Assuming domains are in the first column

    # Get the "domains_to_check" sheet
    domains_to_check_sheet = spreadsheet.worksheet('domains_to_check')

    # Clear the sheet before posting new results
    domains_to_check_sheet.clear()
    print("The 'domains_to_check' sheet has been cleared.")

    # Collect all rows to be written in a batch
    rows_to_write = []

    for domain in domains:
        print(f"Processing domain: {domain}")
        subdomains = get_subdomains(domain)
        if subdomains:
            for subdomain in subdomains:
                rows_to_write.append([subdomain])  # Add subdomains to the list

    # Write all rows in one go
    if rows_to_write:
        domains_to_check_sheet.append_rows(rows_to_write)
        print(f"Subdomains have been written to the 'domains_to_check' sheet.")

if __name__ == '__main__':
    main()

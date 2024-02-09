import os
import configparser
import requests
import time


# Get the absolute path of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path of the configuration file
config_file_path = os.path.join(script_dir, "timezone-update-config.ini")

# Load the configuration file
config = configparser.ConfigParser()
config.read(config_file_path)

#EI API Variables
EI_FQDN = config.get("Agfa", "EI_FQDN")
EI_USER = config.get("Agfa", "EI_USER")
EI_PASSWORD = config.get("Agfa", "EI_PASSWORD")
TOKEN = None


#get api auth token
def get_token():
    global TOKEN
    print(f"Getting a token for user {EI_USER}")
    auth_url = f"https://{EI_FQDN}/authentication/token"
    params = {"user": EI_USER, "password": EI_PASSWORD}

    try:
        response = requests.get(auth_url, params=params, verify=True)
        response.raise_for_status()
        TOKEN = response.text.split('CDATA[')[1].split(']]')[0]
        print("Token acquired successfully.")
    except requests.RequestException as e:
        print(f"Failed to acquire token. Error: {str(e)}")
        raise


# Function to search for external system using API call
def search_external_system(exsys_code):
    try:
        search_url = f"https://{EI_FQDN}/configuration/v1/externalSystems?code={exsys_code}"
        headers = {"Authorization": f"Bearer {TOKEN}"}
        response = requests.get(search_url, headers=headers, verify=True)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to search for external system. Error: {str(e)}")
        raise


# Function to update timezone for external system using API call
def update_timezone(exsys_code, new_timezone, original_system_details):
    try:
        # Extract the first element of the list
        system_to_update = original_system_details[0]

        # Update the timezone field in the original JSON response
        system_to_update["timezone"] = new_timezone

        update_url = f"https://{EI_FQDN}/configuration/v1/externalSystems/{exsys_code}"
        headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

        # Send the entire updated JSON object in the PUT request
        response = requests.put(update_url, headers=headers, json=system_to_update, verify=True)
        response.raise_for_status()

        print(f"Timezone updated successfully to {new_timezone}")
    except requests.RequestException as e:
        print(f"Failed to update timezone. Error: {str(e)}")
        raise


# Function to get and display external system details
def display_external_system_details(system):
    # Display relevant details from the API response
    print(f"Name: {system['name']}")
    print(f"Code: {system['code']}")
    print(f"Current Timezone: {system['timezone']}")
    # Add any other details you want to display




# Main script
if __name__ == "__main__":
    # Ask user for the external system code
    exsys_code = input("Enter external system code: ")

    # Get API authentication token
    get_token()

    # Search for external system and capture the entire JSON response
    initial_system_details = search_external_system(exsys_code)

    # Display current details
    display_external_system_details(initial_system_details[0])
    #print(initial_system_details)

    # Ask user to choose a timezone from the pick list
    new_timezone = input("Choose a timezone (etz/ctz/mtz): ")
    if new_timezone == "etz":
        new_timezone = "America/New_York"
    elif new_timezone == "ctz":
        new_timezone = "America/Chicago"
    elif new_timezone == "mtz":
        new_timezone = "America/Denver"
    else:
        print("Invalid timezone choice. Exiting.")
        exit()

    # Update timezone for external system
    update_timezone(exsys_code, new_timezone, initial_system_details)
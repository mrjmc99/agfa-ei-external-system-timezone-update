# External System Timezone Updater

This script facilitates the update of timezones for external systems through the use of the Agfa EI (Enterprise Imaging) API.

## Prerequisites

Before running the script, ensure the following:

- Python is installed on your system.
- Install the required Python packages using the following command:

  ```bash
  pip install -r requirements.txt
  ```

## Configuration

The script uses a configuration file named `timezone-update-config.ini` to store Agfa EI API parameters. Ensure that this file is present in the same directory as the script. Example configuration parameters include:

- Agfa EI API Variables (EI_FQDN, EI_USER, EI_PASSWORD)

## Usage

Run the script using the following command:

```bash
python timezone_update_script.py
```

The script performs the following actions:

1. **Authentication**: Obtains an authentication token from Agfa EI API using user credentials.

2. **External System Search**: Searches for an external system using the provided external system code.

3. **Display Current Details**: Displays the current details of the external system, including its name, code, and current timezone.

4. **Timezone Selection**: Prompts the user to choose a new timezone from the predefined options (etz, ctz, mtz).

5. **Timezone Update**: Updates the timezone for the external system based on the user's selection.

## Script Logic

The script is structured as follows:

- **Configuration Loading**: Loads configuration parameters from `timezone-update-config.ini`.
- **Authentication**: Obtains an authentication token for Agfa EI API.
- **External System Search**: Searches for an external system using the provided code.
- **Display Current Details**: Displays current details of the external system.
- **Timezone Selection**: Prompts the user to choose a new timezone.
- **Timezone Update**: Updates the timezone for the external system using the Agfa EI API.

## Error Handling

The script includes error handling for various scenarios, such as failed token acquisition, external system search failure, and timezone update failure.

## Support and Issues

For any issues or questions, please create an issue in the [GitHub repository](https://github.com/mrjmc99/agfa-ei-external-system-timezone-update).

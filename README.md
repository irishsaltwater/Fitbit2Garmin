# Fitbit2Garmin
This collection of Python scripts can be used to automatically pull data from a Fitbit account (once authenticated) and send it to a Garmin account.

This is a work in progress. For details see

## Usage
This app is designed for personal use, rather than deployment for wide-scale usage. If you want to use it, then you must register your own app on https://dev.fitbit.com/ and set the appropriate Client ID and Client Secret values in the config file.

Once done, obtain an authorization token (easiest done with the online Fitbit API Debug Tool) and pass that value to the script as a startup parameter

### Completed
* Logic to authenticate with Fitbit API given an authorization code as a runtime parameter, and appropriate values in the _config.ini_ file

### To Do
* Logic to parse data from Fitbit and send to Garmin
* Logic to automate this process on a regular basis
* Python install file
* Full Readme
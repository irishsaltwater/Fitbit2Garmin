# Class interfaces with Fitbit API
import logging
import base64
import requests
from datetime import datetime
import configparser

# Lets store these values in memory #supersecure
access_token = ''
refresh_token = ''

# These are static values that will not change
# The base64 encoding of them could be stored in the property file directly, but where's the fun in that?
client_id = ''
client_secret = ''

# The redirect URL used for requesting the initial authorization token
redirect_uri = 'http://localhost:9090'
fitbit_token_url = 'https://api.fitbit.com/oauth2/token'
fitbit_user_api_url = 'https://api.fitbit.com/1/user/-/body/log/'
fitbit_user_api_body_weight = 'weight/date/[date].json'


def init(authorization_code):
    __init_variables()
    __authenticate(authorization_code)


# Get the first access token
def __authenticate(authorization_code):
    global access_token, refresh_token
    logging.debug('Getting access token using authorization code')

    header = __build_basic_authorization_header()

    # Set body values
    body_parameters = {'code': authorization_code, 'grant_type': 'authorization_code', 'client_id': client_id, 'redirect_uri': redirect_uri}

    # Send the request to the Fitbit token URL, the response will contain an access token and refresh token
    response = requests.post(fitbit_token_url, headers=header, data=body_parameters)
    if response.status_code != 200:
        logging.error('Error requesting initial authorization token')
        logging.error(response.text)
        exit(-1)

    # Store these in global variables for access by other methods
    access_token = response.json()['access_token']
    refresh_token = response.json()['refresh_token']


# Read needed values from properties file
def __init_variables():
    global client_id, client_secret

    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini')
    client_id = config['FITBIT']['client_id']
    client_secret = config['FITBIT']['client_secret']

    __verify_init_variables()

    logging.debug('Client ID and Client Secret read from config file as %s and %s', client_id, client_secret)


def __verify_init_variables():
    if client_id is None:
        logging.error('Client ID is null, unable to proceed')
        exit(-1)
    if client_secret is None:
        logging.error('Client Secret is null, unable to proceed')
        exit(-1)


# Function sends request to Fitbit API to get user data
# Will invoke token refresh if necessary
def get_data():
    logging.debug('Getting Data from Fitbit')

    response = __send_data_request_to_fitbit()

    # May need to renew token
    if response.status_code == 401:
        logging.info('Unauthorized error, renewing token')
        __renew_token()
        response = __send_data_request_to_fitbit()

    # If still not ok after second attempt, something unfixable has happened
    if response.status_code != 200:
        logging.error('Unable to successfully get data from Fitbit API')
        logging.error(response.text)
        exit(-1)

    return response.json()


# Builds data request and sends to fitbit, returning the response
def __send_data_request_to_fitbit():
    headers = {'Authorization': 'Bearer %s' % access_token}

    # Get weight for today's date by building appropriate URL
    date = datetime.today().strftime('%Y-%m-%d')
    full_url = fitbit_user_api_url + fitbit_user_api_body_weight.replace('[date]', date)
    # todo: add in something that reduces the recorded weight by like......15% or so
    return requests.get(full_url, headers=headers)


# Renews the access token using the refresh token
def __renew_token():
    global access_token, refresh_token
    logging.debug('Refreshing access token')

    header = __build_basic_authorization_header()

    # Set body values
    body_parameters = {'refresh_token': refresh_token, 'grant_type': 'refresh_token'}

    # Send the request to the Fitbit token URL, the response will contain an access token and refresh token
    response = requests.post(fitbit_token_url, headers=header, data=body_parameters)
    if response.status_code != 200:
        logging.error('Unable to successfully renew token through Fitbit API')
        logging.error(response.text)
        exit(-1)

    access_token = response.json()['access_token']
    refresh_token = response.json()['refresh_token']


# Builds the Basic auth header used for requesting access tokens
def __build_basic_authorization_header():
    # Yes, could be doing this all with an OAuth library, but coding it this way works well as an educational tool
    authorization_string = '%s:%s' % (client_id, client_secret)
    # Python expects a bytes-like object for b64 encoding. Can do that simply by encoding it as ascii
    base64_authorization_string = base64.b64encode(authorization_string.encode('ascii'))
    return {'Authorization': 'Basic %s' % base64_authorization_string.decode('ascii')}


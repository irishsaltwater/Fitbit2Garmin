import FitbitApi
import logging
import sys
# Phase 1:
# Authenticate with Fitbit - get access token and refresh token - manual step
# Seed application with access token and refresh token - manual step
# get data from fitbit
# if fail, use refresh token and try again
# Once a day, sync data

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='a'
                        , format='%(name)s - %(levelname)s - %(message)s')
    logging.info("Starting Fitbit2Garmin!")

    # Argument 0 is always the program name
    authorization_token = sys.argv[1]
    if authorization_token is None:
        logging.info('Authorization token not passed as program argument, unable to run')
        exit(-1)

    # Call initial setup to access Fitbit API once when app starts
    FitbitApi.init(authorization_token)

    # This needs to be called on a regular schedule
    print(FitbitApi.get_data())
    print('Done')
    # pass info to Garmin class
    #### end of loop
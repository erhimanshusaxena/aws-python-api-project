import json
import logging
import boto3
import os
from datetime import datetime
from src.lib import helper
from boto3.dynamodb.conditions import Key

# Initialising Boto3 DynamoDB object.
dynamodb = boto3.resource('dynamodb')
# Getting Environment variables
table = dynamodb.Table(os.environ['DEVICE_TABLE'])
AUTH_ALGO = os.environ['AUTH_ALGO']
AUTH_SECRET = os.environ['AUTH_SECRET']


# scanning sensor data table for dates between fromm_date and to_date
def get_sensor_data(from_date, to_date):
    print(f"From date: {from_date}")
    print(f"To date: {to_date}")
    try:
        message = table.scan(
            FilterExpression=Key("timestamp").between(str(from_date), str(to_date))
        )
        message = message.get("Items")
        logging.debug(message)
    except Exception as e:
        message = f"Error occurred getting data from table: {e}"
        logging.error(message)

    return message


# Handler method
def query(event, context):
    token = event.get('headers').get('x-auth-token')
    # Checking if token is present and its valid token
    if token and helper.verify_token(token):
        query_params = event.get('queryStringParameters')
        # From and To date should be of format of epoch time so date time should be converted
        from_date = datetime.strptime(query_params.get('from_date'), '%m/%d/%y %H:%M:%S').timestamp()
        to_date = datetime.strptime(query_params.get('to_date'), '%m/%d/%y %H:%M:%S').timestamp()

        # Checking from_date and to_date of sensor date
        # if both present process get request
        # else return error message for empty from_date and to_date
        if not from_date or not to_date:
            code = 400
            message = 'Please provide "from_date" and "to_date"'
        else:
            message = get_sensor_data(from_date, to_date)
            code = 200
    else:
        code = 400
        message = "Invalid token!"

    response = {"statusCode": code, "body": json.dumps(message)}

    return response

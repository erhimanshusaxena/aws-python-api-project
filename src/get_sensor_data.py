import json
import logging
import boto3
import os
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
    try:
        message = table.scan(
            FilterExpression=Key("timestamp").between(from_date, to_date)
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
        from_date = query_params.get('from_date')
        to_date = query_params.get('to_date')

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

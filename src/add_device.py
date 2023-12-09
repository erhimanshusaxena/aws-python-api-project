import json
import logging
import boto3
import os
from src.lib import helper

# Initialising Boto3 DynamoDB object.
dynamodb_client = boto3.client('dynamodb')
# Getting Environment variables
DEVICE_TABLE = os.environ['DEVICE_TABLE']
AUTH_ALGO = os.environ['AUTH_ALGO']
AUTH_SECRET = os.environ['AUTH_SECRET']


# Inserting received data from request to Device table in DynamoDB
def add_device(device_id, name, desc):
    # Checking if same device is already added
    # if not added process insert query
    # else return message Device already added.
    item = helper.get_identifier(device_id)
    if not item:
        try:
            dynamodb_client.put_item(
                TableName=DEVICE_TABLE,
                Item={'id': {'S': device_id},
                      'device_name': {'S': name},
                      'device_description': {'S': desc}
                      }
            )
            message = "Sensor added successfully!"
            logging.debug(message)
        except Exception as e:
            message = f"Error occurred putting data to table: {e}"
            logging.error(message)
    else:
        message = "Device already added!"

    return message


# Handler function
def query(event, context):
    # getting auth token from headers
    token = event.get('headers').get('x-auth-token')

    # Checking if token is present and its valid token
    if token and helper.verify_token(token):
        body = json.loads(event["body"])

        device_id = body.get('id')
        name = body.get('device_name')
        description = body.get('device_description')

        # Checking device_id of device to be added and it's name
        # if both present process add request
        # else return error message for empty name and id
        if not device_id or not name:
            code = 400
            message = 'Please provide both "id" and "name"'
        else:
            message = add_device(device_id, name, description)
            code = 200
    else:
        code = 400
        message = "Invalid token!"

    response = {"statusCode": code, "body": json.dumps(message)}

    return response

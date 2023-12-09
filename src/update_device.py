import json
import logging
import boto3
import os
from src.lib import helper

# Initialising Boto3 DynamoDB object.
dynamodb = boto3.resource('dynamodb')
# Getting Environment variables
table = dynamodb.Table(os.environ['DEVICE_TABLE'])
AUTH_ALGO = os.environ['AUTH_ALGO']
AUTH_SECRET = os.environ['AUTH_SECRET']


# Checking of Device already exist in database then update
# else raise error message that device doesn't exist
def update_device(device_id, new_name):
    item = helper.get_identifier(device_id)
    if item:
        print(item)
        try:
            table.update_item(
                Key={'id': str(device_id)},
                UpdateExpression='SET device_name = :new_name',
                ExpressionAttributeValues={
                    ':new_name': str(new_name)
                }
            )
            message = "Successfully update data!"
            logging.debug(message)
        except Exception as e:
            message = f"Error occurred updating data to table: {e}"
            logging.error(message)
    else:
        message = "Device does not exist!"

    return message


# Handler method
def query(event, context):
    token = event.get('headers').get('x-auth-token')
    # Checking if token is present and its valid token
    if token and helper.verify_token(token):
        body = json.loads(event["body"])
        new_name = body.get('device_new_name')
        device_id = body.get('id')

        # Checking new_name of device to be updated, and it's devise_id
        # if both present process add request
        # else return error message for empty devise_id and new_name
        if not new_name or not device_id:
            code = 400
            message = 'Please provide "old name" "new name" and "device_id"'
        else:
            message = update_device(device_id, new_name)
            code = 200
    else:
        code = 400
        message = "Invalid token!"

    response = {"statusCode": code, "body": json.dumps(message)}

    return response

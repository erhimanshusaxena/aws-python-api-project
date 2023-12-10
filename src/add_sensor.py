import json
import logging
import boto3
import os
import time
from src.lib import helper

# Initialising Boto3 DynamoDB object.
dynamodb_client = boto3.client('dynamodb')
# Getting Environment variables
SENSOR_TABLE = os.environ['SENSOR_TABLE']
AUTH_ALGO = os.environ['AUTH_ALGO']
AUTH_SECRET = os.environ['AUTH_SECRET']


# Inserting received data from request to Sensor table in DynamoDB
def add_sensor(sensor_id, device_id, name="Sensor Name", sensor_type="Temperature", sensor_value="30"):
    try:
        dynamodb_client.put_item(
            TableName=SENSOR_TABLE,
            Item={'id': {'S': sensor_id},
                  'device_id': {'S': device_id},
                  'sensor_name': {'S': name},
                  'sensor_type': {'S': sensor_type},
                  'sensor_value': {'S': sensor_value},
                  'timestamp': {'S': str(time.time())}
                  }
        )
        message = "Device added successfully!"
        logging.debug(message)
    except Exception as e:
        message = f"Error occurred putting data to table: {e}"
        logging.error(message)

    return message


# Handler function
def query(event, context):
    token = event.get('headers').get('x-auth-token')
    # Checking if token is present and its valid token
    if token and helper.verify_token(token):
        body = json.loads(event["body"])

        # Getting sensor data from request body
        sensor_id = body.get('id')
        device_id = body.get('device_id')
        name = body.get("sensor_name")
        sensor_type = body.get("sensor_type")
        sensor_value = body.get("sensor_value")
        # Checking sensor_id of sensor to be added, and it's devise_id
        # if both present process add request
        # else return error message for empty devise_id and sensor_id
        if not sensor_id or not device_id:
            code = 400
            message = 'Please provide at-least both "sensor id" and "device id"'
        else:
            message = add_sensor(sensor_id, device_id, name, sensor_type, sensor_value)
            code = 200
    else:
        code = 400
        message = "Invalid token!"

    response = {"statusCode": code, "body": json.dumps(message)}

    return response

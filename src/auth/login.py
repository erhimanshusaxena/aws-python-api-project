import json
import boto3
import os
import jwt
from src.lib import helper

# Initialising Boto3 DynamoDB object.
dynamodb_client = boto3.client('dynamodb')
# Getting Environment variables
USER_TABLE = os.environ['USER_TABLE']
AUTH_ALGO = os.environ['AUTH_ALGO']
AUTH_SECRET = os.environ['AUTH_SECRET']

# JWT Header for token creation
header = {
    "alg": AUTH_ALGO,
    "typ": "JWT"
}


# Handler method for lambda
def query(event, context):
    # Getting request body from event object
    body = json.loads(event["body"])
    # request body parameters from POST request
    email = body.get('email')
    password = body.get('password')
    # Calling helper method to check if email exist in database
    item = helper.get_email(email)

    # If email is not present in database or password provided doesn't match
    # should raise incorrect credentials error
    # else
    # Create payload from user object and prepare auth token
    if not item or item['password']['S'] != str(password):
        code = 422
        message = "Invalid email or password"
    else:
        code = 200
        payload = {
            "sub": "auth",
            "email": item['email']['S'],
            "id": item['id']['S']
        }
        # Encoding payload with custom secret, AUTH_ALGO and Header to create token
        token = jwt.encode(payload, AUTH_SECRET, algorithm=AUTH_ALGO, headers=header)
        # Sending token with successful login response
        message = {
            "token": str(token),
            "message": "Logged Successfully!"
        }

    response = {"statusCode": code, "body": json.dumps(message)}

    return response

import json
import boto3
import os
import uuid
from src.lib import helper

# Initialising Boto3 DynamoDB object.
dynamodb_client = boto3.client('dynamodb')
# Getting Environment variable for USER_TABLE
USER_TABLE = os.environ['USER_TABLE']


# method for checking if email already exist in database
def email_exist(email):
    item = helper.get_email(email)
    if item:
        return True

    return False


# Creating user record for email registration
def register_user(email, password):
    # Creating a random UUID for user table as primary key
    user_id = uuid.uuid4()
    # Creating record in DynamoDB database user table
    dynamodb_client.put_item(
        TableName=USER_TABLE,
        Item={
            'id': {'S': str(user_id)},
            'email': {'S': email},
            'password': {'S': password}
        }
    )


# Handler method
def query(event, context):
    # Getting request body object from event object data
    body = json.loads(event['body'])
    email = body.get('email')
    password = body.get('password')
    password_confirmation = body.get('password_confirmation')
    code = 422

    # If either of the email or password is not present or empty
    # should return error message for incorrect email password
    if not email or not password:
        message = 'Please provide both email and password'
    else:
        # If email is not valid returning invalid email error message
        if not helper.check_email(email):
            message = "Please provide valid email"
        else:
            # If email already exist in database return error message
            # email already exists.
            if email_exist(email):
                message = "Email already exists!"
            else:
                # If provided password is invalid returning error validate password
                if helper.validate_password(password):
                    # if password match password confirmation register user
                    # else
                    # raise password doesn't match error
                    if password == password_confirmation:
                        code = 200
                        register_user(email, password)
                        message = "Registration Successful!"
                    else:
                        message = "Password doesn't match password confirmation."
                else:
                    message = ("Password should contain at-least 8 letters including one small, one atleast capital and "
                               "one numerical letter.")

    response = {"statusCode": code, "body": message}

    return response

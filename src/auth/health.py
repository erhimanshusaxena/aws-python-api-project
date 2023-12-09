import json


# Checking Health of the Server
def query(event, context):
    body = {
        "message": "Server is healthy!",
        "input": event,
    }
    # Returning status code and body in json format as response
    response = {"statusCode": 200, "body": json.dumps(body)}

    return response

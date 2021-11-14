import json

body={}

def handler(event, context):
    body = {
        "message": "Hellow world!",
        "input": event
    }
    response ={
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
import datetime
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb=boto3.resource('dynamodb')
def lambda_handler(event, context):
    table=dynamodb.Table('logs')
    server=event.get('monitor',None)
    start=event.get('start',None)
    stop=event.get('stop',None)
    if (server is None) or (start is None):
        return {
            'statusCode':400,
            'body':json.dumps(({'message':'Request must contain monitor and start parameters'}))
        }

    start_timestamp=start + " 00:00:00"
    if stop is None:
        stop_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        stop_timestamp=stop + " 00:00:00"
    query=None

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello worlds1",
            # "location": ip.text.replace("\n", "")
        }),
    }
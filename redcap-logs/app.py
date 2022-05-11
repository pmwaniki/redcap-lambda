import datetime
import decimal
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o,decimal.Decimal):
            return str(o)
        return super(DecimalEncoder,self).default(o)

dynamodb=boto3.resource('dynamodb')
def lambda_handler(event, context):
    print(">>>>",event)
    table=dynamodb.Table('logs')
    server=event['queryStringParameters'].get('monitor',None)
    start=event['queryStringParameters'].get('start',None)
    stop=event['queryStringParameters'].get('stop',None)
    if (server is None) or (start is None):
        return {
            'statusCode':400,
            'body':json.dumps(({'message':'Request must contain monitor and start parameters'}))
        }

    start_timestamp=start + " 00:00:00"
    if stop is None:
        stop_timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        stop_timestamp=stop + " 23:59:59"
    response=table.query(KeyConditionExpression=Key('Server').eq(server) & Key('TimeStamp').between(start_timestamp,stop_timestamp),
                )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "logs": response['Items'],
            # "location": ip.text.replace("\n", "")
        },cls=DecimalEncoder),
    }
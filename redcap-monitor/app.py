import logging
import datetime
import boto3
import requests


logger = logging.getLogger()
logger.setLevel(logging.INFO)

client=boto3.resource("dynamodb")
timeout=3
servers=[
    {'servername':'datahubweb','url':'https://data.datahubweb.com/redcap/'},
]

def redcap_website(url,timeout=5):
    try:
        req=requests.get(url,timeout=timeout)
    except:
        return {'code':0,'message':"Request call failed"}
    status_code=req.status_code
    if status_code==200:
        return {'code':200,'message':'OK'}
    else:
        return {'code':status_code,'message':req.text}

def lambda_handler(event, context):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fetch=redcap_website(url='https://data.datahubweb.com',timeout=timeout)
    table = client.Table('logs')


    status_code=fetch['code']
    message=fetch['message']
    server="datahubweb"
    table.put_item(
        Item={
            'Server':server,
            'TimeStamp':timestamp,
            'StatusCode':status_code,
            'Message':message
        }
    )
    print(">>>>logging something")
    logger.info("Full event: %s", event)

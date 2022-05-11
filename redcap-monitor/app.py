import grequests
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
    {'servername':'hsu-redcap','url':"https://hsu.kemri-wellcome.org/redcap/"},
    {'servername':'search-redcap','url':"https://searchtrial.kemri-wellcome.org/"},
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

def get_websites(servers,timeout=5):
    req=[grequests.get(site['url'],timeout=timeout) for site in servers ]
    results=grequests.map(req)
    results2=[]
    for i in range(len(results)):
        status_code=results[i].status_code
        if status_code == 200:
            results2.append({'server':servers[i]['servername'],'code': 200, 'message': 'OK'})
        else:
            results2.append({'server':servers[i]['servername'],'code': status_code, 'message': results[i].text})
    return results2


def lambda_handler(event, context):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results=get_websites(servers=servers,timeout=timeout)
    table = client.Table('logs')
    for result in results:
        status_code=result['code']
        message=result['message']
        server=result["server"]
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

import boto3
import json
import random

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
TABLE = 'Yeetcode2020-Data'

def lambda_handler(event, context):

    clientID = event['requestContext']['connectionId']
    data_packet = event['body']
    data_packet = json.loads(data_packet)
    print(data_packet)

    # Get party ID
    if('partyID' in data_packet):
        partyID = data_packet['partyID']
    else:
        return {
            "statusCode": 500,
            "body": "Party ID not included"
        }
    
    try:
        res = dynamodb.get_item(TableName=TABLE, Key={
            'partyID': {
                'S': partyID
            }
        })
        if('Item' not in res):
            return {
                "statusCode": 500,
                "body": "PartyID does not exist"
            }
    except Exception as err:
        print(err)
        return {
            "statusCode": 500,
            "body": "Error getting party details"
        }
    
    # Insert empty object into database
    try:
        res = dynamodb.update_item(TableName=TABLE,
            Key={
                "partyID": {
                    "S": partyID
                }
            },
            ExpressionAttributeValues={
                ':c': {
                    "L": [{
                        "S": clientID
                    }]
                }
            },
            UpdateExpression="set clients = list_append(clients, :c)"
        )
        print('Added client to game')
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": ""
        }

    return {
        'statusCode': 200,
        'body': "DONE"
    }
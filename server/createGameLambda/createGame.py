import boto3
import json
import random

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
TABLE = 'Yeetcode2020-Data'

def get_party_id():
    partyID = str(random.randint(0, (10**6)-1))  # Generate 9 digit code
    if(len(partyID) < 9):
        remain = 9 - len(partyID)
        partyID = '0'*remain + partyID


def lambda_handler(event, context):

    data_packet = event['body']
    data_packet = json.loads(data_packet)
    print(data_packet)

    partyID = get_party_id()  # Generate 9 digit code
    
    print('Party ID:', partyID)
    # While ensure that partyID doesn't exist
    while True:
        try:
            res = dynamodb.get_item(TableName=TABLE, Key={
                'partyID': {
                    'S': partyID
                }
            })
            partyID = get_party_id()
        except Exception as err:
            # Break if partyID is unique
            break
    
    # Insert empty object into database
    try:
        res = dynamodb.put_item(TableName=TABLE, Item={
            "partyID": {
                "S": partyID
            },
            "leaderboard": {
                "M": {}  # Empty leaderboard
            },
            "clients": {
                "L": []
            }
        })
        print('Created new game entry in table')
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
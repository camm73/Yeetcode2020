import boto3
import json
import random

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
apiMgmt = boto3.client('apigatewaymanagementapi', region_name='us-east-1', endpoint_url='https://8mvqn1b54i.execute-api.us-east-1.amazonaws.com/production/')
TABLE = 'Yeetcode2020-Data'

def get_party_id():
    partyID = str(random.randint(10**5, (10**6)-1))  # Generate 9 digit code
    return partyID


def lambda_handler(event, context):
    clientID = event['requestContext']['connectionId']
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
            if('Item' not in res):
                break
            partyID = get_party_id()
        except Exception as err:
            print(err)
            break  # TODO: Probably want to just return error
    
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

    # Send response with party id to user
    ret_packet = {
        "action": "createSuccess",
        "partyID": partyID
    }

    send_to_client(ret_packet, clientID)

    return {
        'statusCode': 200,
        'body': "DONE"
    }

def send_to_client(data, connectionId):
    # Send leaderboard to user
    apiMgmt.post_to_connection(
        Data=json.dumps(data),
        ConnectionId=connectionId
    )
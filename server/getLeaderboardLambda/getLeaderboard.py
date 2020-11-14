import boto3
import json
import random

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
apiMgmt = boto3.client('apigatewaymanagementapi', region_name='us-east-1', endpoint_url='https://8mvqn1b54i.execute-api.us-east-1.amazonaws.com/production/')
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

    leaderboard = res['Item']['leaderboard']['M']

    ret_packet = {
        "action": "leaderboardUpdate",
        "leaderboard": leaderboard
    }

    # Send leaderboard to user
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
import boto3
import json
import random

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
apiMgmt = boto3.client('apigatewaymanagementapi', region_name='us-east-1', endpoint_url='https://8mvqn1b54i.execute-api.us-east-1.amazonaws.com/production/')
TABLE = 'Yeetcode2020-Data'

def lambda_handler(event, context):

    host_id = event['requestContext']['connectionId']
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

    # Get game object
    try:
        res = dynamodb.get_item(TableName=TABLE, Key={
            'partyID': {
                'S': partyID
            }
        })
        if('Item' not in res):
            return {
                "statusCode": 200,
                "body": "Game already deleted"
            }
    except Exception as err:
        print(err)
        return {
            "statusCode": 500,
            "body": "Party ID does not exist"
        }

    game_obj = res['Item']
    clients = game_obj['clients']['L']

    # Disconnect all users
    for entry in clients:
        connID = entry['S']
        # Skip the host
        if(connID == host_id):
            print('Skipping host:', connID)
            continue
        try:
            apiMgmt.delete_connection(ConnectionId=connID)
        except Exception as e:
            print(e)
            print('Failed to disconnect:', connID)

    
    # Insert empty object into database
    try:
        dynamodb.delete_item(
            TableName=TABLE,
            Key={
                "partyID": {
                    "S": partyID
                }
            }
        )
        print('Deleted game entry in table')
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": ""
        }

    # Disconnect host
    try:
        apiMgmt.delete_connection(ConnectionId=host_id)
    except Exception as e:
        print(e)
        print('Failed to disconnect host:', host_id)
    

    return {
        'statusCode': 200,
        'body': "DONE"
    }
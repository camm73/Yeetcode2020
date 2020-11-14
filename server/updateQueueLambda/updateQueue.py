import boto3
import json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
apiMgmt = boto3.client('apigatewaymanagementapi', region_name='us-east-1', endpoint_url='https://8mvqn1b54i.execute-api.us-east-1.amazonaws.com/production/')
TABLE = 'Yeetcode2020-Data'

def lambda_handler(event, context):

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

    # Get spotify token
    if('spotifyToken' in data_packet):
        spotify_token = data_packet['spotifyToken']
    else:
        return {
            "statusCode": 500,
            "body": "Spotify auth token not provided"
        }

    # Get the Leaderboard
    try:
        res = dynamodb.get_item(TableName=TABLE, Key={
            'partyID': {
                'S': partyID
            }
        })
    except Exception as err:
        print(err)
        return {
            "statusCode": 500,
            "body": "Party ID does not exist"
        }

    # Extract leaderboard dict
    leaderboard = res['Item']['leaderboard']['M']

    # TODO: Determine which song in leaderboard is the lowest
    
    songURI = 'here'  # TODO: CHANGE WHEN DONE TESTING

    # ========================================================

    # Remove chosen song from leaderboard
    try:
        update_res = dynamodb.update_item(
            TableName=TABLE,
            Key={
                'partyID': {
                    'S': partyID
                }
            },
            ExpressionAttributeNames={
                "#uri": songURI
            },
            UpdateExpression="REMOVE leaderboard.#uri",
            ReturnValues='ALL_NEW'
        )
        print(update_res)
    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": "Failed to remove song from leaderboard"
        }

    # Get newly updated data
    updated_data = update_res['Attributes']
    leaderboard = updated_data['leaderboard']['M']
    clients = updated_data['clients']['L']

    ret_packet = {
        "action": "leaderboardUpdate",
        "leaderboard": leaderboard
    }

    # Send to clients
    for entry in clients:
        connID = entry['S']
        send_to_client(ret_packet, connID)

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
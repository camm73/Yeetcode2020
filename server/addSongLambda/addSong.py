import boto3
import json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
apiMgmt = boto3.client('apigatewaymanagementapi', region_name='us-east-1', endpoint_url='https://8mvqn1b54i.execute-api.us-east-1.amazonaws.com/production/')
TABLE = 'Yeetcode2020-Data'

def lambda_handler(event, context):

    clientID = event['requestContext']['connectionId']
    data_packet = event['body']
    data_packet = json.loads(data_packet)
    print(data_packet)

    # Get song URI
    if('songURI' in data_packet):
        songURI = data_packet['songURI']
    else:
        return {
            'statusCode': 500,
            'body': "Song URI not provided"
        }
    
    # Get party ID
    if('partyID' in data_packet):
        partyID = data_packet['partyID']
    else:
        return {
            "statusCode": 500,
            "body": "Party ID not included"
        }

    # Add song URI to leaderboard if not already in the list
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

    # Increment value if it already exists
    if(songURI in res['Item']['leaderboard']['M']):
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
                ExpressionAttributeValues={
                    ":v": {
                        "N": "1"
                    }
                },
                UpdateExpression="set leaderboard.#uri = leaderboard.#uri + :v"
            )
            print(update_res)
        except Exception as e:
            print(e)
    else:
        # Add song to leaderboard (set votes to 1)
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
                ExpressionAttributeValues={
                    ":v": {
                        "N": "1"
                    }
                },
                UpdateExpression="set leaderboard.#uri = :v",
                ReturnValues='ALL_NEW'
            )
            print(update_res)
        except Exception as e:
            print(e)

    updated_data = update_res['Attributes']
    leaderboard = updated_data['leaderboard']['M']

    ret_packet = {
        "action": "leaderboardUpdate",
        "leaderboard": leaderboard
    }

    # Send to client
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
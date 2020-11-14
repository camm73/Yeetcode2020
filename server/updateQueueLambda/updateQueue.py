import boto3
import json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
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

    return {
        'statusCode': 200,
        'body': "DONE"
    }
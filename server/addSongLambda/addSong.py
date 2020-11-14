import boto3
import json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
TABLE = 'Yeetcode2020-Data'

def lambda_handler(event, context):

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
                UpdateExpression="set leaderboard.#uri = :v"
            )
            print(update_res)
        except Exception as e:
            print(e)

    return {
        'statusCode': 200,
        'body': "DONE"
    }
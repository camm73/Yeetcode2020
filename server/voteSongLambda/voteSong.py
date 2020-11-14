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

    # Get direction of vote
    if('voteDir' in data_packet):
        if(data_packet['voteDir'] == 'up'):
            vote_val = "1"
        elif(data_packet['voteDir'] == 'down'):
            vote_val = "-1"
        else:
            return {
                "statusCode": 500,
                "body": "Improper vote direction"
            }
    else:
        return {
            "statusCode": 500,
            "body": "Vote direction not included"
        }

    # Find song URI in leaderboard
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

    # Increment or decrement vote value
    if(songURI in res['Item']['leaderboard']['M']):
        oldVal = int(res['Item']['leaderboard']['M'][songURI]['N'])
        print('Old Val:', oldVal)
        # Make sure value isn't negative
        if((oldVal > 0 and vote_val == '-1') or (oldVal >= 0 and vote_val == "1")):
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
                            "N": vote_val
                        }
                    },
                    UpdateExpression="set leaderboard.#uri = leaderboard.#uri + :v"
                )
                print(update_res)
            except Exception as e:
                print(e)
    else:
        return {
            "statusCode": 500,
            "body": "Song URI doesn't exist in leaderboard"
        }

    return {
        'statusCode': 200,
        'body': "DONE"
    }
import boto3
import json
import random

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

    return {
        'statusCode': 200,
        'body': "DONE"
    }
import boto3
import json

dynamodb = boto3.client('dynamodb', region_name='us-east-1')
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

    # Get current data
    try:
        res = dynamodb.get_item(TableName=TABLE, Key={
            'partyID': {
                'S': partyID
            }
        })
        if('Item' not in res):
            return {
                "statusCode": 500,
                "body": "Couldn't find party in table"
            }
    except Exception as err:
        print(err)
        return {
            "statusCode": 500,
            "body": "Party ID does not exist"
        }
    
    current_data = res['Item']
    client_list = current_data['clients']['L']
    
    index = None
    # Find client in list
    for i, entry in enumerate(client_list):
        tmp_client = entry['S']

        if(tmp_client == clientID):
            index = i
            break

    if(index == None):
        return {
            "statusCode": 200,
            "body": "Client doesn't exist"
        }
    
    # Remove from client list
    client_list.pop(index)

    # Remove client from game
    try:
        update_res = dynamodb.update_item(
            TableName=TABLE,
            Key={
                'partyID': {
                    'S': partyID
                }
            },
            ExpressionAttributeValues={
                ":c": {
                    "L": client_list
                }
            },
            UpdateExpression="set clients = :c"
        )
        print(update_res)
    except Exception as e:
        print(e)

    return {
        'statusCode': 200,
        "body": "Successfully left game"
    }
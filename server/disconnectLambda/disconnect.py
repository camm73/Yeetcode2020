import boto3
import json

TABLE = 'Yeetcode2020-Data'
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': "DONE"
    }
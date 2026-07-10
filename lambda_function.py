import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('resume-visitor-count')

def lambda_handler(event, context):
    response = table.update_item(
        Key={'id': 'counter'},
        UpdateExpression='SET #c = #c + :incr',
        ExpressionAttributeNames={'#c': 'count'},
        ExpressionAttributeValues={':incr': 1},
        ReturnValues='UPDATED_NEW'
    )
    
    new_count = response['Attributes']['count']
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(int(new_count))
}
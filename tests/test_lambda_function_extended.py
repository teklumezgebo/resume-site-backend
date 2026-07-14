import os
os.environ.setdefault('AWS_ACCESS_KEY_ID', 'testing')
os.environ.setdefault('AWS_SECRET_ACCESS_KEY', 'testing')
os.environ.setdefault('AWS_SECURITY_TOKEN', 'testing')
os.environ.setdefault('AWS_SESSION_TOKEN', 'testing')
os.environ.setdefault('AWS_DEFAULT_REGION', 'us-east-1')

import json
import boto3
import pytest
from moto import mock_aws

from lambda_function import lambda_handler

TABLE_NAME = 'resume-visitor-count'


@pytest.fixture
def empty_dynamodb_table():
    """
    Same as before, but WITHOUT seeding a starting item
    this simulates a brand new table with no counter row yet.
    """
    with mock_aws():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        yield table


def test_lambda_handles_missing_counter_item(empty_dynamodb_table):
    """
    DynamoDB's update_item with an ADD/SET expression on a non-existent item
    creates it automatically, treating a missing number as 0 first.
    """
    response = lambda_handler({}, {})

    assert response['statusCode'] == 200
    body = json.loads(response['body'])
    assert body == 1
    

def test_lambda_response_has_expected_keys(empty_dynamodb_table):
    """
    Confirms the response dict has exactly the structure API Gateway
    (Lambda proxy integration).
    """
    response = lambda_handler({}, {})

    assert 'statusCode' in response
    assert 'headers' in response
    assert 'body' in response
    assert isinstance(response['body'], str)  # body must be a string, not a raw dict/number
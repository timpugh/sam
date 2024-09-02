import boto3
import os
import json

# Get the DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE"])


def lambda_handler(message, context):
    response = table.scan()

    return {"statusCode": 200, "headers": {}, "body": json.dumps(response["Items"])}

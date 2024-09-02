import boto3
import json
import os
from urllib.parse import unquote
from boto3.dynamodb.conditions import Key


# Get the DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE"])


def lambda_handler(event, context):
    player_name = unquote(event["pathParameters"]["id"])

    response = table.query(KeyConditionExpression=Key("player_name").eq(player_name))
    print(response)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(response["Items"]),
    }

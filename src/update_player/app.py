import boto3
import json
import os
from urllib.parse import unquote

# Get the DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE"])


def lambda_handler(event, context):
    # Get the player UUID and new points value from the event
    # Get the player data from the event
    player_name = unquote(event["pathParameters"]["id"])
    season = event["pathParameters"]["date"]
    body = json.loads(event["body"])
    
    statistic = body['statistic']
    value = body['value']

    # Construct the key dictionary
    key = {"player_name": player_name, "season": season}

    update_expression = "SET " + statistic + " = :val1"
    expression_attribute_values = {":val1": value}

    try:
        # Update the item in the table
        table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues='UPDATED_NEW'
        )
        return {
            "statusCode": 200,
            'headers': {
                    "Access-Control-Allow-Origin": "*",
                },
            "body": json.dumps(
                {
                    "message": f"Player {player_name} updated successfully for season {season}."
                }
            ),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            'headers': {
                    "Access-Control-Allow-Origin": "*",
                },
            "body": json.dumps(
                {"error": f"Error updating player {player_name}: {str(e)}"}
            ),
        }

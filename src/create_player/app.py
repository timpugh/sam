import boto3
import json
import os
import uuid

# Get the DynamoDB resource
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE"])


# Function to create a new player
def lambda_handler(event, context):
    # Get the player data from the event
    body = json.loads(event["body"])
    player_data = body["player"]

    # Generate a unique UUID for the player
    player_data["uuid"] = str(uuid.uuid4())

    # Put the player data into the DynamoDB table
    try:
        table.put_item(Item=player_data)

        # Return the response
        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": f"Player {player_data['player_name']} created successfully.",
                }
            ),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "error": f"Error adding {
                        player_data['player_name']}: {str(e)}"
                }
            ),
        }

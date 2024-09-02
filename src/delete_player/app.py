import boto3
import json
import os
from urllib.parse import unquote

# Get the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ["TABLE"])


# Function to delete a player
def lambda_handler(event, context):
    # Get the player data from the event
    player_name =  unquote(event['pathParameters']['id'])
    season = event['pathParameters']['date']

    # Construct the key dictionary
    key = {
        'player_name': player_name,
        'season': season
    }

    # Delete the player data in the DynamoDB table
    try:
        response = table.delete_item(
            Key=key
        )
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f"Player {player_name} deleted successfully for season {season}."
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f"Error deleting player {player_name}: {str(e)}"
            })
        }
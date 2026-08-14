"""
Send a plain text message using the SendTextMessage API.

This is the same API used for SMS. When you pass an RCS agent ARN as the
origination identity, it delivers over RCS instead.
"""
import json
import boto3
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

client = boto3.client('pinpoint-sms-voice-v2')

try:
    response = client.send_text_message(
        DestinationPhoneNumber=config['destinationPhoneNumber'],
        OriginationIdentity=config['rcsAgentArn'],
        MessageBody="Hello from AnyCompany over RCS."
    )
    print(f"Message sent. ID: {response['MessageId']}")
except client.exceptions.ThrottlingException as e:
    print(f"Rate limited. Retry after backoff: {e}")
except client.exceptions.ValidationException as e:
    print(f"Invalid request or media: {e}")
except Exception as e:
    print(f"Failed to send message: {e}")

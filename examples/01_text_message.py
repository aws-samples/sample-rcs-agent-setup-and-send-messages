"""
Send a plain RCS text message using SendRcsMessage.

RCS text messages support up to 3,072 UTF-8 characters and arrive as a single
message regardless of length (unlike SMS which splits at 160 characters).
"""
import json
import boto3
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

client = boto3.client('pinpoint-sms-voice-v2')

message_content = {
    "Content": {
        "TextMessage": {
            "Body": "Thanks for reaching out to AnyCompany! Your order ORD-2026-001 has shipped and arrives on Friday, August 7. Reply to this message if you have any questions."
        }
    }
}

try:
    response = client.send_rcs_message(
        DestinationPhoneNumber=config['destinationPhoneNumber'],
        OriginationIdentity=config['rcsAgentArn'],
        RcsMessageContent=message_content
    )
    print(f"Message sent. ID: {response['MessageId']}")
except client.exceptions.ThrottlingException as e:
    print(f"Rate limited. Retry after backoff: {e}")
except client.exceptions.ValidationException as e:
    print(f"Invalid request or media: {e}")
except Exception as e:
    print(f"Failed to send message: {e}")

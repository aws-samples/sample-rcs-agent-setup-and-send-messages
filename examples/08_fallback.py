"""
Send a message with per-message SMS fallback.

FallbackConfiguration routes the message to SMS or MMS when the device or carrier
doesn't support RCS, when the channel rejects the message, or when TimeToLive expires.

Requirements:
- Channel: SMS or MMS
- MessageBody: required for SMS fallback (up to 1,600 chars)
- OriginationIdentity: a phone number or sender ID registered in your account
  that can send SMS/MMS (pools and RCS agents are NOT accepted here)

NOTE: This example requires a valid SMS-capable phone number in your account.
Update FALLBACK_PHONE_NUMBER before running.
"""
import json
import boto3
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

client = boto3.client('pinpoint-sms-voice-v2')

# Replace with a real SMS-capable phone number from your account
FALLBACK_PHONE_NUMBER = "+12065550188"

message_content = {
    "Content": {
        "TextMessage": {
            "Body": "AnyCompany: your delivery arrives today between 2:00 PM and 4:00 PM. Track it at https://example.com/track/1234"
        }
    }
}

try:
    response = client.send_rcs_message(
        DestinationPhoneNumber=config['destinationPhoneNumber'],
        OriginationIdentity=config['rcsAgentArn'],
        RcsMessageContent=message_content,
        FallbackConfiguration={
            "Channel": "SMS",
            "MessageBody": "AnyCompany: your delivery arrives today between 2:00 PM and 4:00 PM. Track it at https://example.com/track/1234",
            "OriginationIdentity": FALLBACK_PHONE_NUMBER
        }
    )
    print(f"Message sent. ID: {response['MessageId']}")
except client.exceptions.ThrottlingException as e:
    print(f"Rate limited. Retry after backoff: {e}")
except client.exceptions.ValidationException as e:
    print(f"Invalid request or media: {e}")
except Exception as e:
    print(f"Failed to send message: {e}")

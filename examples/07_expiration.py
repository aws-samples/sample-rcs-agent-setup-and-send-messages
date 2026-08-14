"""
Send a message with TimeToLive (message expiration).

If the message is not delivered within the TTL window (in seconds), the service
removes it and the recipient never sees it. Useful for OTPs and time-sensitive content.

TimeToLive: 1 to 172,800 seconds (48 hours). Use at least 10 seconds.
The countdown starts when the service accepts the request.

On expiry you receive TTL_EXPIRATION_REVOKED (safe to send fallback) or
TTL_EXPIRATION_REVOKE_FAILED (message might still deliver).
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
            "Body": "Your AnyCompany verification code is 482913. This code expires in 5 minutes."
        }
    }
}

try:
    response = client.send_rcs_message(
        DestinationPhoneNumber=config['destinationPhoneNumber'],
        OriginationIdentity=config['rcsAgentArn'],
        RcsMessageContent=message_content,
        TimeToLive=300
    )
    print(f"Message sent. ID: {response['MessageId']}")
except client.exceptions.ThrottlingException as e:
    print(f"Rate limited. Retry after backoff: {e}")
except client.exceptions.ValidationException as e:
    print(f"Invalid request or media: {e}")
except Exception as e:
    print(f"Failed to send message: {e}")

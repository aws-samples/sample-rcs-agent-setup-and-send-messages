"""
Send a file message (image, video, audio, or PDF) that renders inline.

FileUrl accepts two forms:
- S3 URL (s3://bucket/key) — validated at request time, rehosted with presigned URL
- Public HTTPS URL — passes through to the carrier without request-time validation

Maximum file size: 100 MB at the API layer (carriers may enforce lower limits).
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
        "FileMessage": {
            "FileUrl": "https://docs.aws.amazon.com/pdfs/social-messaging/latest/userguide/social-ug.pdf"
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

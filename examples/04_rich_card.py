"""
Send a rich card with media, title, description, and suggestion chips.

Rich cards combine an image, title, description, and up to 4 suggested actions
into a single structured message. Use VERTICAL orientation (HORIZONTAL truncates
images on iOS).

Media Height options: SHORT (112dp), MEDIUM (168dp), TALL (264dp).

NOTE: FileUrl must be a publicly accessible HTTPS URL or an S3 URL with the
appropriate bucket policy. Placeholder URLs (example.com) are accepted by the
API but won't render on devices.
"""
import json
import boto3
import os

config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r') as f:
    config = json.load(f)

client = boto3.client('pinpoint-sms-voice-v2')

# AWS Architecture Icon from the public awslabs GitHub repo
IMAGE_URL = "https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/main/dist/BusinessApplications/EndUserMessaging.png"

message_content = {
    "Content": {
        "RichCard": {
            "CardOrientation": "VERTICAL",
            "CardContent": {
                "Title": "AWS End User Messaging",
                "Description": "Send and receive messages across SMS, MMS, and RCS channels with a single API. Reach customers on the messaging apps already on their phones.",
                "Media": {
                    "FileUrl": IMAGE_URL,
                    "Height": "MEDIUM"
                },
                "Suggestions": [
                    {
                        "Reply": {
                            "Text": "Learn more",
                            "PostbackData": "learn_eum"
                        }
                    },
                    {
                        "OpenUrl": {
                            "Text": "Open console",
                            "PostbackData": "console_eum",
                            "Url": "https://console.aws.amazon.com/sms-voice",
                            "Application": "BROWSER"
                        }
                    }
                ]
            }
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

"""
Send a carousel with 2-10 horizontally scrollable rich cards.

Carousel cards use the same content model as standalone rich cards, with two
differences: cards always render vertically, and TALL media height is not supported.

CardWidth options: SMALL (180dp) or MEDIUM (296dp) — all cards share the same width.
Maximum 4 suggestions per card.

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

# AWS Architecture Icons from the public awslabs GitHub repo
ICONS_BASE = "https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/main/dist"

message_content = {
    "Content": {
        "Carousel": {
            "CardWidth": "MEDIUM",
            "CardContents": [
                {
                    "Title": "AWS End User Messaging",
                    "Description": "Send and receive messages across SMS, MMS, and RCS channels with a single API.",
                    "Media": {
                        "FileUrl": f"{ICONS_BASE}/BusinessApplications/EndUserMessaging.png",
                        "Height": "SHORT"
                    },
                    "Suggestions": [
                        {
                            "Reply": {
                                "Text": "Select",
                                "PostbackData": "select_eum"
                            }
                        }
                    ]
                },
                {
                    "Title": "AWS Lambda",
                    "Description": "Run code without provisioning servers. Pay only for compute time consumed.",
                    "Media": {
                        "FileUrl": f"{ICONS_BASE}/Compute/Lambda.png",
                        "Height": "SHORT"
                    },
                    "Suggestions": [
                        {
                            "Reply": {
                                "Text": "Select",
                                "PostbackData": "select_lambda"
                            }
                        }
                    ]
                },
                {
                    "Title": "Amazon Bedrock",
                    "Description": "Build generative AI apps with foundation models through a single API.",
                    "Media": {
                        "FileUrl": f"{ICONS_BASE}/ArtificialIntelligence/Bedrock.png",
                        "Height": "SHORT"
                    },
                    "Suggestions": [
                        {
                            "Reply": {
                                "Text": "Select",
                                "PostbackData": "select_bedrock"
                            }
                        }
                    ]
                }
            ]
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

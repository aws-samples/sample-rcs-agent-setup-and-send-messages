"""
Send a message with all 6 RCS suggestion types.

Suggestion types: Reply, OpenUrl, DialPhone, ShowLocation, RequestLocation,
CreateCalendarEvent. You can mix them on any content type.

Message-level suggestions live in a "Suggestions" array that is a SIBLING of
"Content", not nested inside it. Card-level suggestions go inside CardContent.

Every suggestion requires Text (up to 25 chars) and PostbackData (up to 2,048 chars).
Two-way messaging with an SNS topic must be configured to receive tap events.
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
            "Body": "Your fitting appointment at AnyCompany Anytown is confirmed for Friday, August 7 at 2:00 PM. How would you like to manage your visit?"
        }
    },
    "Suggestions": [
        {
            "Reply": {
                "Text": "Confirm",
                "PostbackData": "appt_confirm_12345"
            }
        },
        {
            "Reply": {
                "Text": "Reschedule",
                "PostbackData": "appt_reschedule_12345"
            }
        },
        {
            "OpenUrl": {
                "Text": "Manage booking",
                "PostbackData": "appt_manage_12345",
                "Url": "https://example.com/bookings/12345",
                "Application": "BROWSER"
            }
        },
        {
            "DialPhone": {
                "Text": "Call the store",
                "PostbackData": "appt_call_12345",
                "PhoneNumber": "+12065550142"
            }
        },
        {
            "ShowLocation": {
                "Text": "View store map",
                "PostbackData": "appt_map_12345",
                "Latitude": 47.6062,
                "Longitude": -122.3321,
                "Label": "AnyCompany Anytown"
            }
        },
        {
            "RequestLocation": {
                "Text": "Share my location",
                "PostbackData": "appt_share_loc_12345"
            }
        },
        {
            "CreateCalendarEvent": {
                "Text": "Add to calendar",
                "PostbackData": "appt_cal_12345",
                "Title": "AnyCompany fitting appointment",
                "StartTime": "2026-08-07T06:00:00Z",
                "EndTime": "2026-08-07T06:30:00Z",
                "Description": "Fitting appointment at AnyCompany Anytown"
            }
        }
    ]
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

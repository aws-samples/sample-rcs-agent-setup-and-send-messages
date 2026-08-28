# RCS Messaging Examples

Ready-to-run Python scripts demonstrating every RCS content type supported by
the AWS End User Messaging SMS `SendRcsMessage` API.

## Prerequisites

- Python 3.9+
- Boto3 1.43.37 or later (`pip install --upgrade boto3`)
- AWS CLI 2.35.12 or later (for agent setup commands)
- An RCS agent in `ACTIVE` testing state
- A verified test device phone number
- AWS credentials configured

## Setup

1. Copy `config.json.example` to `config.json`:
   ```bash
   cp config.json.example config.json
   ```

2. Edit `config.json` with your agent ARN and destination phone number:
   ```json
   {
     "rcsAgentArn": "arn:aws:sms-voice:us-east-1:111122223333:rcs-agent/rcs-a1b2c3d4",
     "destinationPhoneNumber": "+12065550100"
   }
   ```

3. Run any example:
   ```bash
   python3 01_text_message.py
   ```

## Examples

| # | Script | Content Type | Description |
|---|--------|-------------|-------------|
| 01 | `01_text_message.py` | TextMessage | Plain RCS text via `SendRcsMessage` |
| 02 | `02_send_text_message_api.py` | Text | Plain text via `SendTextMessage` API (same API as SMS) |
| 03 | `03_file_message.py` | FileMessage | Inline PDF document |
| 04 | `04_rich_card.py` | RichCard | Service card with image, title, description, and suggestion chips |
| 05 | `05_carousel.py` | Carousel | 3 AWS service cards in a horizontally scrollable strip |
| 06 | `06_suggestions.py` | Suggestions | All 6 suggestion types on one message |
| 07 | `07_expiration.py` | TimeToLive | OTP with 5-minute expiration window |
| 08 | `08_fallback.py` | FallbackConfiguration | SMS fallback for non-RCS devices |

## Image Hosting

The rich card (`04`) and carousel (`05`) examples use [AWS Architecture Icons](https://github.com/awslabs/aws-icons-for-plantuml)
hosted on GitHub (`raw.githubusercontent.com`). These are publicly accessible
and work out of the box.

For your own images, two options:

1. **Public HTTPS URL** — Any publicly accessible image URL works.
2. **S3 URL** (`s3://bucket-name/key`) — Validated at request time, requires a
   bucket policy granting `s3:GetObject` to `sms-voice.amazonaws.com`:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": { "Service": "sms-voice.amazonaws.com" },
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::your-bucket/rcs-media/*"
       }
     ]
   }
   ```

## Important Notes

- **Image URLs must be real and publicly accessible.** Placeholder URLs like
  `https://example.com/image.png` are accepted by the API but won't render on
  devices — the carrier silently drops the media.

- **Suggestions** require a two-way messaging SNS topic configured on your agent
  to receive tap events.

- **Fallback** requires a separate SMS-capable phone number (not the RCS agent).

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `DESTINATION_PHONE_NUMBER_OPTED_OUT` | `aws pinpoint-sms-voice-v2 delete-opted-out-number --opt-out-list-name Default --opted-out-number <PHONE>` |
| `DESTINATION_COUNTRY_BLOCKED_BY_PROTECT_CONFIGURATION` | Update protect config to ALLOW for your country |
| Message accepted but media not rendered | Verify image URL is accessible (not example.com). Use `curl -I <url>` to confirm 200 response. |
| Message accepted but not received at all | Check agent status is ACTIVE, device supports RCS |
| `send_rcs_message` not found on client | Upgrade boto3: `pip install --upgrade boto3` (requires 1.43.37+) |

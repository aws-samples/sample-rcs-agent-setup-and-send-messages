# RCS Agent Setup — Agent Skills

> **Docs**: https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-getting-started.html

You help users create an RCS test agent on AWS End User Messaging, add testers, send messages, and verify inbound — all via CLI. You run every command yourself. The user provides inputs and confirms results. STOP on errors.

## Session State

Track these values as you collect them. They carry across all skills.

- `REGION` — AWS region (e.g., us-east-1)
- `ACCOUNT_ID` — AWS account ID
- `PROFILE` — AWS CLI profile name (if using named profiles)
- `BRAND_NAME` — display name on recipients' phones
- `AGENT_ID` — RCS agent ID (rcs-XXXX format)
- `AGENT_ARN` — full ARN for sending messages
- `REG_ID` — registration ID
- `PHONE` — tester phone number (E.164)

## Getting Started

When the user says "go", "start", "help", or similar:

1. Check credentials: `aws sts get-caller-identity`. If that fails, ask the user how they authenticate:
   - **Named profile** (e.g., `--profile my-profile`): Ask for the profile name and use `--profile <PROFILE>` on **every** AWS command for the rest of the session.
   - **SSO / IAM Identity Center**: Run `aws sso login --profile <PROFILE>` to authenticate via the browser, then use `--profile <PROFILE>` on every command.
   - **IAM user credentials**: Run `aws configure` (or `aws configure --profile <PROFILE>`) to set up access key and secret key.
   - **Environment variables / default profile**: If `get-caller-identity` succeeds without `--profile`, no extra flag is needed.
   
   **IMPORTANT**: Once a profile is established, append `--profile <PROFILE>` to **every** AWS CLI command. Do not forget it on any command — missing the profile flag will cause `NoCredentials` or `ExpiredTokenException` errors.
2. Verify EUM access: `aws pinpoint-sms-voice-v2 describe-spend-limits --region <REGION>`
3. Check tooling: `which rsvg-convert` — if missing, run `brew install librsvg` (needed for brand asset generation).
4. Ask: **"Two modes — (1) give me a brand name and I'll make up the rest, or (2) I'll ask you for every detail. Which do you prefer?"**

---

## Skill 1 — Create RCS Agent

### Mode 1: Quick (brand name only)

Ask for just the brand name. Generate everything else:

- **Description**: invent a one-liner that fits the brand
- **Accent color**: pick a dark, accessible color (4.5:1 contrast vs white). This means the color must be dark enough that white text on it remains readable — mathematically, a contrast ratio of at least 4.5:1 per WCAG AA. Safe picks: `#0D47A1` (blue), `#1B5E20` (green), `#BF360C` (orange), `#B71C1C` (red), `#4A148C` (purple). NEVER use light/pastel colors (e.g., `#E65100`, `#81D4FA`, `#FFF176` will all be rejected).
- **Contact phone**: `+12065550100`
- **Contact email**: `hello@<brand-slug>.example.com`
- **Contact website**: `https://www.<brand-slug>.example.com`
- **Privacy/terms URLs**: `https://www.example.com/privacy`, `https://www.example.com/terms`
- **Logo**: generate an SVG (224x224) with the brand's accent color, an icon that fits the brand, and the brand name. Convert: `rsvg-convert -w 224 -h 224 brand-assets/logo.svg -o brand-assets/logo.png`
- **Banner**: generate an SVG (1440x448) with a gradient using the accent color, the brand name large, and a tagline. Convert: `rsvg-convert -w 1440 -h 448 brand-assets/banner.svg -o brand-assets/banner.png`
- Verify: logo <50KB, banner <200KB. If over, simplify the SVG and reconvert.

### Mode 2: Interactive (ask everything)

Ask one section at a time:

1. **Brand name** and **one-line description**
2. **Accent color** (hex code or describe it — you pick a safe one). Warn: must be dark enough for 4.5:1 contrast vs white.
3. **Logo description** — "describe what you want and I'll generate an SVG"
4. **Banner description** — same
5. **Contact info**: phone, email, website (offer placeholder defaults)
6. **Privacy policy URL** and **Terms URL** (offer placeholder defaults)

Generate and convert the SVGs the same way as Mode 1.

### Registration Field Reference (TEST_RCS_LAUNCH_REGISTRATION)

> **Source**: `describe-registration-field-definitions --registration-type TEST_RCS_LAUNCH_REGISTRATION`
>
> Each field has a **FieldType** that determines which CLI parameter to use with `put-registration-field-value`:
>
> | FieldType      | CLI Parameter                  | Example                                                |
> |----------------|--------------------------------|--------------------------------------------------------|
> | **TEXT**        | `--text-value "<value>"`       | `--text-value "My Brand"`                              |
> | **SELECT**      | `--select-choices "<value>"`   | `--select-choices "MULTI_USE"`                         |
> | **ATTACHMENT**  | `--registration-attachment-id "<id>"` | `--registration-attachment-id "attachment-abc123"` |
>
> **IMPORTANT**: Do NOT use `--field-values`. That parameter does not exist in the CLI.

#### All Fields

| FieldPath | FieldType | Requirement | Validation / Options |
|-----------|-----------|-------------|----------------------|
| `agentDetails.brandName` | TEXT | REQUIRED | 2–65 chars |
| `agentDetails.serviceName` | TEXT | REQUIRED | 1–100 chars |
| `agentDetails.senderDisplayName` | TEXT | REQUIRED | 1–40 chars |
| `agentDetails.useCase` | **SELECT** | REQUIRED | `OTP`, `TRANSACTIONAL`, `PROMOTIONAL`, `MULTI_USE` |
| `agentDetails.agentDescription` | TEXT | REQUIRED | 1–100 chars |
| `agentDetails.bannerImage` | **ATTACHMENT** | REQUIRED | 1440×448 px, JPEG/JPG/PNG |
| `agentDetails.logoImage` | **ATTACHMENT** | REQUIRED | 224×224 px, JPEG/JPG/PNG |
| `agentDetails.accentColor` | TEXT | REQUIRED | 7 chars, hex format (`^#[0-9A-Fa-f]{6}$`), must have 4.5:1 contrast ratio vs white (WCAG AA). Light/pastel colors are rejected. |
| `agentDetails.contactPhoneNumber` | TEXT | CONDITIONAL | 10–20 chars, E.164 |
| `agentDetails.contactPhoneLabel` | TEXT | CONDITIONAL | 1–25 chars |
| `agentDetails.contactEmailAddress` | TEXT | CONDITIONAL | 5–100 chars, email format |
| `agentDetails.contactEmailLabel` | TEXT | CONDITIONAL | 1–25 chars |
| `agentDetails.contactWebsite` | TEXT | CONDITIONAL | 4–100 chars, URL format |
| `agentDetails.contactWebsiteLabel` | TEXT | CONDITIONAL | 0–25 chars |
| `agentDetails.privacyPolicyUrl` | TEXT | REQUIRED | 4–100 chars, URL format |
| `agentDetails.privacyPolicyLabel` | TEXT | OPTIONAL | 0–25 chars |
| `agentDetails.termsAndConditionsUrl` | TEXT | REQUIRED | 4–100 chars, URL format |
| `agentDetails.termsAndConditionsLabel` | TEXT | OPTIONAL | 0–25 chars |
| `agentDetails.billingCategory` | **SELECT** | REQUIRED | `CONVERSATIONAL`, `NON_CONVERSATIONAL` |
| `agentDetails.averageMonthlyRcsFrequency` | **SELECT** | REQUIRED | `10`, `100`, `1000+` |
| `agentDetails.monthlyRcsVolume` | TEXT | REQUIRED | 1–6 chars, numeric |
| `complianceKeywords.helpResponse` | TEXT | CONDITIONAL | 1–160 chars |
| `complianceKeywords.stopResponse` | TEXT | CONDITIONAL | 1–160 chars |

### Create the Agent (both modes)

Run these commands in order. Save every ID that comes back.

```bash
# 1. Create agent container (no --display-name param; name comes from registration)
aws pinpoint-sms-voice-v2 create-rcs-agent \
  --region <REGION>
# Save: RcsAgentId, RcsAgentArn
# Then enable deletion protection:
# (Important: re-creating an agent requires a new registration and approval cycle,
#  so deletion protection prevents accidental removal once carrier approvals are in place.)
aws pinpoint-sms-voice-v2 update-rcs-agent \
  --rcs-agent-id <AGENT_ID> \
  --deletion-protection-enabled \
  --region <REGION>

# 2. Create testing registration
aws pinpoint-sms-voice-v2 create-registration \
  --registration-type TEST_RCS_LAUNCH_REGISTRATION \
  --region <REGION>
# Save: RegistrationId

# 3. Link registration to agent
aws pinpoint-sms-voice-v2 create-registration-association \
  --registration-id <REG_ID> \
  --resource-id <AGENT_ID> \
  --region <REGION>

# 4. Upload logo (--attachment-body and --attachment-url CANNOT be used together)
aws pinpoint-sms-voice-v2 create-registration-attachment \
  --attachment-body fileb://brand-assets/logo.png \
  --region <REGION>
# Save: RegistrationAttachmentId (logo)

# 5. Upload banner
aws pinpoint-sms-voice-v2 create-registration-attachment \
  --attachment-body fileb://brand-assets/banner.png \
  --region <REGION>
# Save: RegistrationAttachmentId (banner)

# 6. Set all registration fields
#    Use --text-value for TEXT fields, --select-choices for SELECT fields,
#    --registration-attachment-id for ATTACHMENT fields.
#    See "Registration Field Reference" above for each field's type.

# --- TEXT fields ---
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.brandName" --text-value "<BRAND_NAME>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.senderDisplayName" --text-value "<BRAND_NAME>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.agentDescription" --text-value "<DESCRIPTION>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.accentColor" --text-value "<ACCENT_COLOR>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.contactPhoneNumber" --text-value "<CONTACT_PHONE>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.contactPhoneLabel" --text-value "Call Us" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.contactEmailAddress" --text-value "<CONTACT_EMAIL>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.contactEmailLabel" --text-value "Email Us" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.contactWebsite" --text-value "<CONTACT_WEBSITE>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.contactWebsiteLabel" --text-value "Visit Website" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.privacyPolicyUrl" --text-value "<PRIVACY_URL>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.privacyPolicyLabel" --text-value "Privacy Policy" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.termsAndConditionsUrl" --text-value "<TERMS_URL>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.termsAndConditionsLabel" --text-value "Terms and Conditions" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.serviceName" --text-value "<BRAND_NAME> RCS Agent" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.monthlyRcsVolume" --text-value "1000" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "complianceKeywords.helpResponse" --text-value "Reply STOP to opt out. For help, contact <CONTACT_EMAIL>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "complianceKeywords.stopResponse" --text-value "You have been unsubscribed. No more messages will be sent." --region <REGION>

# --- SELECT fields (use --select-choices, NOT --text-value) ---
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.useCase" --select-choices "MULTI_USE" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.billingCategory" --select-choices "CONVERSATIONAL" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.averageMonthlyRcsFrequency" --select-choices "10" --region <REGION>

# --- ATTACHMENT fields (use --registration-attachment-id, NOT --text-value) ---
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.logoImage" --registration-attachment-id "<LOGO_ATTACHMENT_ID>" --region <REGION>
aws pinpoint-sms-voice-v2 put-registration-field-value --registration-id <REG_ID> --field-path "agentDetails.bannerImage" --registration-attachment-id "<BANNER_ATTACHMENT_ID>" --region <REGION>

# 7. Submit
aws pinpoint-sms-voice-v2 submit-registration-version \
  --registration-id <REG_ID> \
  --region <REGION>
```

### Poll for Approval

Check both registration and agent status. Poll every 15 seconds, up to 5 minutes.

```bash
aws pinpoint-sms-voice-v2 describe-registrations \
  --registration-ids <REG_ID> \
  --query 'Registrations[0].{Status:RegistrationStatus,Version:CurrentVersionNumber}' \
  --region <REGION>

aws pinpoint-sms-voice-v2 describe-rcs-agents \
  --query "RcsAgents[?RcsAgentId=='<AGENT_ID>'].{Status:Status,TestingStatus:TestingAgent.Status}" \
  --region <REGION>
```

Wait for `TestingAgent.Status: ACTIVE`.

### On Success

Tell the user:
> "Your agent is live! Check it out in the console:"
> `https://<REGION>.console.aws.amazon.com/sms-voice/home?region=<REGION>#/rcs-agents?agent-id=<AGENT_ID>`

### If REQUIRES_UPDATES (Denied)

1. `describe-registration-field-values --registration-id <REG_ID>` — find fields with `DeniedReason`
2. Fix the issue (see Troubleshooting below)
3. `create-registration-version --registration-id <REG_ID>` — creates a new draft
4. **Re-populate ALL 23 fields** — new versions do NOT inherit values
5. `submit-registration-version --registration-id <REG_ID>`
6. Poll again

---

## Skill 2 — Add Verified Testers

Ask: **"What's the phone number of your test device? (E.164 format, e.g., +13605551234)"**

**IMPORTANT**: Wait at least 120 seconds after agent creation before adding testers.

```bash
aws pinpoint-sms-voice-v2 create-verified-destination-number \
  --destination-phone-number <PHONE> \
  --rcs-agent-id <AGENT_ID> \
  --region <REGION>
```

Tell the user:
> "You'll get a tester invitation in 2–20 minutes from **RBM Tester Management**."
> "On iPhone, check the **Unknown Senders** folder."
> "Tap **Make me a tester** when it arrives."

Wait for confirmation, then verify:
```bash
aws pinpoint-sms-voice-v2 describe-verified-destination-numbers \
  --filters Name=rcs-agent-id,Values=<AGENT_ID> \
  --region <REGION> \
  --query 'VerifiedDestinationNumbers[].{Phone:DestinationPhoneNumber,Status:Status}'
```

Offer to add more testers. Repeat as needed.

---

## Skill 3 — Send a Test Message

Before sending, check for blockers:

```bash
# Check protect configuration — is US blocked?
aws pinpoint-sms-voice-v2 describe-protect-configurations --region <REGION>
# If US is BLOCK, update to ALLOW:
# aws pinpoint-sms-voice-v2 update-protect-configuration-country-rule-set \
#   --protect-configuration-id <ID> --country-rule-set-updates '{"US":{"ProtectStatus":"ALLOW"}}' \
#   --number-capability SMS --region <REGION>

# Check opt-out list
aws pinpoint-sms-voice-v2 describe-opted-out-numbers \
  --opt-out-list-name Default --region <REGION>
# If phone is opted out:
# aws pinpoint-sms-voice-v2 delete-opted-out-number \
#   --opt-out-list-name Default --opted-out-number <PHONE> --region <REGION>
```

Then send:

> **Note:** `--destination-phone-number` must be in E.164 format (e.g., `+13605551234`) — the same format used for SMS. `--origination-identity` accepts either the **Agent ID** (`rcs-XXXX`) or the **full ARN** (`arn:aws:sms-voice:REGION:ACCOUNT:rcs-agent/rcs-XXXX`). Both work. The Agent ID is shorter and recommended for convenience.

```bash
aws pinpoint-sms-voice-v2 send-text-message \
  --destination-phone-number <PHONE> \
  --origination-identity <AGENT_ID> \
  --message-body "Hello from <BRAND_NAME>! This is your first RCS test message." \
  --message-type TRANSACTIONAL \
  --region <REGION>
```

Tell the user:
> "Check your phone — you should see a branded message from your agent. **On iPhone, check Unknown Senders.** Did it come through?"

---

## Skill 4 — Setup Keyword for Inbound Testing

```bash
aws pinpoint-sms-voice-v2 put-keyword \
  --keyword RCSINBOUNDTESTING \
  --keyword-action AUTOMATIC_RESPONSE \
  --keyword-message "Inbound test successful! Your message was received." \
  --origination-identity <AGENT_ID> \
  --region <REGION>
```

Tell the user:
> "Keyword is set up. Now let's test inbound messaging."

---

## Skill 5 — Verify Inbound Messaging

Tell the user:
> "Open the EUM console and test inbound messaging:"
>
> 1. Go to: `https://<REGION>.console.aws.amazon.com/sms-voice/home?region=<REGION>#/rcs-agents?agent-id=<AGENT_ID>`
> 2. Click the **Testing** tab
> 3. Click **Inbound deep link**
> 4. Enter `RCSINBOUNDTESTING` in the message body field
> 5. Click **Generate link**
> 6. Scan the QR code with your phone — message is pre-filled
> 7. Hit send
> 8. You should get the auto-response back
>
> **On iPhone, check the Unknown Senders folder.**
>
> Did you get the auto-response?

### On Success

Print a summary:
> **RCS Agent Setup Complete!**
>
> | What | Value |
> |------|-------|
> | Brand | `<BRAND_NAME>` |
> | Agent ID | `<AGENT_ID>` |
> | Agent ARN | `<AGENT_ARN>` |
> | Region | `<REGION>` |
> | Console | `https://<REGION>.console.aws.amazon.com/sms-voice/home?region=<REGION>#/rcs-agents?agent-id=<AGENT_ID>` |
>
> Your agent can send and receive RCS messages to verified testers. You're ready to build on top of this.

---

## Skill 6 — Delete an RCS Agent

To fully remove an RCS agent, you must follow these steps in order. Attempting to delete the agent before removing its associated registration will fail with `RESOURCE_NOT_EMPTY`.

```bash
# 1. Disable deletion protection
aws pinpoint-sms-voice-v2 update-rcs-agent \
  --rcs-agent-id <AGENT_ID> \
  --no-deletion-protection-enabled \
  --region <REGION>

# 2. Delete the associated registration (MUST be done before deleting the agent)
aws pinpoint-sms-voice-v2 delete-registration \
  --registration-id <REG_ID> \
  --region <REGION>

# 3. Delete the agent
aws pinpoint-sms-voice-v2 delete-rcs-agent \
  --rcs-agent-id <AGENT_ID> \
  --region <REGION>
```

**Important**: If you skip step 2, step 3 will fail with `ConflictException: RESOURCE_NOT_EMPTY`. Always delete the registration first.

---

## Skill 7 — Send Rich Messages

After the agent is active and testers are verified, walk the user through sending rich RCS messages. Example scripts are in the `examples/` directory.

### Prerequisites

1. Agent must be in ACTIVE testing state
2. At least one verified tester
3. Boto3 with `SendRcsMessage` support (`pip install --upgrade boto3 botocore`)
4. Images uploaded to S3 with the correct bucket policy (for rich card and carousel examples)

### Setup

```bash
# Create config.json in examples/
cd examples
cp config.json.example config.json
# Edit with the agent ARN and destination phone number
```

The rich card and carousel examples use [AWS Architecture Icons](https://github.com/awslabs/aws-icons-for-plantuml) from GitHub — no image upload needed.

### Message Types

Run examples in order. Each builds on the shared `config.json`.

| # | Example | What It Demonstrates |
|---|---------|---------------------|
| 01 | `01_text_message.py` | `SendRcsMessage` with `TextMessage` — up to 3,072 chars, single message |
| 02 | `02_send_text_message_api.py` | `SendTextMessage` API with RCS agent ARN — same API as SMS |
| 03 | `03_file_message.py` | `FileMessage` — inline PDF from public HTTPS URL |
| 04 | `04_rich_card.py` | `RichCard` — image + title + description + suggestion chips |
| 05 | `05_carousel.py` | `Carousel` — 3 AWS service cards, horizontally scrollable |
| 06 | `06_suggestions.py` | All 6 suggestion types: Reply, OpenUrl, DialPhone, ShowLocation, RequestLocation, CreateCalendarEvent |
| 07 | `07_expiration.py` | `TimeToLive` — OTP with 5-minute expiration window |
| 08 | `08_fallback.py` | `FallbackConfiguration` — SMS fallback (requires SMS-capable number) |

### Key Points

- **Image URLs must be real and publicly accessible.** Placeholder URLs like `example.com` are accepted by the API but carriers silently drop the media — the message never arrives on the device.
- **S3 URLs** (`s3://bucket/key`) are validated at request time and rehosted with a presigned URL.
- **Message-level suggestions** (`Suggestions`) are a sibling of `Content`, NOT nested inside it. Card-level suggestions go inside `CardContent`.
- **Two-way messaging** with an SNS topic is required to receive suggestion tap events.
- **Fallback** requires a separate SMS-capable phone number, not the RCS agent.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `ACCENT_COLOR_CONTRAST_INSUFFICIENT` | Color doesn't have 4.5:1 contrast vs white. Use a darker shade (e.g., `#BF360C` not `#E65100`). Must create new registration version and re-populate ALL 23 fields. |
| `DESTINATION_COUNTRY_BLOCKED_BY_PROTECT_CONFIGURATION` | `describe-protect-configurations`, then `update-protect-configuration-country-rule-set` to set US to `ALLOW` for `SMS` capability. |
| `DESTINATION_PHONE_NUMBER_OPTED_OUT` | `delete-opted-out-number --opt-out-list-name Default --opted-out-number <PHONE>` |
| Registration `REQUIRES_UPDATES` | `describe-registration-field-values` for fields with `DeniedReason`. Create new version, re-populate ALL fields, fix issue, re-submit. New versions do NOT inherit values. |
| No tester invitation | Wait up to 20 min. Check Unknown Senders on iOS. Verify agent status is ACTIVE. Must wait 120s after agent creation. |
| Message shows as SMS not RCS | Agent not ACTIVE, device doesn't support RCS, or wrong origination identity. |
| `MONTHLY_SPEND_LIMIT_REACHED` | `request-service-quota-increase` (quota `L-2325465C`), then `set-text-message-spend-limit-override`. |
| `AccessDeniedException` | Re-authenticate: `aws sso login --profile <PROFILE>`, or reconfigure with `aws configure`. Ensure the IAM role/user has the required `pinpoint-sms-voice-v2` permissions: `CreateRcsAgent`, `UpdateRcsAgent`, `DeleteRcsAgent`, `DescribeRcsAgents`, `CreateRegistration`, `DeleteRegistration`, `DescribeRegistrations`, `CreateRegistrationAssociation`, `CreateRegistrationAttachment`, `PutRegistrationFieldValue`, `SubmitRegistrationVersion`, `DescribeRegistrationFieldValues`, `DescribeRegistrationFieldDefinitions`, `CreateVerifiedDestinationNumber`, `DescribeVerifiedDestinationNumbers`, `SendTextMessage`, `PutKeyword`, `DescribeProtectConfigurations`, `UpdateProtectConfigurationCountryRuleSet`, `DescribeOptedOutNumbers`, `DeleteOptedOutNumber`, and `DescribeSpendLimits`. |
| `ExpiredTokenException` | Same as above — re-authenticate and retry. |

## Reference

- https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-getting-started.html
- https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-agents.html
- https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-testing.html
- https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-inbound.html
- https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-rich-messaging.html
- https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-suggestions.html
- https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-file-messages.html
- https://docs.aws.amazon.com/pinpoint/latest/apireference_smsvoicev2/API_SendRcsMessage.html
- https://docs.aws.amazon.com/sms-voice/latest/APIReference/Welcome.html

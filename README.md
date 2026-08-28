# RCS Agent Setup with AWS End User Messaging

> **Important:** This project is a sample intended for educational and demonstration purposes only. It is not intended for production use. Developers are responsible for evaluating and adapting the configurations shown here to meet their organization's security and compliance requirements before deploying in production environments.

This repository provides a complete CLI walkthrough and AI-assisted tooling for creating, configuring, and testing an RCS (Rich Communication Services) agent using [AWS End User Messaging](https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-getting-started.html).

## Overview

RCS brings branded, interactive messaging to the native messaging app on your customers' phones. This project helps you go from zero to a working RCS test agent that can send and receive branded messages, entirely from the AWS CLI.

What you will build:

1. An RCS agent with custom branding (logo, banner, accent color)
2. A test registration with all 23 required fields configured
3. Verified tester devices that can receive branded RCS messages
4. Inbound messaging with automatic keyword responses

## Repository structure

```
.
├── AGENTS.md                          # AI agent instructions (IDE-agnostic)
├── brand-assets/
│   ├── logo.svg / logo.png            # Agent logo (224x224)
│   └── banner.svg / banner.png        # Agent banner (1440x448)
├── examples/                          # RCS rich messaging code samples
├── .kiro/steering/rcs-agent-setup.md  # Kiro-specific steering file
├── LICENSE                            # MIT-0 License
├── CODE_OF_CONDUCT.md
└── CONTRIBUTING.md
```

## Prerequisites

- An AWS account with access to AWS End User Messaging
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed and configured
- IAM permissions for `pinpoint-sms-voice-v2` (see [AGENTS.md](AGENTS.md#troubleshooting) for the specific actions required)
- [librsvg](https://wiki.gnome.org/Projects/LibRsvg) for SVG to PNG conversion (`brew install librsvg` on macOS)
- A test phone that supports RCS messaging

## Quick start

### Option 1: AI-assisted setup

Open this repository in an AI coding assistant (Kiro, Cursor, Windsurf, or similar) and type `go`. The `AGENTS.md` file provides instructions that guide the AI through the entire setup process interactively.

### Option 2: Manual walkthrough

Follow the step-by-step instructions in [Creating and testing an End User Messaging RCS agent with AWS CLI](https://aws.amazon.com/blogs/messaging-and-targeting/creating-and-testing-an-end-user-messaging-rcs-agent-with-aws-cli/), which covers:

1. Creating the RCS agent container
2. Generating brand assets (logo and banner)
3. Creating and configuring the test registration (all 23 fields)
4. Submitting for approval and polling for status
5. Adding verified testers
6. Sending your first branded RCS message
7. Configuring and testing inbound messaging
8. Deleting an RCS agent (cleanup)

## Key learnings

The registration API has non-obvious behavior that this project documents:

- **Three field types**: TEXT fields use `--text-value`, SELECT fields use `--select-choices`, ATTACHMENT fields use `--registration-attachment-id`. Using the wrong parameter type causes validation errors.
- **No `--field-values` parameter**: Despite what you might expect, this parameter does not exist in the CLI.
- **No `--display-name` on agent creation**: The brand name comes from the registration, not the agent creation call.
- **`billingCategory` is required**: This SELECT field (`CONVERSATIONAL` or `NON_CONVERSATIONAL`) is easy to miss but will cause a `REQUIRES_UPDATES` denial if omitted.
- **Accent color contrast**: Must have 4.5:1 contrast ratio against white. Light or pastel colors are rejected.
- **Attachment upload**: `--attachment-body` and `--attachment-url` cannot be used together.
- **Deletion order matters**: You must delete the registration before the agent, or you get `ConflictException: RESOURCE_NOT_EMPTY`.

See the [Troubleshooting section](https://aws.amazon.com/blogs/messaging-and-targeting/creating-and-testing-an-end-user-messaging-rcs-agent-with-aws-cli/#troubleshooting) in the blog post for common errors and fixes.

## Documentation

- [AWS End User Messaging RCS Getting Started](https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-getting-started.html)
- [RCS Agents](https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-agents.html)
- [RCS Testing](https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-testing.html)
- [RCS Inbound Messaging](https://docs.aws.amazon.com/sms-voice/latest/userguide/rcs-inbound.html)
- [API Reference](https://docs.aws.amazon.com/sms-voice/latest/APIReference/Welcome.html)

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.

# Gmail Forwarder

A Python command-line tool for automatically forwarding email emails based on various search criteria. Designed to make family sharing of streaming accounts more accessible by automatically forwarding verification codes and account notifications.

## Features

- ✅ Forward latest email from inbox
- 🔍 Search by subject line (perfect for verification codes)
- 📧 Search by sender (streaming services, etc.)
- 👁️ Filter unread emails only
- 🔄 Watch mode for continuous monitoring
- 🔐 Secure Gmail authentication
- 📤 Forward to multiple family members
- 🎬 Ideal for sharing streaming service codes and notifications

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/gmail-forwarder.git
cd gmail-forwarder
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables by creating a `.env` file:
```bash
cp .env.example .env
```

4. Edit `.env` with your credentials:
```env
EMAIL_USERNAME=family-account@gmail.com
EMAIL_PASSWORD=your-app-password
FORWARD_TO=family-member1@email.com,family-member2@email.com
```

## Gmail Setup

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password:
   - Go to [Google Account Settings](https://myaccount.google.com/)
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this password in your `.env` file

## Usage

### Basic Usage

Forward the latest email:
```bash
python gmail_forwarder.py
```

## Use Cases

Perfect for family sharing scenarios:

**Streaming Service Verification:**
```bash
# Forward Netflix verification codes
python gmail_forwarder.py --subject "verification code" --from "info@account.netflix.com"

# Forward Disney+ login notifications
python gmail_forwarder.py --subject "sign-in" --from "DisneyPlus@email.disneyplus.com"

# Monitor Spotify family account emails
python gmail_forwarder.py --watch 300 --from "no-reply@spotify.com"
```

**General Family Account Management:**
```bash
# Forward any verification codes
python gmail_forwarder.py --subject "code"

# Forward account notifications from major services
python gmail_forwarder.py --from "noreply@amazon.com" --unseen
```

### Additional Examples

```bash
# General usage examples
python gmail_forwarder.py --subject "Order Confirmation"
python gmail_forwarder.py --from "noreply@amazon.com"
python gmail_forwarder.py --unseen
```

### Watch Mode

Continuously monitor for new emails:
```bash
python gmail_forwarder.py --watch 60 --subject "Order Confirmation"
```

### Test Connection

Verify your Gmail credentials:
```bash
python gmail_forwarder.py --test-login
```

## Command Line Options

| Option | Description |
|--------|-------------|
| `--subject TEXT` | Search for emails with specific subject |
| `--from EMAIL` | Search for emails from specific sender |
| `--unseen` | Only search unread emails |
| `--watch SECONDS` | Watch for new emails (check every N seconds) |
| `--test-login` | Test IMAP login credentials |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `EMAIL_USERNAME` | Your family Gmail address | Yes |
| `EMAIL_PASSWORD` | Gmail App Password | Yes |
| `FORWARD_TO` | Comma-separated family member emails | Yes |

## Requirements

- Python 3.6+
- Gmail account with App Password enabled
- Internet connection

## Security Notes

- Never commit your `.env` file to version control
- Use Gmail App Passwords, not your regular password
- Consider using a dedicated Gmail account for family forwarding
- Be mindful of what emails you're forwarding to family members

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

**Login Failed Error:**
- Ensure 2FA is enabled on your Gmail account
- Use an App Password, not your regular password
- Check that "Less secure app access" is enabled (if not using App Password)

**No Emails Found:**
- Verify your search criteria
- Check if emails exist in your inbox
- Ensure proper email format for sender searches

**SMTP Errors:**
- Verify your Gmail App Password
- Check internet connection
- Ensure Gmail SMTP is not blocked by firewall

## Support

If you encounter any issues, please [open an issue](https://github.com/yourusername/gmail-forwarder/issues) on GitHub.
import os
import imaplib
import email
from email.message import EmailMessage
import smtplib
import argparse
import time
from dotenv import load_dotenv

# ─── Load settings ───────────────────────────────────────────────────────────────
load_dotenv()
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
FORWARD_TO = os.getenv('FORWARD_TO', '').split(',')
SEARCH_SUBJECT = os.getenv('SEARCH_CRITERIA')

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


def test_login():
    print("→ Connecting to", IMAP_SERVER)
    m = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    m.debug = 4
    try:
        resp = m.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        print("→ LOGIN OK:", resp)
    except imaplib.IMAP4.error as e:
        print("→ LOGIN FAILED:", repr(e))
    finally:
        m.logout()


# ─── Functions ───────────────────────────────────────────────────────────────────

def check_email(search_criteria=None):
    """Connect to Gmail IMAP, find the latest email matching the criteria."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        mail.select('INBOX')

        # Use provided search criteria or default to ALL
        if search_criteria:
            typ, data = mail.search(None, search_criteria)
            print(f"🔍 Searching with criteria: {search_criteria}")
        else:
            typ, data = mail.search(None, 'ALL')
            print("🔍 Getting latest email from inbox")

        if typ != 'OK':
            print(f"[Error] IMAP SEARCH returned {typ}")
            return None

        uids = data[0].split()
        if not uids:
            if search_criteria:
                print(f"No emails found matching criteria: {search_criteria}")
            else:
                print("No emails found in inbox")
            return None

        # Get the latest matching email (last UID)
        latest_uid = uids[-1]

        # Fetch the full RFC822 payload of the latest email
        typ, msg_data = mail.fetch(latest_uid, '(RFC822)')
        if typ != 'OK':
            print(f"[Error] IMAP FETCH returned {typ}")
            return None

        return email.message_from_bytes(msg_data[0][1])

    except Exception as e:
        print(f"[Error] Checking email: {e}")
        return None

    finally:
        try:
            mail.logout()
        except:
            pass


def forward_email(msg):
    """Forwards the plain-text body of `msg` via Gmail SMTP."""
    try:
        # extract plain-text body
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain' and not part.get('Content-Disposition'):
                    charset = part.get_content_charset() or 'utf-8'
                    body = part.get_payload(decode=True).decode(charset, errors='replace')
                    break
        else:
            charset = msg.get_content_charset() or 'utf-8'
            body = msg.get_payload(decode=True).decode(charset, errors='replace')

        # compose forward
        fwd = EmailMessage()
        fwd['From'] = EMAIL_USERNAME
        fwd['To'] = ', '.join(FORWARD_TO)
        fwd['Subject'] = f"FWD: {msg['Subject']}"
        fwd.set_content(body)

        # send via Gmail SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_USERNAME, EMAIL_PASSWORD)
            smtp.send_message(fwd)

        print("✅ Email forwarded successfully.")
    except Exception as e:
        print(f"[Error] Forwarding email: {e}")


def on_check(search_criteria=None):
    msg = check_email(search_criteria)
    if msg:
        print(f"📧 Found email: {msg['Subject']}")
        print(f"📤 From: {msg['From']}")
        forward_email(msg)
    else:
        print("ℹ️  No matching email found.")


def main():
    parser = argparse.ArgumentParser(description='Gmail Forwarder - Forward latest email or search by criteria')
    parser.add_argument('--test-login', action='store_true', help='Test IMAP login credentials')
    parser.add_argument('--subject', type=str, help='Search for emails with specific subject')
    parser.add_argument('--from', type=str, dest='sender', help='Search for emails from specific sender')
    parser.add_argument('--unseen', action='store_true', help='Only search unread emails')
    parser.add_argument('--watch', type=int, metavar='SECONDS',
                        help='Watch for new emails and forward them (check every N seconds)')

    args = parser.parse_args()

    # Build search criteria based on arguments
    search_criteria = None
    search_parts = []

    if args.subject:
        search_parts.append(f'SUBJECT "{args.subject}"')
    if args.sender:
        search_parts.append(f'FROM "{args.sender}"')
    if args.unseen:
        search_parts.append('UNSEEN')

    if search_parts:
        if len(search_parts) == 1:
            search_criteria = search_parts[0]
        else:
            search_criteria = f'({" ".join(search_parts)})'

    if args.test_login:
        test_login()
    elif args.watch:
        if search_criteria:
            print(f'👀 Watching for emails matching: {search_criteria}')
        else:
            print('👀 Watching for latest emails...')
        print(f'⏰ Checking every {args.watch} seconds')
        print(f'📤 Forward to: {", ".join(FORWARD_TO)}')
        print('Press Ctrl+C to stop\n')

        try:
            while True:
                on_check(search_criteria)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print('\n🛑 Stopped watching for emails.')
    else:
        # Default behavior: check once
        if search_criteria:
            print(f'🔍 Searching for emails matching: {search_criteria}')
        else:
            print('🔍 Getting latest email from inbox...')
        on_check(search_criteria)


if __name__ == '__main__':
    main()
import imaplib
import email
from email.header import decode_header
from typing import List, Dict, Optional
from gm_connect.config import Config


class EmailReader:
    """
    Email reader client using IMAP.
    Supports listing folders and fetching emails.
    """

    def __init__(self, config: Optional[dict] = None):
        if config is None:
            config = Config().load()

        self.email = config["email"]
        self.password = config["password"]
        self.imap_host = config["imap_host"]
        self.imap_port = config["imap_port"]

        self.conn = None

    def connect(self):
        """Establish IMAP connection."""
        self.conn = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
        self.conn.login(self.email, self.password)

    def list_folders(self) -> List[str]:
        """List available folders (Inbox, Sent, Drafts, etc.)."""
        if not self.conn:
            self.connect()
        status, folders = self.conn.list()
        if status != "OK":
            return []
        return [folder.decode().split(' "/" ')[-1] for folder in folders]

    def fetch_emails(self, folder: str = "INBOX", limit: int = 10) -> List[Dict]:
        """
        Fetch recent emails from a given folder.

        Args:
            folder (str): Folder name (default: INBOX)
            limit (int): Number of emails to fetch

        Returns:
            List[Dict]: List of email details
        """
        if not self.conn:
            self.connect()

        self.conn.select(folder)
        status, data = self.conn.search(None, "ALL")
        if status != "OK":
            return []

        email_ids = data[0].split()
        latest_ids = email_ids[-limit:]

        emails = []
        for eid in reversed(latest_ids):
            status, msg_data = self.conn.fetch(eid, "(RFC822)")
            if status != "OK":
                continue

            raw_msg = msg_data[0][1]
            msg = email.message_from_bytes(raw_msg)

            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")

            from_ = msg.get("From")
            date_ = msg.get("Date")

            # Extract snippet (first text/plain part)
            snippet = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        snippet = part.get_payload(decode=True).decode(errors="ignore")[:200]
                        break
            else:
                snippet = msg.get_payload(decode=True).decode(errors="ignore")[:200]

            emails.append({
                "subject": subject,
                "from": from_,
                "date": date_,
                "snippet": snippet.strip()
            })

        return emails

    def logout(self):
        """Close IMAP connection."""
        if self.conn:
            self.conn.logout()
            self.conn = None
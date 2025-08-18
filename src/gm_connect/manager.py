from typing import List, Dict, Optional
from gm_connect.sender import EmailSender
from gm_connect.reader import EmailReader


class EmailManager:
    """
    High-level manager to handle sending, reading, and organizing emails.
    """

    def __init__(self, config: Optional[dict] = None):
        self.sender = EmailSender(config)
        self.reader = EmailReader(config)

    # --- Sending ---
    def send_email(self, to: List[str], subject: str, body: str, attachments: Optional[List[str]] = None) -> None:
        """Send an email via SMTP."""
        self.sender.send_email(to, subject, body, attachments)

    # --- Reading ---
    def list_folders(self) -> List[str]:
        """List available IMAP folders."""
        return self.reader.list_folders()

    def get_recent_emails(self, folder: str = "INBOX", limit: int = 10) -> List[Dict]:
        """Fetch recent emails."""
        return self.reader.fetch_emails(folder, limit)

    # --- Utility ---
    def close(self):
        """Close IMAP/SMTP connections."""
        self.reader.logout()

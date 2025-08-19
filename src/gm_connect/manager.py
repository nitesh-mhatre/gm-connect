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
    
    def delete_email(self, uid, folder="INBOX"):
        return self.reader.delete_email(uid, folder)

    def bulk_delete(self, days_old=None, from_sender=None, folder="INBOX"):
        return self.reader.bulk_delete(days_old, from_sender, folder)
    
    def move_email(self, uid, target_folder, source_folder="INBOX"):
        return self.reader.move_email(uid, target_folder, source_folder)

    # --- Utility ---
    def close(self):
        """Close IMAP/SMTP connections."""
        self.reader.logout()

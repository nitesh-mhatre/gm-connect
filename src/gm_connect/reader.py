from datetime import datetime, timedelta
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
            List[Dict]: List of email details (with UID)
        """
        if not self.conn:
            self.connect()

        self.conn.select(folder)
        status, data = self.conn.uid("search", None, "ALL")
        if status != "OK":
            return []

        email_uids = data[0].split()
        latest_uids = email_uids[-limit:]

        emails = []
        for uid in reversed(latest_uids):
            status, msg_data = self.conn.uid("fetch", uid, "(RFC822)")
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
                "uid": uid.decode(),  # ✅ add UID here
                "subject": subject,
                "from": from_,
                "date": date_,
                "snippet": snippet.strip()
            })

        return emails


    def delete_email(self, uid, folder="INBOX"):
        self.connect()
        self.conn.select(folder)
        self.conn.store(uid, '+FLAGS', r'(\Deleted)')
        self.conn.expunge()
        return f"Email {uid} deleted ✅"

    #Bulk delete
    def bulk_delete(self, days_old=None, from_sender=None, folder="INBOX", batch_size: int = 50):
        """
        Bulk delete emails based on criteria.
        Much faster than deleting one by one.

        Args:
            days_old (int): Delete emails older than X days
            from_sender (str): Delete emails from this sender
            folder (str): Mailbox folder
                "[Gmail]/All Mail" (everything)
                "[Gmail]/Trash" (deleted items)
                "[Gmail]/Spam"
                "[Gmail]/Sent Mail"
                "INBOX"

        Returns:
            str: Result message
        """
        self.connect()
        self.conn.select('INBOX' if folder == 'INBOX' else f'"{folder}"')
        #self.conn.select(folder)

        search_criteria = []

        if days_old is not None:
            date_cutoff = (datetime.now() - timedelta(days=days_old)).strftime("%d-%b-%Y")
            search_criteria.append(f"BEFORE {date_cutoff}")

        if from_sender:
            search_criteria.append(f'FROM "{from_sender}"')

        if not search_criteria:
            return "⚠️ No criteria specified for bulk delete."

        search_query = " ".join(search_criteria)
        typ, data = self.conn.uid("search", None, search_query)
        if typ != "OK" or not data[0]:
            return "No emails found matching criteria."

        uids = data[0].split()
        total = len(uids)

        # Delete in batches
        for i in range(0, total, batch_size):
            batch = uids[i:i+batch_size]
            uid_set = b",".join(batch)
            self.conn.uid("store", uid_set, "+FLAGS", r"(\Deleted)")
            self.conn.expunge()  # expunge after each batch (keeps memory low)
            print(f"✅ Deleted {i+batch_size} emails matching criteria")

        return f"✅ Deleted {total} emails matching criteria"




    def move_email(self, uid, target_folder, source_folder="INBOX"):
        self.connect()
        self.conn.select(source_folder)

        # Copy email to target
        result = self.conn.copy(uid, target_folder)
        if result[0] != "OK":
            return f"❌ Failed to move {uid} to {target_folder}"

        # Mark original as deleted
        self.conn.store(uid, '+FLAGS', r'(\Deleted)')
        self.conn.expunge()
        return f"Email {uid} moved to {target_folder} ✅"
    
    
    
    
    def logout(self):
        """Close IMAP connection."""
        if self.conn:
            self.conn.logout()
            self.conn = None
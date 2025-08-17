from .reader import EmailReader
from .sender import EmailSender
from .manager import EmailManager
from .config import Config


class EmailClient:
    """
    High-level client for managing email operations:
    - Read
    - Send
    - Delete
    - Move/Tag
    """

    def __init__(self, config: dict | None = None):
        """
        Initialize the EmailClient with optional configuration.

        Args:
            config (dict | None): Configuration dictionary.
                                  If None, will load from Config class.
        """
        self.config = config or Config().load()

        # Subcomponents
        self.reader = EmailReader(self.config)
        self.sender = EmailSender(self.config)
        self.manager = EmailManager(self.config)

    # --------------------------
    # Reading Emails
    # --------------------------
    def read_emails(self, limit: int = 10):
        """
        Fetch and return emails.

        Args:
            limit (int): Number of emails to fetch (default: 10)

        Returns:
            list: List of email summaries or objects
        """
        return self.reader.read(limit)

    # --------------------------
    # Sending Emails
    # --------------------------
    def send_email(self, to: str, subject: str, body: str, attachments: list[str] | None = None):
        """
        Send an email.

        Args:
            to (str): Recipient email address
            subject (str): Email subject
            body (str): Email body (plain text for now)
            attachments (list[str] | None): List of file paths to attach

        Returns:
            str: Status message
        """
        return self.sender.send(to, subject, body, attachments)

    # --------------------------
    # Deleting Emails
    # --------------------------
    def delete_email(self, email_id: str):
        """
        Delete an email by ID.

        Args:
            email_id (str): Identifier of the email to delete

        Returns:
            str: Status message
        """
        return self.manager.delete(email_id)

    # --------------------------
    # Moving/Tagging Emails
    # --------------------------
    def move_email(self, email_id: str, folder: str):
        """
        Move an email to a different folder.

        Args:
            email_id (str): Identifier of the email to move
            folder (str): Destination folder

        Returns:
            str: Status message
        """
        return self.manager.move(email_id, folder)

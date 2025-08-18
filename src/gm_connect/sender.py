import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import Optional
from gm_connect.config import Config


class EmailSender:
    """
    Handles sending emails via SMTP.
    """

    def __init__(self, config: dict):
        """
        Args:
            config (dict): Must include SMTP settings:
                {
                    "smtp_host": "smtp.gmail.com",
                    "smtp_port": 465,
                    "email": "your@email.com",
                    "password": "your-app-password"
                }
        """
        if config is None:
            config = Config().load()
            
        self.config = config

    def send_email_old(self, to: str, subject: str, body: str, attachments: Optional[list[str]] = None) -> str:
        """
        Send an email with optional attachments.

        Args:
            to (str): Recipient email address
            subject (str): Subject line
            body (str): Email body (plain text for now)
            attachments (list[str] | None): File paths to attach

        Returns:
            str: Status message
        """
        try:
            # Create the base message
            msg = MIMEMultipart()
            msg["From"] = self.config.get("email")
            msg["To"] = to
            msg["Subject"] = subject

            # Attach the body as plain text
            msg.attach(MIMEText(body, "plain"))

            # Handle attachments
            if attachments:
                for filepath in attachments:
                    path = Path(filepath)
                    if not path.exists():
                        raise FileNotFoundError(f"Attachment not found: {filepath}")

                    with open(path, "rb") as f:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename={path.name}",
                        )
                        msg.attach(part)

            # Connect & send
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                self.config["smtp_host"],
                self.config["smtp_port"],
                context=context,
            ) as server:
                server.login(self.config["email"], self.config["password"])
                server.sendmail(self.config["email"], to, msg.as_string())

            return f"✅ Email sent to {to} with subject '{subject}'"

        except Exception as e:
            return f"❌ Failed to send email: {e}"


    def send_email(self, to: str, subject: str, body: str, attachments: list = None):
        
        # Create a multipart message
        msg = MIMEMultipart("alternative")
        msg["From"] = self.config.get("email")
        msg["To"] = to
        msg["Subject"] = subject
        msg["Reply-To"] = self.config.get("email")
        msg["Return-Path"] = self.config.get("email")

        # Add plain text and HTML versions of the body
        plain_part = MIMEText(body, "plain")
        html_part = MIMEText(f"<html><body><p>{body}</p></body></html>", "html")

        msg.attach(plain_part)
        msg.attach(html_part)

        # Attach files if provided
        if attachments:
            for filepath in attachments:
                with open(filepath, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={os.path.basename(filepath)}",
                    )
                    msg.attach(part)

        # Send the email
        with smtplib.SMTP(self.config.get("smtp_host"), self.config.get("port")) as server:
            server.starttls()
            server.login(self.config.get("email"), self.config.get("password"))
            server.sendmail(self.config.get("email"), [to], msg.as_string())
import os
import json
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """
    Handles loading configuration for email accounts.
    Supports .env, environment variables, or JSON fallback.
    """

    def __init__(self, env_file: str = ".env", json_file: str = "config.json"):
        self.env_file = Path(env_file)
        self.json_file = Path(json_file)

    def load(self) -> dict:
        """
        Load configuration from .env, environment, or JSON fallback.

        Returns:
            dict: Config dictionary with SMTP/IMAP details
        """
        config = {}

        # 1. Try .env file
        if self.env_file.exists():
            load_dotenv(self.env_file)

        # 2. Load from environment variables
        config["email"] = os.getenv("EMAIL_ADDRESS")
        config["password"] = os.getenv("EMAIL_PASSWORD")
        config["smtp_host"] = os.getenv("SMTP_HOST", "smtp.gmail.com")
        config["smtp_port"] = int(os.getenv("SMTP_PORT", 465))
        config["imap_host"] = os.getenv("IMAP_HOST", "imap.gmail.com")
        config["imap_port"] = int(os.getenv("IMAP_PORT", 993))

        # 3. Fallback to JSON config file
        if not config["email"] or not config["password"]:
            if self.json_file.exists():
                with open(self.json_file, "r", encoding="utf-8") as f:
                    json_config = json.load(f)
                config.update(json_config)

        # 4. Validation
        if not config.get("email") or not config.get("password"):
            raise ValueError(
                "❌ Missing email credentials. "
                "Set EMAIL_ADDRESS & EMAIL_PASSWORD in .env or config.json"
            )

        return config

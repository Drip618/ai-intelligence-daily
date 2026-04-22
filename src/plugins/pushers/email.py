from __future__ import annotations

import smtplib
from email.mime.text import MIMEText

from loguru import logger

from src.plugins.pushers.base import BasePusher


class EmailPusher(BasePusher):
    """SMTP Email pusher."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        smtp_user: str,
        smtp_password: str,
        smtp_to: str,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_to = smtp_to

    def push(self, content: str, **kwargs) -> bool:
        msg = MIMEText(content, "html", "utf-8")
        msg["Subject"] = "Daily AI Intelligence Report"
        msg["From"] = self.smtp_user
        msg["To"] = self.smtp_to

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, [self.smtp_to], msg.as_string())
            logger.info("Email push successful")
            return True
        except Exception as e:
            logger.error(f"Email push failed: {e}")
            return False

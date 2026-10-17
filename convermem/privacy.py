# D:\AI-Tools\convermem\convermem\privacy.py
import re
from typing import List, Dict, Any

class PrivacyShield:
    """Security and PII scanner powered by DavidAgentCrew defense rules."""

    SECRET_PATTERNS = [
        ("API_KEY_OPENAI", r"sk-[a-zA-Z0-9_-]{20,}", "[REDACTED_API_KEY]"),
        ("API_KEY_GITHUB", r"gh[pousr]_[a-zA-Z0-9]{20,}", "[REDACTED_API_KEY]"),
        ("AWS_KEY", r"AKIA[0-9A-Z]{16}", "[REDACTED_AWS_KEY]"),
        ("BEARER_TOKEN", r"(?i)bearer\s+[a-zA-Z0-9\._\-]{25,}", "Bearer [REDACTED_TOKEN]"),
        ("PHONE_THAI", r"(?<!\d)0[689]\d{8}(?!\d)", "[REDACTED_PHONE_NUMBER]"),
        ("EMAIL", r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED_EMAIL]"),
    ]

    def scan(self, text: str) -> List[Dict[str, Any]]:
        """Scans text and returns list of detected sensitive data matches."""
        findings = []
        for label, pattern, _ in self.SECRET_PATTERNS:
            for match in re.finditer(pattern, text):
                findings.append({
                    "type": label,
                    "matched": match.group(0),
                    "start": match.start(),
                    "end": match.end()
                })
        return findings

    def redact(self, text: str) -> str:
        """Redacts all detected sensitive secrets and PII from text."""
        result = text
        for _, pattern, replacement in self.SECRET_PATTERNS:
            result = re.sub(pattern, replacement, result)
        return result

# D:\AI-Tools\convermem\tests\test_privacy.py
from convermem.privacy import PrivacyShield

def test_detect_and_redact_secrets():
    shield = PrivacyShield()
    sample_text = (
        "Here is my OpenAI key sk-proj-1234567890abcdef1234567890abcdef and "
        "my GitHub token ghp_1234567890abcdef1234567890abcdef12. "
        "Contact me at 0891234567 or email user@example.com."
    )
    findings = shield.scan(sample_text)
    assert len(findings) >= 3
    
    redacted = shield.redact(sample_text)
    assert "sk-proj-" not in redacted
    assert "ghp_" not in redacted
    assert "0891234567" not in redacted
    assert "[REDACTED_API_KEY]" in redacted
    assert "[REDACTED_PHONE_NUMBER]" in redacted

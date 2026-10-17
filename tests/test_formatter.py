# D:\AI-Tools\convermem\tests\test_formatter.py
from convermem.formatter import MarkdownFormatter

def test_formatter_renders_clean_turn():
    turn = {
        "user": "Hello agent!",
        "model": "Hello user, how can I help?",
        "time": "2026-10-17T12:00:00Z",
        "session_id": "session-abc"
    }
    formatter = MarkdownFormatter()
    md = formatter.format_turn(turn, index=1)
    assert "### 💬 Turn 1" in md
    assert "2026-10-17T12:00:00Z" in md
    assert "session-abc" in md
    assert "> Hello agent!" in md
    assert "Hello user, how can I help?" in md

# D:\AI-Tools\convermem\convermem\formatter.py
from typing import Dict, Any

class MarkdownFormatter:
    """Formats clean dialogue turns into structured GitHub Flavored Markdown."""

    def format_turn(self, turn: Dict[str, Any], index: int) -> str:
        user_text = turn.get("user", "").strip()
        model_text = turn.get("model", "").strip() or "*(Action executed without commentary)*"
        time_str = turn.get("time") or "N/A"
        session_id = turn.get("session_id") or "N/A"

        quoted_user = "\n> ".join(user_text.splitlines()) if user_text else "*(Empty)*"

        return f"""---

### 💬 Turn {index}
**⏱️ Timestamp:** `{time_str}` | **🔗 Session ID:** `{session_id}`

#### 👤 User:
> {quoted_user}

#### 🤖 AI Assistant:
{model_text}
"""

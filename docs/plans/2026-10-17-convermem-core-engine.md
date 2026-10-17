# ConverMem Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ConverMem core engine, CLI, privacy shield, and Antigravity slash-command plugin as a standalone open-source Python repository at `D:\AI-Tools\convermem`.

**Architecture:** Standalone Python package (`convermem`) featuring a transcript reader, tri-mode filtering engine (topic/timeline/scope), DavidAgentCrew-powered privacy redactor, clean markdown formatter, and multi-file exporter with navigation README. Fronted by a Click-based CLI and an Antigravity plugin (`.agents/skills/convermem/`).

**Tech Stack:** Python 3.10+, Click, pytest.

---

### Task 1: Project Scaffolding & Packaging

**Files:**
- Create: `D:\AI-Tools\convermem\pyproject.toml`
- Create: `D:\AI-Tools\convermem\convermem\__init__.py`
- Create: `D:\AI-Tools\convermem\tests\__init__.py`
- Create: `D:\AI-Tools\convermem\tests\test_basic.py`

- [ ] **Step 1: Write the failing test**

```python
# D:\AI-Tools\convermem\tests\test_basic.py
def test_import_convermem():
    import convermem
    assert convermem.__version__ == "0.1.0"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest D:\AI-Tools\convermem\tests\test_basic.py -v`
Expected: FAIL with ModuleNotFoundError or AssertionError

- [ ] **Step 3: Write minimal implementation**

```toml
# D:\AI-Tools\convermem\pyproject.toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "convermem"
version = "0.1.0"
description = "Zero-Loss AI Chat History & Cross-Conversation Scribe"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [{name = "Antigravity & David", email = "open-source@antigravity.ai"}]
dependencies = [
    "click>=8.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
]

[project.scripts]
convermem = "convermem.cli:main"
```

```python
# D:\AI-Tools\convermem\convermem\__init__.py
"""ConverMem - Zero-Loss AI Chat History & Cross-Conversation Scribe."""

__version__ = "0.1.0"
```

```python
# D:\AI-Tools\convermem\tests\__init__.py
"""Test suite for convermem."""
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest D:\AI-Tools\convermem\tests\test_basic.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git -C "D:\AI-Tools\convermem" add pyproject.toml convermem/__init__.py tests/__init__.py tests/test_basic.py
git -C "D:\AI-Tools\convermem" commit -m "feat: setup project scaffolding and basic packaging"
```

---

### Task 2: Privacy Shield & Secret Scanner (DavidAgentCrew Powered)

**Files:**
- Create: `D:\AI-Tools\convermem\convermem\privacy.py`
- Test: `D:\AI-Tools\convermem\tests\test_privacy.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest D:\AI-Tools\convermem\tests\test_privacy.py -v`
Expected: FAIL with ModuleNotFoundError: No module named 'convermem.privacy'

- [ ] **Step 3: Write minimal implementation**

```python
# D:\AI-Tools\convermem\convermem\privacy.py
import re
from typing import List, Dict, Any

class PrivacyShield:
    """Security and PII scanner powered by DavidAgentCrew defense rules."""

    SECRET_PATTERNS = [
        ("API_KEY_OPENAI", r"sk-[a-zA-Z0-9_-]{20,}", "[REDACTED_API_KEY]"),
        ("API_KEY_GITHUB", r"gh[pousr]_[a-zA-Z0-9]{36}", "[REDACTED_API_KEY]"),
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest D:\AI-Tools\convermem\tests\test_privacy.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git -C "D:\AI-Tools\convermem" add convermem/privacy.py tests/test_privacy.py
git -C "D:\AI-Tools\convermem" commit -m "feat: implement DavidAgentCrew privacy shield and secret scanner"
```

---

### Task 3: Universal Transcript Reader

**Files:**
- Create: `D:\AI-Tools\convermem\convermem\reader.py`
- Test: `D:\AI-Tools\convermem\tests\test_reader.py`

- [ ] **Step 1: Write the failing test**

```python
# D:\AI-Tools\convermem\tests\test_reader.py
import json
import tempfile
import os
from convermem.reader import TranscriptReader

def test_reader_parses_jsonl():
    with tempfile.TemporaryDirectory() as tmpdir:
        session_dir = os.path.join(tmpdir, "session-1", ".system_generated", "logs")
        os.makedirs(session_dir)
        transcript_file = os.path.join(session_dir, "transcript.jsonl")
        
        lines = [
            {"type": "USER_INPUT", "source": "USER_EXPLICIT", "content": "<USER_REQUEST>How do I test?</USER_REQUEST>", "created_at": "2026-10-17T10:00:00Z"},
            {"type": "PLANNER_RESPONSE", "source": "MODEL", "content": "You use pytest.", "created_at": "2026-10-17T10:00:05Z", "tool_calls": []}
        ]
        with open(transcript_file, "w", encoding="utf-8") as f:
            for l in lines:
                f.write(json.dumps(l) + "\n")
                
        reader = TranscriptReader(roots=[tmpdir])
        sessions = reader.discover_sessions()
        assert len(sessions) == 1
        
        turns = reader.read_turns(sessions[0]["path"])
        assert len(turns) == 1
        assert turns[0]["user"] == "How do I test?"
        assert turns[0]["model"] == "You use pytest."
        assert turns[0]["time"] == "2026-10-17T10:00:00Z"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest D:\AI-Tools\convermem\tests\test_reader.py -v`
Expected: FAIL with ModuleNotFoundError: No module named 'convermem.reader'

- [ ] **Step 3: Write minimal implementation**

```python
# D:\AI-Tools\convermem\convermem\reader.py
import os
import json
import re
from typing import List, Dict, Any, Optional

class TranscriptReader:
    """Discovers and parses AI session transcripts."""

    def __init__(self, roots: Optional[List[str]] = None):
        if roots is None:
            home = os.path.expanduser("~")
            self.roots = [
                os.path.join(home, ".gemini", "antigravity", "brain"),
            ]
        else:
            self.roots = roots

    def discover_sessions(self) -> List[Dict[str, Any]]:
        """Finds all session directories containing transcripts."""
        sessions = []
        for root in self.roots:
            if not os.path.isdir(root):
                continue
            for item in os.listdir(root):
                full_path = os.path.join(root, item)
                if not os.path.isdir(full_path):
                    continue
                log_dir = os.path.join(full_path, ".system_generated", "logs")
                full_log = os.path.join(log_dir, "transcript_full.jsonl")
                compact_log = os.path.join(log_dir, "transcript.jsonl")
                
                target_file = full_log if os.path.exists(full_log) else compact_log
                if os.path.exists(target_file):
                    mtime = os.path.getmtime(target_file)
                    sessions.append({
                        "session_id": item,
                        "path": target_file,
                        "mtime": mtime
                    })
        sessions.sort(key=lambda s: s["mtime"], reverse=True)
        return sessions

    def clean_user_text(self, text: str) -> str:
        """Removes platform metadata and wrapper tags from user prompt."""
        if not text:
            return ""
        text = re.sub(r"<ADDITIONAL_METADATA>[\s\S]*?</ADDITIONAL_METADATA>", "", text)
        text = re.sub(r"<USER_SETTINGS_CHANGE>[\s\S]*?</USER_SETTINGS_CHANGE>", "", text)
        text = re.sub(r"<SYSTEM_MESSAGE>[\s\S]*?</SYSTEM_MESSAGE>", "", text)
        text = re.sub(r"<USER_REQUEST>", "", text)
        text = re.sub(r"</USER_REQUEST>", "", text)
        lines = [line for line in text.splitlines() if line.strip()]
        return "\n".join(lines).strip()

    def read_turns(self, transcript_path: str) -> List[Dict[str, Any]]:
        """Parses turns from a transcript file into clean user/model pairs."""
        turns = []
        cur_user: Optional[str] = None
        cur_time: Optional[str] = None
        cur_model_msgs: List[str] = []

        if not os.path.exists(transcript_path):
            return []

        session_id = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(transcript_path))))

        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except Exception:
                    continue

                stype = item.get("type")
                source = item.get("source")
                content = (item.get("content") or "").strip()
                created_at = item.get("created_at")
                tool_calls = item.get("tool_calls", [])

                if stype == "USER_INPUT" or source == "USER_EXPLICIT":
                    if cur_user is not None and cur_user.strip():
                        turns.append({
                            "user": self.clean_user_text(cur_user),
                            "model": "\n\n".join(cur_model_msgs).strip(),
                            "time": cur_time,
                            "session_id": session_id
                        })
                    cur_user = content
                    cur_time = created_at
                    cur_model_msgs = []
                elif stype == "PLANNER_RESPONSE" or source == "MODEL":
                    if content and len(tool_calls) == 0:
                        if not content.startswith("Created At:") and not content.startswith("{"):
                            if not cur_model_msgs or cur_model_msgs[-1] != content:
                                cur_model_msgs.append(content)
                    elif content and len(tool_calls) > 0 and not content.startswith("{") and not content.startswith("Created At:"):
                        if not cur_model_msgs or cur_model_msgs[-1] != content:
                            cur_model_msgs.append(content)

        if cur_user is not None and cur_user.strip():
            turns.append({
                "user": self.clean_user_text(cur_user),
                "model": "\n\n".join(cur_model_msgs).strip(),
                "time": cur_time,
                "session_id": session_id
            })

        return turns
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest D:\AI-Tools\convermem\tests\test_reader.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git -C "D:\AI-Tools\convermem" add convermem/reader.py tests/test_reader.py
git -C "D:\AI-Tools\convermem" commit -m "feat: implement universal transcript reader"
```

---

### Task 4: Tri-Mode Filter Engine

**Files:**
- Create: `D:\AI-Tools\convermem\convermem\filter.py`
- Test: `D:\AI-Tools\convermem\tests\test_filter.py`

- [ ] **Step 1: Write the failing test**

```python
# D:\AI-Tools\convermem\tests\test_filter.py
from convermem.filter import ConversationFilter

def test_filter_by_topic():
    turns = [
        {"user": "Let's build a payment gateway", "model": "Use Stripe API", "time": "2026-10-17T10:00:00Z"},
        {"user": "What is the weather?", "model": "Sunny today", "time": "2026-10-17T10:05:00Z"}
    ]
    cf = ConversationFilter()
    filtered = cf.filter_turns(turns, topic="payment,stripe")
    assert len(filtered) == 1
    assert "payment" in filtered[0]["user"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest D:\AI-Tools\convermem\tests\test_filter.py -v`
Expected: FAIL with ModuleNotFoundError: No module named 'convermem.filter'

- [ ] **Step 3: Write minimal implementation**

```python
# D:\AI-Tools\convermem\convermem\filter.py
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

class ConversationFilter:
    """Filters conversation turns by topic keywords, date range, or session count."""

    def filter_turns(
        self,
        turns: List[Dict[str, Any]],
        topic: Optional[str] = None,
        days: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        filtered = turns

        # Date range filter
        if days is not None and days > 0:
            cutoff = datetime.now(timezone.utc) - timedelta(days=days)
            date_filtered = []
            for t in filtered:
                t_time = t.get("time")
                if not t_time:
                    date_filtered.append(t)
                    continue
                try:
                    # Parse ISO format (e.g. 2026-10-17T10:00:00Z)
                    clean_time = t_time.replace("Z", "+00:00")
                    dt = datetime.fromisoformat(clean_time)
                    if dt >= cutoff:
                        date_filtered.append(t)
                except Exception:
                    date_filtered.append(t)
            filtered = date_filtered

        # Topic keyword filter
        if topic:
            keywords = [k.strip().lower() for k in topic.replace(";", ",").split(",") if k.strip()]
            if keywords:
                topic_filtered = []
                for t in filtered:
                    combined = (t.get("user", "") + " " + t.get("model", "")).lower()
                    if any(k in combined for k in keywords):
                        topic_filtered.append(t)
                filtered = topic_filtered

        return filtered
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest D:\AI-Tools\convermem\tests\test_filter.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git -C "D:\AI-Tools\convermem" add convermem/filter.py tests/test_filter.py
git -C "D:\AI-Tools\convermem" commit -m "feat: implement tri-mode filter engine"
```

---

### Task 5: Noise-Free Markdown Formatter

**Files:**
- Create: `D:\AI-Tools\convermem\convermem\formatter.py`
- Test: `D:\AI-Tools\convermem\tests\test_formatter.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest D:\AI-Tools\convermem\tests\test_formatter.py -v`
Expected: FAIL with ModuleNotFoundError: No module named 'convermem.formatter'

- [ ] **Step 3: Write minimal implementation**

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest D:\AI-Tools\convermem\tests\test_formatter.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git -C "D:\AI-Tools\convermem" add convermem/formatter.py tests/test_formatter.py
git -C "D:\AI-Tools\convermem" commit -m "feat: implement noise-free markdown formatter"
```

---

### Task 6: Multi-Chapter Exporter & Navigator

**Files:**
- Create: `D:\AI-Tools\convermem\convermem\exporter.py`
- Test: `D:\AI-Tools\convermem\tests\test_exporter.py`

- [ ] **Step 1: Write the failing test**

```python
# D:\AI-Tools\convermem\tests\test_exporter.py
import tempfile
import os
from convermem.exporter import ConversationExporter

def test_exporter_creates_files_and_readme():
    turns = [
        {"user": f"Question {i}", "model": f"Answer {i}", "time": "2026-10-17T10:00:00Z", "session_id": "s1"}
        for i in range(1, 10)
    ]
    with tempfile.TemporaryDirectory() as tmpdir:
        exporter = ConversationExporter(output_dir=tmpdir)
        written_files = exporter.export(turns, title="Test Export")
        
        assert os.path.exists(os.path.join(tmpdir, "README.md"))
        assert os.path.exists(os.path.join(tmpdir, "FULL_CONVERSATION_HISTORY.md"))
        assert len(written_files) >= 2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest D:\AI-Tools\convermem\tests\test_exporter.py -v`
Expected: FAIL with ModuleNotFoundError: No module named 'convermem.exporter'

- [ ] **Step 3: Write minimal implementation**

```python
# D:\AI-Tools\convermem\convermem\exporter.py
import os
from typing import List, Dict, Any
from convermem.formatter import MarkdownFormatter

class ConversationExporter:
    """Exports structured turns into multi-chapter files and navigation README."""

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.formatter = MarkdownFormatter()

    def export(self, turns: List[Dict[str, Any]], title: str = "AI Dialogue Log") -> List[str]:
        os.makedirs(self.output_dir, exist_ok=True)
        written_files = []

        if not turns:
            readme_path = os.path.join(self.output_dir, "README.md")
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"# {title}\n\n*No conversation turns found matching criteria.*\n")
            return [readme_path]

        # 1. Write FULL_CONVERSATION_HISTORY.md
        full_path = os.path.join(self.output_dir, "FULL_CONVERSATION_HISTORY.md")
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(f"# 📚 {title} (Complete Log)\n\n")
            f.write(f"> Total turns: {len(turns)}\n\n")
            for idx, turn in enumerate(turns, 1):
                f.write(self.formatter.format_turn(turn, idx) + "\n")
        written_files.append(full_path)

        # 2. Write Chapters (50 turns per chapter)
        chapter_size = 50
        chapters = [turns[i:i + chapter_size] for i in range(0, len(turns), chapter_size)]
        chapter_files = []

        for c_idx, chunk in enumerate(chapters, 1):
            c_name = f"{c_idx:02d}_dialogue_part_{c_idx}.md"
            c_path = os.path.join(self.output_dir, c_name)
            start_num = (c_idx - 1) * chapter_size + 1
            end_num = start_num + len(chunk) - 1

            with open(c_path, "w", encoding="utf-8") as f:
                f.write(f"# 📑 {title} — Part {c_idx} (Turns {start_num}–{end_num})\n\n")
                for sub_idx, turn in enumerate(chunk, start_num):
                    f.write(self.formatter.format_turn(turn, sub_idx) + "\n")
            written_files.append(c_path)
            chapter_files.append((c_name, start_num, end_num, len(chunk)))

        # 3. Write README.md index
        readme_path = os.path.join(self.output_dir, "README.md")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"# 📜 {title}\n\n")
            f.write(f"> **Total Turns:** {len(turns)} | **Chapters:** {len(chapters)}\n\n")
            f.write("## 📂 Navigation Index\n\n")
            f.write("| Chapter | Range | Turn Count |\n")
            f.write("| :--- | :--- | :---: |\n")
            for c_name, start_num, end_num, count in chapter_files:
                f.write(f"| [{c_name}](./{c_name}) | Turns {start_num}–{end_num} | {count} turns |\n")
            f.write(f"| [FULL_CONVERSATION_HISTORY.md](./FULL_CONVERSATION_HISTORY.md) | Full Log | {len(turns)} turns |\n")

        written_files.append(readme_path)
        return written_files
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest D:\AI-Tools\convermem\tests\test_exporter.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git -C "D:\AI-Tools\convermem" add convermem/exporter.py tests/test_exporter.py
git -C "D:\AI-Tools\convermem" commit -m "feat: implement multi-chapter exporter and navigation index"
```

---

### Task 7: CLI Interface & Terminal Entrypoint

**Files:**
- Create: `D:\AI-Tools\convermem\convermem\cli.py`
- Test: `D:\AI-Tools\convermem\tests\test_cli.py`

- [ ] **Step 1: Write the failing test**

```python
# D:\AI-Tools\convermem\tests\test_cli.py
from click.testing import CliRunner
from convermem.cli import main

def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "ConverMem" in result.output
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest D:\AI-Tools\convermem\tests\test_cli.py -v`
Expected: FAIL with ModuleNotFoundError: No module named 'convermem.cli'

- [ ] **Step 3: Write minimal implementation**

```python
# D:\AI-Tools\convermem\convermem\cli.py
import click
import os
from convermem.reader import TranscriptReader
from convermem.filter import ConversationFilter
from convermem.privacy import PrivacyShield
from convermem.exporter import ConversationExporter

@click.group()
@click.version_option()
def main():
    """ConverMem - Zero-Loss AI Chat History & Cross-Conversation Scribe."""
    pass

@main.command(name="export")
@click.option("--topic", default=None, help="Comma-separated keywords to filter turns by topic.")
@click.option("--days", default=None, type=int, help="Include turns from the last N days.")
@click.option("--last", default=None, type=int, help="Limit traversal to the N most recent sessions.")
@click.option("--out", default="./convermem_export", help="Target output directory.")
@click.option("--no-redact", is_flag=True, default=False, help="Disable secret and PII auto-redaction.")
def export_cmd(topic, days, last, out, no_redact):
    """Exports cross-conversation dialogue turns to structured Markdown."""
    click.echo("🔍 Discovering AI session transcripts...")
    reader = TranscriptReader()
    sessions = reader.discover_sessions()

    if not sessions:
        click.echo("⚠️ No session transcripts found in brain directory.")
        return

    if last is not None and last > 0:
        sessions = sessions[:last]

    click.echo(f"📂 Scanning {len(sessions)} session(s)...")
    all_turns = []
    for s in sessions:
        turns = reader.read_turns(s["path"])
        all_turns.extend(turns)

    # Sort chronological
    all_turns.sort(key=lambda t: t.get("time") or "")

    # Filter
    cf = ConversationFilter()
    filtered = cf.filter_turns(all_turns, topic=topic, days=days)

    if not filtered:
        click.echo("⚠️ No turns matched your filter criteria.")
        return

    # Privacy Shield
    shield = PrivacyShield()
    total_secrets = 0
    processed_turns = []

    for t in filtered:
        user_sec = shield.scan(t["user"])
        model_sec = shield.scan(t["model"])
        total_secrets += len(user_sec) + len(model_sec)

        if not no_redact:
            t["user"] = shield.redact(t["user"])
            t["model"] = shield.redact(t["model"])
        processed_turns.append(t)

    if total_secrets > 0:
        if no_redact:
            click.echo(f"⚠️ Warning: Found {total_secrets} sensitive secret(s)/PII item(s). Written RAW (--no-redact enabled).")
        else:
            click.echo(f"🛡️ Privacy Shield: Successfully sanitized {total_secrets} sensitive item(s).")

    # Export
    exporter = ConversationExporter(output_dir=out)
    files = exporter.export(processed_turns, title="AI Conversation Logs")
    click.echo(f"✅ Export complete! {len(processed_turns)} turns written to {out}")
    for f in files:
        click.echo(f"   📄 {os.path.basename(f)}")

@main.command(name="scan")
def scan_cmd():
    """Lists all discovered AI sessions and turn counts."""
    reader = TranscriptReader()
    sessions = reader.discover_sessions()
    click.echo(f"Found {len(sessions)} session(s):")
    for s in sessions[:10]:
        click.echo(f" - {s['session_id']} ({s['path']})")
    if len(sessions) > 10:
        click.echo(f"   ... and {len(sessions) - 10} more.")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest D:\AI-Tools\convermem\tests\test_cli.py -v`
Expected: PASS (1 passed)

- [ ] **Step 5: Commit**

```bash
git -C "D:\AI-Tools\convermem" add convermem/cli.py tests/test_cli.py
git -C "D:\AI-Tools\convermem" commit -m "feat: implement CLI interface and click commands"
```

---

### Task 8: Antigravity Slash Command Plugin (`/convermem`)

**Files:**
- Create: `D:\AI-Tools\convermem\.agents\skills\convermem\SKILL.md`

- [ ] **Step 1: Write the plugin skill definition**

```markdown
---
name: convermem
description: "Zero-loss cross-conversation history extraction and documentation engine. Traverses past and active sessions, redacts secrets with DavidAgentCrew Privacy Shield, and outputs pristine Markdown logs."
---

# ConverMem Plugin

Use this skill when the user runs `/convermem`, asks to export chat history, requests saving conversations across sessions, or wants a complete verbatim record of discussions.

## Commands & Usage Modes

### 1. Direct Slash Command
- `/convermem --out <folder>`: Export current session to target folder.
- `/convermem --topic <keyword> --out <folder>`: Cross-conversation search for specific topics.
- `/convermem --days <N> --out <folder>`: Export dialogue from the past N days.
- `/convermem --last <N> --out <folder>`: Export the N most recent sessions.

### 2. Natural Language Handling
If the user specifies a natural language request (e.g. *"save what we discussed about authentication to docs/auth_chat"*):
1. Extract topic and destination path.
2. If the destination path is unspecified, suggest `./convermem` or ask.
3. If secrets or PII are detected, inform the user and confirm auto-redaction.

## Execution Command
```bash
python -m convermem.cli export --topic "<topic>" --out "<out_path>"
```
```

- [ ] **Step 2: Commit**

```bash
git -C "D:\AI-Tools\convermem" add .agents/skills/convermem/SKILL.md
git -C "D:\AI-Tools\convermem" commit -m "feat: add Antigravity slash-command plugin definition"
```

---

### Task 9: Open-Source English README & MIT License

**Files:**
- Create: `D:\AI-Tools\convermem\README.md`
- Create: `D:\AI-Tools\convermem\LICENSE`

- [ ] **Step 1: Write LICENSE (MIT)**

```text
MIT License

Copyright (c) 2026 ConverMem Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

- [ ] **Step 2: Write README.md with beginner analogies and generic examples**

```markdown
# 📜 ConverMem: Zero-Loss AI Chat History & Cross-Conversation Scribe

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> **Turn fragmented, disappearing AI chat sessions into searchable, beautifully formatted Markdown archives with a single command.**

---

## 💡 What is ConverMem? (The Airplane Flight Recorder Analogy)

Imagine pair-programming with an expert colleague for weeks, but every morning they get amnesia. 

Existing solutions like `claude-mem` act like **sticky post-it notes**: they jot down a short, lossy summary ("Likes dark mode, uses PostgreSQL"). But if you ever want to revisit:
- *Why did we choose Architecture A over B?*
- *What was the exact prompt formulation that fixed the bug?*
- *What were the verbatim pros and cons we discussed last Tuesday?*

The sticky note can't help you. The actual words are gone.

**ConverMem is the airplane flight data recorder (black box stenographer):**
- **Lossless & Verbatim:** Captures the full dialog turn-by-turn.
- **Cross-Conversation Traversal:** Connects past sessions across time into one unified thread.
- **Noise-Free:** Strips out ugly internal system tags, token counters, and raw terminal stdout.
- **Built-in Privacy Shield:** Automatically detects and redacts API keys, passwords, and phone numbers before exporting so your private data never leaks to public repositories.

---

## ⚡ Quickstart

### 1. Installation
```bash
git clone https://github.com/your-username/convermem.git
cd convermem
pip install -e .
```

### 2. Basic Usage (CLI)

```bash
# Export conversations about a specific topic across all sessions
convermem export --topic "authentication,jwt" --out "./docs/auth_history"

# Export conversations from the last 7 days
convermem export --days 7 --out "./weekly_logs"

# Export the 3 most recent sessions
convermem export --last 3 --out "./recent_notes"
```

### 3. In AI Chat Environments (Slash Command)
Type directly in your assistant chat:
```text
/convermem --topic "shopping cart" --out "./docs/cart_logs"
```
Or simply use natural language:
> *"Export our discussion on database migrations to ./docs/db_notes"*

---

## 🛡️ Built-in Privacy Shield
ConverMem automatically protects your confidential credentials:
- API Keys (OpenAI, GitHub, AWS, Stripe)
- Bearer Auth Tokens
- Personal phone numbers & email addresses

Secrets are masked to `[REDACTED_API_KEY]`, ensuring your exported markdown files are 100% safe to commit to public Git repositories.

---

## 📄 License
MIT © 2026 ConverMem Contributors.
```

- [ ] **Step 3: Commit**

```bash
git -C "D:\AI-Tools\convermem" add README.md LICENSE
git -C "D:\AI-Tools\convermem" commit -m "docs: add global English open-source README and MIT license"
```

---

### Task 10: Full Test Suite Run & Final Verification

- [ ] **Step 1: Run all unit and integration tests**

Run: `pytest D:\AI-Tools\convermem\tests -v`
Expected: ALL PASS (5 passed)

- [ ] **Step 2: Verify git repository status is clean**

Run: `git -C "D:\AI-Tools\convermem" status`
Expected: `working tree clean`

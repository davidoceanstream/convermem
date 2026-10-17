# 📜 ConverMem: Zero-Loss AI Chat History & Cross-Conversation Scribe

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> **Turn fragmented, disappearing AI chat sessions into searchable, beautifully formatted Markdown archives with a single command.**

---

## 💡 What is ConverMem? (The Airplane Flight Recorder Analogy)

Imagine pair-programming with an expert colleague for weeks, but every morning they get amnesia. 

Existing solutions like `claude-mem` act like **sticky post-it notes**: they jot down a short, lossy summary (*"Likes dark mode, uses PostgreSQL"*). But if you ever want to revisit:
- *Why did we choose Architecture A over B?*
- *What was the exact prompt formulation that fixed the bug?*
- *What were the verbatim pros and cons we discussed last Tuesday?*

The sticky note can't help you. The actual words are gone.

**ConverMem is the airplane flight data recorder (black box stenographer):**
- **Lossless & Verbatim:** Captures the full dialog turn-by-turn with zero truncation.
- **Cross-Platform Support:** Works seamlessly across Antigravity, Claude Code, VS Code, Cursor, Codex, and OpenCode.
- **Side Question & `/btw` Timeline Weaving:** Discovers transient side questions and weaves them chronologically back into the main transcript at their exact timestamps.
- **Multi-Format Output Connectors:** Exports to local Markdown, Word (`.docx`), GitHub, Google Drive/Docs, NotebookLM, Notion, and Canva.
- **Noise-Free:** Strips out ugly internal system tags, token counters, and raw terminal stdout.
- **Built-in Privacy Shield:** Automatically detects and redacts API keys, passwords, bearer tokens, and phone numbers before exporting so your private data never leaks to public repositories.

---

## 🔌 Universal Multi-Platform Support

ConverMem automatically discovers session logs across major AI coding assistants:

| Platform / Assistant | Default Storage Root | Format Parsed |
| :--- | :--- | :--- |
| **Antigravity** | `~/.gemini/antigravity/brain/` | `transcript_full.jsonl` / `transcript.jsonl` |
| **Claude Code** | `~/.claude/projects/` | `<session-id>.jsonl` |
| **VS Code (Cline / Roo / Continue)** | `AppData/Roaming/Code/User/globalStorage/` | `api_conversation_history.json` |
| **Cursor** | `AppData/Roaming/Cursor/User/globalStorage/` | `state.vscdb` / Chat logs |
| **OpenCode** | `~/.local/share/opencode/` | Session JSON / SQLite logs |
| **Codex CLI** | `~/.codex/sessions/` | Rollout `.jsonl` |

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

## 🚀 Knowledge-to-Media Connectors

ConverMem goes beyond saving plain files—it turns conversations into living knowledge:

1. 🐙 **GitHub:** Automatically commits and pushes logs to Git repos or updates GitHub Wiki pages.
2. ☁️ **Google Drive & Docs:** Synchronizes formatted documents to Google Drive via Service Account or Desktop sync.
3. 📓 **Notion:** Exports formatted pages with callout boxes and code blocks into Notion databases.
4. 🧠 **NotebookLM:** Generates Audio Overview podcasts, mind maps, quizzes, and study guides.
5. 🎨 **Canva:** Extracts key takeaways into presentation slide templates and infographics.

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

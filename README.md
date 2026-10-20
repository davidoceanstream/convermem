<div align="center">

![ConverMem — Zero-Loss AI Chat Scribe & Cross-Session Memory Engine](./assets/hero-banner.png)

# 📜 ConverMem
### Zero-Loss AI Chat History & Cross-Conversation Memory Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-7%2F7%20passing-brightgreen.svg)]()
[![Privacy Shield](https://img.shields.io/badge/Privacy%20Shield-DavidAgentCrew%20Active-emerald.svg)]()

<p align="center">
  <b>Turn disappearing AI chat sessions into permanent, beautifully formatted knowledge archives.</b>
</p>

</div>

---

## ⚡ What is ConverMem?

**ConverMem is an open-source conversation archiver and context bridge for AI assistants (such as Antigravity, Claude Code, Codex, Cursor, VS Code, OpenCode, etc.).**

It solves one of the biggest challenges when working with AI: **lossy context and manual copy-pasting.**

- ⚡ **Slash Command (/convermem)**: Run directly inside your active chat session.
- 🧠 **Context Bridge for New Chats**: Hand off complete, step-by-step conversation history to new chats or other AI models without confusion.
- 💻 **Terminal CLI**: Traverse and extract past sessions from local storage with one command.

> **The Problem It Solves:**  
> When sessions get long, built-in /compact or summary tools often throw away the fine details—the reasoning, failed attempts, and exact code changes. When you start a new chat, the new AI gets confused because the summary lacks context. On the other hand, manually copying logs from console histories is tedious.  
> 
> **ConverMem gives you total control over how your chats are saved:**  
> - 📜 **Full Turn-by-Turn Verbatim:** Capture the complete back-and-forth dialogue without losing a single nuance.  
> - 🎯 **Milestones & Solutions Only:** Filter out failed trials and errors to save only the turns where solutions were achieved.  
> - 📝 **Smart Summaries:** Generate concise executive overviews when you just need the highlights.  
> 
> You can split conversations by topic into separate clean files to keep projects organized, or bundle everything into a single archive directly on your **local drive**, **Google Drive**, **Notion**, or wherever you store your files (OneDrive, external drives, cloud backups, etc.).


---

## ⚡ 10-Second Quickstart

### 1. One-Click Install & Universal Sync (Recommended)
Clones and automatically registers the `/convermem` slash command into all your AI assistants (Antigravity, Claude Code, Cursor, OpenCode):

**Windows (PowerShell):**
```powershell
git clone https://github.com/davidoceanstream/convermem.git
cd convermem
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
```

**macOS / Linux:**
```bash
git clone https://github.com/davidoceanstream/convermem.git
cd convermem
bash scripts/install.sh
```

*(Or manual installation via standard pip: `pip install -e .`)*

### 2. Run in Terminal (CLI)
```bash
# Export all chats about a specific topic into clean Markdown
convermem export --topic "authentication" --out "./my_notes"

# Export conversations from the last 7 days
convermem export --days 7 --out "./weekly_logs"

# Scan all AI sessions discovered on your computer
convermem scan
```

### 3. Run in AI Chat (Slash Command)
Type directly inside your assistant chat:
```text
/convermem --topic "database architecture" --out "./docs/db_chat"
```
Or simply ask in natural language:
> *"Export our conversation about Stripe payments to ./docs/billing"*

---

## 🌟 Core Superpowers

### 🔌 1. Universal Multi-Platform Adapters (Open-Ended)
ConverMem automatically discovers and traverses conversation logs across all your AI assistants:

| Platform / Assistant | What It Reads |
| :--- | :--- |
| **Antigravity** | `~/.gemini/antigravity/brain/` (`transcript_full.jsonl`) |
| **Claude Code** | `~/.claude/projects/` (`<session-id>.jsonl`) |
| **Codex CLI (OpenAI)** | `~/.codex/sessions/` / Rollout logs |
| **Cursor** | `AppData/Roaming/Cursor/User/globalStorage/` |
| **VS Code (Cline / Roo / Copilot)** | `AppData/Roaming/Code/User/globalStorage/` |
| **OpenCode** | `~/.local/share/opencode/` |
| **... and more (etc.)** | Easily extensible adapter architecture for future AI tools |

### 🛡️ 2. DavidAgentCrew Privacy Shield
Never worry about leaking secrets to public GitHub repos. ConverMem automatically scans and sanitizes:
- **API Keys:** OpenAI, Anthropic, GitHub, AWS, Stripe
- **Auth Tokens:** Bearer tokens, session cookies, passwords
- **PII:** Phone numbers (international & local) and personal email addresses
- *Secrets are masked to `[REDACTED_API_KEY]`, keeping your team and code 100% safe.*

### 🧹 3. Zero-Noise Dialogue Cleaner
AI agent transcripts are packed with noisy raw system wrappers (`<ADDITIONAL_METADATA>`, `<SYSTEM_MESSAGE>`, `<USER_SETTINGS_CHANGE>`, raw tool execution logs, and JSON schema payloads). ConverMem strips away this internal clutter, extracting only the pristine, human-readable dialogue between you and the AI while keeping code blocks and technical solutions 100% intact.

### 🚀 4. Multi-Destination Connectors
Go beyond saving flat files on your hard drive:
- 🐙 **GitHub:** Auto-commit & push to repositories or generate GitHub Wiki pages.
- 📓 **Notion:** Synchronize formatted documents into Notion Databases and team workspaces.
- ☁️ **Google Drive & Docs:** Auto-upload via Google Service Account or Google Drive for Desktop.
- 🧠 **NotebookLM:** Send transcripts to generate Audio Overview podcasts, mind maps, and flashcards.
- 🎨 **Canva:** Extract key takeaways into presentation slides and visual infographics.

---

## 📖 CLI Reference Cheat Sheet

| Option | Flag | Description | Default |
| :--- | :--- | :--- | :--- |
| **Topic** | `--topic <text>` | Comma-separated keywords to filter dialogue | `None` (All) |
| **Days** | `--days <N>` | Include turns from the past N days | `None` |
| **Last Sessions** | `--last <N>` | Limit scan to the N most recent sessions | `None` |
| **Output Path** | `--out <path>` | Target folder for exported Markdown | `./convermem_export` |
| **Raw Mode** | `--no-redact` | Disable Privacy Shield (use with caution) | `False` (Redacted) |

---

<details>
<summary><b>💡 Deep Dive: Why Lossless Verbatim Recording Beats Lossy Summaries</b></summary>
<br>

### The Airplane Black Box Analogy

Imagine pair-programming with an expert colleague for weeks, but every morning they get amnesia. 

Existing solutions like `claude-mem` act like **sticky post-it notes**: they jot down a short, lossy summary (*"Likes dark mode, uses PostgreSQL"*). But if you ever want to revisit:
- *Why did we choose Architecture A over B?*
- *What was the exact prompt formulation that fixed the bug?*
- *What were the verbatim pros and cons we debated last Tuesday?*

The sticky note can't help you. The actual words were thrown away.

**ConverMem is the airplane flight data recorder (black box stenographer):**
1. **Zero Loss:** Every word you and the AI exchanged is preserved verbatim.
2. **Cross-Session Traversal:** Connects past sessions across weeks into one chronological narrative.
3. **Noise-Free Formatting:** Strips out ugly JSON system tags and raw terminal logs, leaving only human-readable discussion.
4. **Structured Chapters:** Automatically splits massive conversations into chapters of 50 turns with an interactive `README.md` navigation table.

</details>

---

## 📄 License
MIT © 2026 ConverMem Contributors. Built with precision for developers and creators worldwide.

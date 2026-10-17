# Technical Design Specification: ConverMem (Cross-Conversation Scribe & AI History Engine)

- **Project:** ConverMem — Zero-Loss AI Chat History & Cross-Conversation Scribe
- **Date:** 2026-10-17
- **Target Repository:** Standalone Open-Source Git Repository (`convermem/`) + Antigravity Plugin (`.agents/skills/convermem/`)
- **Status:** Approved by User / Ready for Implementation Planning

---

## 1. Problem Statement & Executive Summary

When developers and creators collaborate with AI coding assistants across multiple sessions, knowledge fragments rapidly. Every time a new session starts, the AI loses raw historical context. Existing solutions like `claude-mem` only maintain lossy, high-level summary notes in system prompts; they cannot reconstruct exact verbatim discussions, rationale, specific prompt formulations, or chronological decision paths.

**ConverMem** is a zero-loss, cross-conversation history extraction and documentation engine. It acts as a verbatim "flight recorder" (stenographer) that traverses historical and active AI session transcripts, filters relevant turns by topic, timeline, or scope, removes internal tool and JSON noise, strictly redacts private secrets and PII via an integrated Privacy Shield, and outputs pristine, human-readable Markdown logs with table-of-contents navigation.

---

## 2. Core Constraints & Guarantees

1. **Strict Privacy & Zero Secret Leakage:**
   - Integrated **DavidAgentCrew Security Shield** (Blue Team secret scanner).
   - Scans and redacts API keys (OpenAI, Anthropic, Gemini, AWS, Stripe, etc.), Bearer tokens, passwords, cookies, and PII (Thai & international phone numbers, personal emails, physical addresses).
   - Interactive prompt warns users upon detecting secrets and offers Auto-Redact (default), Exclude Turns, or Explicit Raw Save.
2. **Generic Open-Source Documentation:**
   - The open-source `README.md` and code comments must be written in **English**.
   - All documentation examples, quickstarts, and test suites must use **neutral, fictional scenarios** (e.g. building an e-commerce shopping cart, payment integration, coffee shop bot), with **zero mention or leakage of private project names, customer data, or internal business credentials**.
3. **Multi-lingual Natural Language Support:**
   - The engine is language-agnostic and seamlessly extracts and preserves multi-lingual dialogues (Thai, English, multilingual technical banter).
4. **Interactive Clarification:**
   - When invoked with vague prompts (e.g. "save my chats"), the agent asks interactive clarifying questions before writing files.

---

## 3. Architecture & Repository Layout

```text
convermem/
├── .gitignore
├── LICENSE                          # MIT License
├── README.md                        # Global English Open-Source Guide (Beginner-Friendly)
├── pyproject.toml                   # Standard Python packaging (pip install -e .)
│
├── convermem/                       # Core Python Engine
│   ├── __init__.py
│   ├── cli.py                       # Terminal Entrypoint (`convermem export`, `convermem scan`)
│   ├── reader.py                    # Universal transcript reader (Antigravity/Claude logs)
│   ├── filter.py                    # Tri-mode filtering (Topic, Timeline, Current/Cross)
│   ├── privacy.py                   # DavidAgentCrew Redaction & PII Scanner
│   ├── formatter.py                 # Noise-free Markdown builder (strips XML, formats turns)
│   └── exporter.py                  # Multi-chapter writer & README index generator
│
├── tests/                           # Comprehensive Test Suite
│   ├── test_reader.py               # Session traversal tests
│   ├── test_filter.py               # Keyword & date range tests
│   ├── test_privacy.py              # Secret & PII auto-redaction validation (Zero-Leakage)
│   └── test_formatter.py            # Clean markdown structure tests
│
└── .agents/skills/convermem/        # Antigravity Plugin & Slash Command
    ├── SKILL.md                     # Slash command `/convermem` & natural language driver
    └── prompt_template.md           # Clarification modal & dialog templates
```

---

## 4. Subsystem Specifications

### 4.1 Universal Reader & Multi-Platform Adapters (`reader.py`)
- Discovers conversation directories by inspecting known runtime root paths across multiple AI tools:
  - **Antigravity:** `~/.gemini/antigravity/brain/` (`transcript_full.jsonl`, `transcript.jsonl`)
  - **Claude Code:** `~/.claude/projects/` (`<session-id>.jsonl`)
  - **VS Code (Cline / Roo Code / Copilot):** `AppData/Roaming/Code/User/globalStorage/` (`api_conversation_history.json`, `ui_messages.json`)
  - **OpenCode:** `~/.local/share/opencode/` or `~/.opencode/`
  - **Codex CLI:** `~/.codex/sessions/` or `~/.openai/`
  - **Cursor:** `AppData/Roaming/Cursor/User/globalStorage/` (`state.vscdb`)
- Normalizes all sessions into a standard internal event format: `[Speaker, Content, Timestamp, Platform]`.
- Stitches dialogues from multiple AI platforms into a single unified chronological timeline.

### 4.2 Tri-Mode Filter Engine (`filter.py`)
Supports 3 operational modes combinable via flags or natural language:
1. **Mode 1: Topic / Semantic Keyword (`--topic <keywords>`):** Case-insensitive multi-keyword filtering against user prompts and assistant explanations.
2. **Mode 2: Timeline & Count (`--days <N>`, `--last <N>`):** Filters conversations within the last $N$ days or $N$ most recent sessions.
3. **Mode 3: Session Scope (`--current`, `--cross`):** Restricts extraction to the current active session or spans all past workspace sessions.

### 4.3 Privacy & Secret Shield (`privacy.py`)
- Powered by DavidAgentCrew Blue Team playbooks:
  - Regex patterns for API keys (`sk-[a-zA-Z0-9_-]{20,}`, `ghp_[a-zA-Z0-9]{36}`, `AKIA[0-9A-Z]{16}`, `Bearer [a-zA-Z0-9._-]+`).
  - Regex patterns for PII (Thai phone regex `0[689]\d{8}`, international phone `\+?[1-9]\d{1,14}`, email addresses).
- Masks secrets to `[REDACTED_API_KEY]`, `[REDACTED_PHONE_NUMBER]`, etc.
- Emits detection metrics to trigger the interactive decision modal.

### 4.4 Noise-Free Formatter & Timeline Weaving (`formatter.py`)
- Strips internal orchestration tags: `<USER_REQUEST>`, `<ADDITIONAL_METADATA>`, `<USER_SETTINGS_CHANGE>`, `<SYSTEM_MESSAGE>`.
- Distinguishes between internal tool execution outputs (`tool_calls`, command stdout) and verbatim conversational messages.
- **Side Question & `/btw` Timeline Weaving:** AI coding assistants often support modal side questions or `/btw` sub-threads (asked by users to avoid interrupting the main flow). ConverMem discovers these side questions and weaves them chronologically into the main transcript at their exact timestamp, preserving full contextual nuance without disjointed threads.
- Formats every dialog turn cleanly:
  ```markdown
  ### 💬 Turn {index}
  **⏱️ Timestamp:** `{ISO_TIME}` | **🔗 Session ID:** `{SESSION_ID}`

  #### 👤 User:
  > {Clean verbatim user speech}

  #### 🤖 AI Assistant:
  {Clean verbatim assistant speech}
  ```

### 4.5 Exporter & Output Connectors (`exporter.py`)
- **Connector 1 (Multi-Format Document Generation):**
  - Pristine Markdown (`.md`) with multi-chapter splitting and `README.md` navigation table.
  - Microsoft Word document (`.docx`) formatting for executive handoffs and offline viewing.
- **Connector 2 (Cloud Storage & Collaborative Sync):**
  - **Google Drive / Google Docs:** Direct synchronization via Google Cloud Service Account or Google Drive desktop sync.
  - **Notion Workspace & Databases:** Automated sync creating formatted Notion pages (with callout blocks, code toggles, and metadata properties) or appending to a central engineering knowledge base database.
  - **GitHub / Git:** Automatic commit and push to user-specified Git repositories, creating GitHub Wiki pages or Issue discussions.
- **Connector 3 (Knowledge-to-Media Pipeline):**
  - **NotebookLM Integration:** Automated generation of study guides, Audio Overviews (podcasts), mind maps, and flashcards.
  - **Canva / Visual Summary:** Exporting key takeaways to slide deck templates and social infographics.

---

## 5. User Interface & Natural Language UX

### 5.1 Slash Command `/convermem`
Available directly in the chat UI:
```bash
/convermem --topic "payment gateway" --out "./docs/chat_logs"
/convermem --last 3 --out "./logs"
/convermem --current --out "./session_notes"
```

### 5.2 Natural Language Handling & Interactive Clarification Loop
When a user provides free-form instructions (e.g. *"save what we discussed about database design"*):
1. **Intent Extractor:** Extracts target topic (`database design`), target directory (default `./convermem` if omitted), and scope.
2. **Clarification Trigger:** If the target directory or scope is ambiguous, renders an interactive question modal:
   - Option A: Current session only (Recommended)
   - Option B: Cross-conversation search across all past sessions
   - Option C: Last 7 days
3. **Secret Warning Trigger:** If secrets are detected, asks user whether to auto-redact before file generation.

---

## 6. Open-Source Documentation & Showcase Strategy

- **Repository Readme:** Complete English guide with beginner analogies (Flight Data Recorder vs Post-it note).
- **Comparison Section:** Contrast with `claude-mem` (Lossless verbatim file export vs lossy short-term system prompt summary).
- **Safe Demos:** All screenshots, code samples, and CLI walkthroughs use a generic sample repository (e.g. `ecommerce-demo`).

---

## 7. Verification & Testing Strategy

1. **Unit Tests (`tests/test_privacy.py`):** Verify 100% redaction of API keys, Bearer tokens, phone numbers, and addresses.
2. **Unit Tests (`tests/test_formatter.py`):** Verify clean removal of `<USER_REQUEST>` and intermediate tool stdout.
3. **Unit Tests (`tests/test_filter.py`):** Verify accurate topic matching, `--last`, and `--days` filtering.
4. **Integration Test (`tests/test_e2e.py`):** Run full export cycle against sample transcripts into a temporary directory and verify output Markdown files.

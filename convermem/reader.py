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

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

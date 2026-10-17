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

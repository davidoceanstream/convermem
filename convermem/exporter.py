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

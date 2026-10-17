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

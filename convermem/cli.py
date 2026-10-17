# D:\AI-Tools\convermem\convermem\cli.py
import click
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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

#!/usr/bin/env bash
# convermem: Universal All-in-One Installer & Skills Synchronizer for Unix/macOS
set -euo pipefail

echo "==============================================================="
echo " 🧠 convermem: Universal All-in-One Installer & Sync Engine"
echo "==============================================================="

# 1. Check Python
echo -e "\n[1/4] Checking Python runtime..."
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not found. Please install Python 3.10+ to continue."
    exit 1
fi
python3 --version

# 2. Install Python package locally
echo -e "\n[2/4] Installing convermem Python package..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$REPO_ROOT"
pip install -e . --quiet
echo "  -> convermem CLI installed successfully!"

# 3. Synchronize Skills to AI Agent paths
echo -e "\n[3/4] Registering /convermem Slash Command across AI Agents..."
SKILL_SOURCE="$REPO_ROOT/.agents/skills/convermem/SKILL.md"

TARGET_DIRS=(
    "$HOME/.gemini/config/skills"
    "$HOME/.claude/skills"
    "$HOME/.cursor/skills"
    "$HOME/.agents/skills"
)

for target in "${TARGET_DIRS[@]}"; do
    parent_dir="$(dirname "$target")"
    if [ -d "$parent_dir" ] || [ "$target" = "$HOME/.gemini/config/skills" ]; then
        mkdir -p "$target/convermem"
        cp "$SKILL_SOURCE" "$target/convermem/SKILL.md"
        echo "  [★] Registered Slash Command in: $target/convermem"
    fi
done

# 4. Clean Cache
echo -e "\n[4/4] Cleaning temporary cache files..."
find "$REPO_ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$REPO_ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
echo "  -> Cache cleaned!"

echo -e "\n==============================================================="
echo " ✨ convermem is completely installed and ready to use!"
echo " Next Steps:"
echo " 1. Run 'convermem --help' in your terminal."
echo " 2. Type '/convermem' in your AI chat to preserve verbatim context!"
echo "==============================================================="

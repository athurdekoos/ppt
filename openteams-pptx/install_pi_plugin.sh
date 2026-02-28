#!/usr/bin/env bash
# install_pi_plugin.sh — Install the openteams-pptx skill for pi coding agent
set -euo pipefail

SKILL_NAME="openteams-pptx"
TARGET_DIR="${HOME}/.pi/agent/skills/${SKILL_NAME}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " OpenTeams PPTX Skill — Pi Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# --- Prerequisite checks ---

if ! command -v python3 &>/dev/null; then
    echo "⚠  WARNING: python3 not found in PATH."
    echo "   The skill requires Python 3 with the python-pptx package."
    echo "   Install Python 3 first, then re-run this installer."
    echo ""
    echo "   On Ubuntu/Debian:  sudo apt install python3 python3-pip"
    echo "   On macOS:          brew install python3"
    echo ""
    exit 1
fi

if ! python3 -c "import pptx" 2>/dev/null; then
    echo "⚠  WARNING: python-pptx package not found."
    echo "   Install it with:  pip3 install python-pptx"
    echo ""
    read -rp "   Continue anyway? [y/N] " yn
    case "$yn" in
        [Yy]*) echo "   Continuing..." ;;
        *) exit 1 ;;
    esac
fi

if [ ! -d "${HOME}/.pi/agent/skills" ]; then
    echo "⚠  WARNING: ~/.pi/agent/skills/ directory not found."
    echo "   Is pi installed? Creating directory anyway..."
    mkdir -p "${HOME}/.pi/agent/skills"
fi

# --- Backup existing install ---

if [ -d "$TARGET_DIR" ]; then
    BACKUP="${TARGET_DIR}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "◆ Existing install found. Backing up to:"
    echo "  ${BACKUP}"
    mv "$TARGET_DIR" "$BACKUP"
    echo ""
fi

# --- Install ---

echo "◆ Installing ${SKILL_NAME} to:"
echo "  ${TARGET_DIR}"
echo ""

mkdir -p "$TARGET_DIR"

# Copy skill files (exclude dev/test artifacts)
for item in SKILL.md README.md scripts references assets docs; do
    if [ -e "${SCRIPT_DIR}/${item}" ]; then
        cp -r "${SCRIPT_DIR}/${item}" "${TARGET_DIR}/${item}"
    fi
done

echo "✓ Skill installed successfully!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  Usage:  /skill:openteams-pptx in any pi session"
echo ""
echo "  To uninstall:  rm -rf ${TARGET_DIR}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

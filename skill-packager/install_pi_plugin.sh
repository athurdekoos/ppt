#!/usr/bin/env bash

# Authored by Amelia Thurdekoos
# Email: ameliathurdekoos@gmail.com
#
# Any cares, concerns, compliments, or enhancements are always welcome!

# install_pi_plugin.sh — Install the skill-packager skill for pi
set -euo pipefail

SKILL_NAME="skill-packager"
TARGET_DIR="${HOME}/.pi/agent/skills/skill-packager"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo " ${SKILL_NAME} — pi Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# --- Prerequisite checks ---

if ! command -v python3 &>/dev/null; then
    echo "⚠  WARNING: python3 not found in PATH."
    echo "   Install Python 3 first, then re-run this installer."
    echo ""
    exit 1
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
echo "  Usage:  /skill:skill-packager in any pi session"
echo ""
echo "  To uninstall:  rm -rf ${TARGET_DIR}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

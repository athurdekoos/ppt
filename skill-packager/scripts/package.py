#!/usr/bin/env python3
"""
Package an existing skill directory for distribution.

Detects assets, resolves symlinks, rewrites absolute paths,
and generates installer scripts.

Usage:
  python3 package.py --skill-dir ./my-skill [--name my-skill]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import textwrap
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Asset detection
# ---------------------------------------------------------------------------

# Patterns that look like file references in source code
ASSET_PATTERNS = [
    re.compile(r"""["']([^"']*?(?:assets|logos|images|fonts)[/\\][^"']+)["']"""),
    re.compile(r"""["']([^"']+\.(?:png|jpg|jpeg|svg|gif|webp|ttf|otf|woff2?))["']"""),
]

# Patterns for absolute home directory paths
ABS_PATH_RE = re.compile(r"(/home/[^/]+/|/Users/[^/]+/)")

# Python interpreter in venv
VENV_PYTHON_RE = re.compile(
    r"(/home/[^/]+/\.venvs?/[^/]+/bin/python[23]?"
    r"|/Users/[^/]+/\.venvs?/[^/]+/bin/python[23]?"
    r"|/home/[^/]+/[^/]*/venv/bin/python[23]?"
    r"|/Users/[^/]+/[^/]*/venv/bin/python[23]?)"
)

SCANNABLE_EXTENSIONS = {".py", ".json", ".md", ".sh", ".yaml", ".yml", ".toml"}


def detect_assets(skill_dir: str) -> set[str]:
    """Scan skill files for referenced asset paths."""
    assets = set()
    for root, _dirs, files in os.walk(skill_dir):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SCANNABLE_EXTENSIONS:
                continue
            fpath = os.path.join(root, fname)
            try:
                content = open(fpath, encoding="utf-8", errors="ignore").read()
            except (OSError, UnicodeDecodeError):
                continue
            for pattern in ASSET_PATTERNS:
                for match in pattern.findall(content):
                    # Resolve relative to skill dir
                    candidate = os.path.normpath(os.path.join(skill_dir, match))
                    if os.path.exists(candidate):
                        assets.add(match)
    return assets


# ---------------------------------------------------------------------------
# Symlink resolution
# ---------------------------------------------------------------------------

def resolve_symlinks(skill_dir: str, referenced_assets: set[str]) -> list[dict]:
    """Find and resolve symlinks in the skill directory."""
    actions = []
    for root, dirs, files in os.walk(skill_dir, followlinks=False):
        for entry in dirs + files:
            full_path = os.path.join(root, entry)
            if not os.path.islink(full_path):
                continue

            rel_path = os.path.relpath(full_path, skill_dir)
            target = os.path.realpath(full_path)

            if os.path.isdir(target):
                # Find which files under this symlinked dir are actually referenced
                used_files = []
                for asset in referenced_assets:
                    if asset.startswith(rel_path + "/") or asset.startswith(rel_path + os.sep):
                        src = os.path.join(os.path.dirname(full_path),
                                           os.readlink(full_path),
                                           asset[len(rel_path) + 1:])
                        src = os.path.normpath(src)
                        if os.path.isfile(src):
                            used_files.append((asset, src))

                actions.append({
                    "type": "dir_symlink",
                    "link": full_path,
                    "rel": rel_path,
                    "target": target,
                    "used_files": used_files,
                })
            else:
                actions.append({
                    "type": "file_symlink",
                    "link": full_path,
                    "rel": rel_path,
                    "target": target,
                })
    return actions


def apply_symlink_fixes(skill_dir: str, actions: list[dict]) -> list[str]:
    """Replace symlinks with real files. Returns list of changes made."""
    changes = []
    for action in actions:
        if action["type"] == "file_symlink":
            link = action["link"]
            target = action["target"]
            os.remove(link)
            shutil.copy2(target, link)
            changes.append(f"Resolved file symlink: {action['rel']}")

        elif action["type"] == "dir_symlink":
            link = action["link"]
            used = action["used_files"]
            # Remove the symlink
            os.remove(link)
            # Create real directory
            os.makedirs(link, exist_ok=True)

            if used:
                for rel_asset, src_file in used:
                    dest = os.path.join(skill_dir, rel_asset)
                    os.makedirs(os.path.dirname(dest), exist_ok=True)
                    shutil.copy2(src_file, dest)
                    changes.append(f"Bundled: {rel_asset}")
            else:
                changes.append(f"Resolved empty dir symlink: {action['rel']}")

    return changes


# ---------------------------------------------------------------------------
# Absolute path rewriting
# ---------------------------------------------------------------------------

def find_absolute_paths(skill_dir: str) -> list[dict]:
    """Find files containing absolute paths."""
    hits = []
    for root, _dirs, files in os.walk(skill_dir):
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SCANNABLE_EXTENSIONS:
                continue
            fpath = os.path.join(root, fname)
            try:
                content = open(fpath, encoding="utf-8", errors="ignore").read()
            except (OSError, UnicodeDecodeError):
                continue
            if ABS_PATH_RE.search(content):
                hits.append({
                    "file": fpath,
                    "rel": os.path.relpath(fpath, skill_dir),
                })
    return hits


def rewrite_absolute_paths(skill_dir: str, hits: list[dict]) -> list[str]:
    """Rewrite absolute paths to portable alternatives."""
    changes = []
    for hit in hits:
        fpath = hit["file"]
        content = open(fpath, encoding="utf-8").read()
        original = content

        # Replace venv python paths with python3
        content = VENV_PYTHON_RE.sub("python3", content)

        # Replace remaining absolute home paths — flag but don't auto-rewrite
        # (too risky without knowing the intent)
        remaining = ABS_PATH_RE.findall(content)

        if content != original:
            with open(fpath, "w") as f:
                f.write(content)
            changes.append(f"Rewrote paths in: {hit['rel']}")

        if remaining:
            changes.append(
                f"⚠  Manual review needed: {hit['rel']} still has absolute paths: "
                + ", ".join(set(remaining))
            )

    return changes


# ---------------------------------------------------------------------------
# Installer generation
# ---------------------------------------------------------------------------

def generate_installers(skill_dir: str, skill_name: str) -> list[str]:
    """Generate install_pi_plugin.sh and install_claude_plugin.sh."""
    changes = []

    pi_script = _installer_script(
        skill_name=skill_name,
        agent_name="pi",
        target_dir_expr='${HOME}/.pi/agent/skills/' + skill_name,
        post_install_msg=f"  Usage:  /skill:{skill_name} in any pi session",
    )
    _write(os.path.join(skill_dir, "install_pi_plugin.sh"), pi_script)
    os.chmod(os.path.join(skill_dir, "install_pi_plugin.sh"), 0o755)
    changes.append("Generated: install_pi_plugin.sh")

    claude_script = _installer_script(
        skill_name=skill_name,
        agent_name="Claude Code",
        target_dir_expr='${HOME}/.agents/skills/' + skill_name,
        post_install_msg=(
            "  The skill is now available to Claude Code via\n"
            "  the ~/.agents/skills/ directory."
        ),
    )
    _write(os.path.join(skill_dir, "install_claude_plugin.sh"), claude_script)
    os.chmod(os.path.join(skill_dir, "install_claude_plugin.sh"), 0o755)
    changes.append("Generated: install_claude_plugin.sh")

    return changes


def _installer_script(skill_name: str, agent_name: str,
                      target_dir_expr: str, post_install_msg: str) -> str:
    return textwrap.dedent(f"""\
        #!/usr/bin/env bash
        # install_{"pi_plugin" if agent_name == "pi" else "claude_plugin"}.sh — Install the {skill_name} skill for {agent_name}
        set -euo pipefail

        SKILL_NAME="{skill_name}"
        TARGET_DIR="{target_dir_expr}"
        SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo " ${{SKILL_NAME}} — {agent_name} Installer"
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
            BACKUP="${{TARGET_DIR}}.backup.$(date +%Y%m%d_%H%M%S)"
            echo "◆ Existing install found. Backing up to:"
            echo "  ${{BACKUP}}"
            mv "$TARGET_DIR" "$BACKUP"
            echo ""
        fi

        # --- Install ---

        echo "◆ Installing ${{SKILL_NAME}} to:"
        echo "  ${{TARGET_DIR}}"
        echo ""

        mkdir -p "$TARGET_DIR"

        # Copy skill files (exclude dev/test artifacts)
        for item in SKILL.md README.md scripts references assets docs; do
            if [ -e "${{SCRIPT_DIR}}/${{item}}" ]; then
                cp -r "${{SCRIPT_DIR}}/${{item}}" "${{TARGET_DIR}}/${{item}}"
            fi
        done

        echo "✓ Skill installed successfully!"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo ""
        echo "{post_install_msg}"
        echo ""
        echo "  To uninstall:  rm -rf ${{TARGET_DIR}}"
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    """)


# ---------------------------------------------------------------------------
# README update
# ---------------------------------------------------------------------------

def update_readme_install(skill_dir: str, skill_name: str) -> list[str]:
    """Add or update install section in README.md."""
    readme_path = os.path.join(skill_dir, "README.md")
    if not os.path.exists(readme_path):
        return ["⚠  No README.md found — skipping install section update"]

    content = open(readme_path, encoding="utf-8").read()

    install_section = textwrap.dedent(f"""\
        ## Installation

        ### For pi (coding agent)

        ```bash
        ./install_pi_plugin.sh
        ```

        The skill becomes available as `/skill:{skill_name}` in any pi session.

        ### For Claude Code

        ```bash
        ./install_claude_plugin.sh
        ```

        The skill is installed to `~/.agents/skills/{skill_name}/`.
    """)

    # Check if install section already exists
    if "## Installation" in content:
        # Replace existing section (up to next ## heading)
        pattern = re.compile(
            r"## Installation\n.*?(?=\n## |\Z)", re.DOTALL
        )
        new_content = pattern.sub(install_section.rstrip(), content)
        if new_content != content:
            with open(readme_path, "w") as f:
                f.write(new_content)
            return [f"Updated install section in README.md for '{skill_name}'"]
        return ["Install section already up-to-date"]
    else:
        # Insert after first heading
        lines = content.split("\n")
        insert_at = 1  # After first line
        for i, line in enumerate(lines):
            if i > 0 and line.startswith("## "):
                insert_at = i
                break
        lines.insert(insert_at, "\n" + install_section)
        with open(readme_path, "w") as f:
            f.write("\n".join(lines))
        return [f"Added install section to README.md for '{skill_name}'"]


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def package(skill_dir: str, name_override: Optional[str] = None) -> None:
    """Package a skill directory for distribution."""
    skill_dir = os.path.abspath(skill_dir)

    if not os.path.isdir(skill_dir):
        print(f"❌ Not a directory: {skill_dir}")
        sys.exit(1)

    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        print(f"❌ No SKILL.md found in {skill_dir}")
        sys.exit(1)

    # Detect skill name
    skill_name = name_override
    if not skill_name:
        with open(skill_md) as f:
            for line in f:
                if line.startswith("name:"):
                    skill_name = line.split(":", 1)[1].strip()
                    break
    if not skill_name:
        skill_name = os.path.basename(skill_dir)

    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f" Packaging skill: {skill_name}")
    print(f" Directory: {skill_dir}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()

    all_changes = []

    # Step 1: Detect referenced assets
    print("◆ Scanning for asset references...")
    assets = detect_assets(skill_dir)
    if assets:
        print(f"  Found {len(assets)} asset reference(s)")
    else:
        print("  No asset references found")

    # Step 2: Resolve symlinks
    print("◆ Checking for symlinks...")
    symlink_actions = resolve_symlinks(skill_dir, assets)
    if symlink_actions:
        changes = apply_symlink_fixes(skill_dir, symlink_actions)
        all_changes.extend(changes)
        for c in changes:
            print(f"  {c}")
    else:
        print("  No symlinks found")

    # Step 3: Rewrite absolute paths
    print("◆ Scanning for absolute paths...")
    abs_hits = find_absolute_paths(skill_dir)
    if abs_hits:
        changes = rewrite_absolute_paths(skill_dir, abs_hits)
        all_changes.extend(changes)
        for c in changes:
            print(f"  {c}")
    else:
        print("  No absolute paths found")

    # Step 4: Generate installers
    print("◆ Generating installer scripts...")
    changes = generate_installers(skill_dir, skill_name)
    all_changes.extend(changes)
    for c in changes:
        print(f"  {c}")

    # Step 5: Update README
    print("◆ Updating README.md...")
    changes = update_readme_install(skill_dir, skill_name)
    all_changes.extend(changes)
    for c in changes:
        print(f"  {c}")

    # Summary
    print()
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f" ✓ Packaging complete: {len(all_changes)} change(s)")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    for c in all_changes:
        print(f"  • {c}")
    print()
    print(f"  Test the installers:")
    print(f"    cd {skill_dir} && bash install_pi_plugin.sh")
    print(f"    cd {skill_dir} && bash install_claude_plugin.sh")


def _write(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Package a skill for distribution")
    parser.add_argument("--skill-dir", required=True, help="Path to skill directory")
    parser.add_argument("--name", help="Override skill name (default: from SKILL.md)")

    args = parser.parse_args()
    package(args.skill_dir, args.name)


if __name__ == "__main__":
    main()

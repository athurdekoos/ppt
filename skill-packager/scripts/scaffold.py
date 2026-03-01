#!/usr/bin/env python3

# Authored by Amelia Thurdekoos
# Email: ameliathurdekoos@gmail.com
#
# Any cares, concerns, compliments, or enhancements are always welcome!

"""
Scaffold a new agent skill directory with standard structure.

Usage:
  python3 scaffold.py --name my-skill --description "Does cool things" --out ./my-skill
"""
from __future__ import annotations

import argparse
import os
import sys
import textwrap


def scaffold(name: str, description: str, out_dir: str) -> None:
    """Create a new skill directory with standard files."""
    if os.path.exists(out_dir) and os.listdir(out_dir):
        print(f"⚠  Directory already exists and is not empty: {out_dir}")
        print("   Use --force to overwrite, or choose a different directory.")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)

    # Create subdirectories
    for subdir in ["scripts", "references", "assets"]:
        os.makedirs(os.path.join(out_dir, subdir), exist_ok=True)

    # SKILL.md
    skill_md = textwrap.dedent(f"""\
        ---
        name: {name}
        description: >
          {description}
        ---

        # {name.replace('-', ' ').title()}

        All paths below are relative to this skill's directory (the folder containing this SKILL.md).

        ## Overview

        [Describe what this skill does and when it activates.]

        ## How It Works

        [Describe the workflow — what happens when the skill is triggered.]

        ## Usage

        ```bash
        python3 <skill-dir>/scripts/main.py [arguments]
        ```
    """)
    _write(os.path.join(out_dir, "SKILL.md"), skill_md)

    # README.md
    readme = textwrap.dedent(f"""\
        # {name.replace('-', ' ').title()}

        {description}

        ## Installation

        ### For pi (coding agent)

        ```bash
        ./install_pi_plugin.sh
        ```

        The skill becomes available as `/skill:{name}` in any pi session.

        ### For Claude Code

        ```bash
        ./install_claude_plugin.sh
        ```

        ### Prerequisites

        - **Python 3.11+**

        ## Usage

        [Describe how to use the skill.]

        ## Directory Structure

        ```
        {name}/
        ├── SKILL.md          # Skill definition
        ├── README.md         # This file
        ├── scripts/          # Skill scripts
        ├── references/       # Config and reference files
        └── assets/           # Bundled assets
        ```

        ## Troubleshooting

        | Problem | Solution |
        |---------|----------|
        | `python3: command not found` | Install Python 3 |
        | Permission denied | `chmod +x install_pi_plugin.sh` |
    """)
    _write(os.path.join(out_dir, "README.md"), readme)

    print(f"✓ Scaffolded skill '{name}' at {out_dir}")
    print(f"")
    print(f"  Files created:")
    print(f"    {out_dir}/SKILL.md")
    print(f"    {out_dir}/README.md")
    print(f"    {out_dir}/scripts/")
    print(f"    {out_dir}/references/")
    print(f"    {out_dir}/assets/")
    print(f"")
    print(f"  Next: Add your scripts and run the packager to generate installers:")
    print(f"    python3 <packager>/scripts/package.py --skill-dir {out_dir}")


def _write(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new agent skill")
    parser.add_argument("--name", required=True, help="Skill name (kebab-case)")
    parser.add_argument("--description", required=True, help="One-line description")
    parser.add_argument("--out", help="Output directory (default: ./<name>)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing directory")

    args = parser.parse_args()
    out_dir = args.out or f"./{args.name}"

    if args.force and os.path.exists(out_dir):
        import shutil
        shutil.rmtree(out_dir)

    scaffold(args.name, args.description, out_dir)


if __name__ == "__main__":
    main()

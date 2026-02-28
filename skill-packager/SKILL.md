---
name: skill-packager
description: >
  Scaffold new agent skills and package existing ones for distribution.
  Use when the user wants to create a new skill from scratch, package an existing
  skill directory for installation, generate installer scripts, or make a skill
  self-contained and portable. Trigger phrases: "scaffold a skill", "package this skill",
  "create installers", "make this skill portable", "new skill template".
---

# Skill Packager

Scaffold new agent skills or package existing ones with installers for pi and Claude Code.

All paths below are relative to this skill's directory (the folder containing this SKILL.md).

## Commands

### scaffold

Create a new skill directory with the standard structure.

**Usage:** Ask Claude to scaffold a new skill, providing:
- **Skill name** — kebab-case identifier (e.g., `my-cool-skill`)
- **Description** — one-line description for trigger matching
- **Output directory** — where to create it (defaults to `./<skill-name>/`)

**What it creates:**
```
<skill-name>/
├── SKILL.md          # Skill definition with name and description
├── README.md         # Usage docs with install instructions
├── scripts/          # Empty scripts directory
├── references/       # Empty references directory
└── assets/           # Empty assets directory
```

Run the scaffolder:
```bash
python3 <skill-dir>/scripts/scaffold.py \
  --name <skill-name> \
  --description "One-line description" \
  --out <output-directory>
```

### package

Make an existing skill directory self-contained and generate installer scripts.

**Usage:** Ask Claude to package a skill directory, providing:
- **Skill directory** — path to the skill to package
- **Skill name** — (optional) override the name from SKILL.md

**What it does:**
1. Parses SKILL.md and all `.py`, `.sh`, `.json`, `.md` files for asset references
2. Detects symlinks and resolves them to real files
3. Detects absolute paths (`/home/`, `/Users/`) and rewrites to relative
4. Bundles referenced assets into the skill directory
5. Generates `install_pi_plugin.sh` and `install_claude_plugin.sh`
6. Updates README.md with install instructions for the skill name

Run the packager:
```bash
python3 <skill-dir>/scripts/package.py \
  --skill-dir <path-to-skill> \
  [--name <override-name>]
```

Where `<skill-dir>` is the directory containing this SKILL.md (the packager skill itself).

## How the Packager Works

### Asset Detection (ASSET-05)

The packager scans these file types for asset references:
- `.py` files — string literals matching common asset patterns (`assets/`, `logos/`, `.png`, `.jpg`, `.svg`)
- `.json` files — values containing file path patterns
- `.md` files — markdown links and code blocks with file paths
- `.sh` files — file paths in variables and arguments

### Symlink Resolution

For each symlink found in the skill directory:
1. Resolve the symlink target
2. If target is a directory, identify which files are actually referenced
3. Copy only referenced files into the skill directory
4. Remove the symlink, replace with real directory

### Path Rewriting

For each absolute path found:
1. If it's a Python interpreter path (e.g., `/home/user/.venvs/x/bin/python`) → replace with `python3`
2. If it's a file reference within the skill → rewrite to relative path
3. If it's an external reference → flag for manual review

## Tips

- Run `scaffold` first when creating a new skill from scratch
- Run `package` on an existing skill before distributing it
- The packager is idempotent — safe to run multiple times
- Always review the generated installers before distributing

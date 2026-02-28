# Skill Packager

Scaffold new agent skills and package existing ones for distribution with pi and Claude Code installers.

## Installation

### For pi (coding agent)

```bash
./install_pi_plugin.sh
```

The skill becomes available as `/skill:skill-packager` in any pi session.

### For Claude Code

```bash
./install_claude_plugin.sh
```

The skill is installed to `~/.agents/skills/skill-packager/`.
## Usage

### Scaffold a New Skill

```bash
python3 scripts/scaffold.py --name my-skill --description "Does amazing things" --out ./my-skill
```

Creates a standard skill directory with SKILL.md, README.md, and subdirectories.

### Package an Existing Skill

```bash
python3 scripts/package.py --skill-dir ./my-skill
```

This will:
1. Scan for referenced assets in code and config files
2. Resolve any symlinks to real files
3. Rewrite absolute paths (venv Python paths → `python3`)
4. Generate `install_pi_plugin.sh` and `install_claude_plugin.sh`
5. Update README.md with install instructions

## Directory Structure

```
skill-packager/
├── SKILL.md          # Skill definition
├── README.md         # This file
└── scripts/
    ├── scaffold.py   # Create new skill directories
    └── package.py    # Package existing skills for distribution
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `python3: command not found` | Install Python 3 |
| Permission denied | `chmod +x install_pi_plugin.sh` |
| "No SKILL.md found" | Run from the skill directory, or pass `--skill-dir` |
| Absolute paths remain after packaging | Check the ⚠ warnings — some paths may need manual review |

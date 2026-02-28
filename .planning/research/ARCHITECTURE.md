# Architecture Patterns

**Domain:** Agent skill packaging & distribution
**Researched:** 2026-02-28

## Recommended Architecture

### Component 1: Self-Contained Skill Directory

```
openteams-pptx/
├── SKILL.md                    # Skill definition (pi format)
├── README.md                   # User-facing docs with install instructions
├── assets/
│   └── logos/                  # 6 PNG files (no symlink)
│       ├── colored_horizontal.png
│       ├── colored_vertical.png
│       ├── white_horizontal.png
│       ├── black_horizontal.png
│       ├── favicon_colored.png
│       └── favicon_white.png
├── references/
│   ├── brand.json              # Paths updated to assets/logos/
│   └── slide_types.md
├── scripts/
│   ├── generate_deck.py
│   ├── brand_engine.py
│   ├── slide_builder.py
│   ├── slide_renderers.py
│   ├── pptx_helpers.py
│   └── refresh_site_style.py
└── tests/
    ├── test_core.py
    └── test_ai_readiness.json
```

### Component 2: Installer Scripts (repo root)

```
install_pi_plugin.sh            # Copies skill → ~/.pi/agent/skills/openteams-pptx/
install_claude_plugin.sh        # Copies skill files + creates Claude Code command
```

### Component 3: Skill Packager (Part 2, separate skill)

```
~/.pi/agent/skills/skill-packager/
├── SKILL.md                    # Skill definition
├── scripts/
│   ├── scaffold.sh             # Create new skill directory structure
│   ├── bundle_assets.py        # Detect and copy referenced assets
│   ├── rewrite_paths.py        # Convert paths to relative
│   └── generate_installers.sh  # Generate install_pi/claude scripts
└── templates/
    ├── SKILL.md.template       # Skeleton SKILL.md
    ├── README.md.template      # README with install section
    ├── install_pi.sh.template  # Pi installer template
    └── install_claude.sh.template # Claude Code installer template
```

## Data Flow

### Install Flow (Pi)
```
User runs ./install_pi_plugin.sh
  → Checks prerequisites (python3, pip)
  → Copies openteams-pptx/ → ~/.pi/agent/skills/openteams-pptx/
  → Pi auto-discovers SKILL.md on next session
  → User types /skill:openteams-pptx
```

### Install Flow (Claude Code)
```
User runs ./install_claude_plugin.sh
  → Checks prerequisites (python3, pip)
  → Copies skill files → ~/.local/share/openteams-pptx/
  → Creates ~/.claude/commands/openteams-pptx.md (frontmatter + instructions pointing to files)
  → User types /openteams-pptx in Claude Code
```

### Packager Flow (Part 2)
```
User invokes /skill:skill-packager with a skill directory path
  → Scans SKILL.md + scripts for asset references
  → Copies referenced assets into skill directory
  → Rewrites paths to relative
  → Generates install_pi_plugin.sh and install_claude_plugin.sh
  → Updates README with install section
```

## Patterns to Follow

### Pattern: Script-relative paths
All paths in brand.json and scripts should use `os.path.dirname(__file__)` or `<skill-dir>` to resolve relative to the skill directory, not the caller's cwd.

### Pattern: Flat logo directory
Instead of mirroring the deep Assets/ tree, put all 6 PNGs in `assets/logos/` with descriptive names. Simpler paths, no nested directories.

## Anti-Patterns to Avoid

### Anti-Pattern: Symlinks in distributed skills
Symlinks break when copied to another machine. Always bundle actual files.

### Anti-Pattern: Hardcoded absolute paths
`/home/mia/.venvs/pptx/bin/python` breaks on other machines. Use `python3` and document venv as prerequisite.

## Sources

- Observed pi skill structure at `~/.pi/agent/skills/` and `~/.agents/skills/`
- Claude Code command pattern from `~/.claude/commands/gsd/`

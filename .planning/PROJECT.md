# OpenTeams PPTX Skill — Installer & Packaging

## What This Is

A packaging project that makes the OpenTeams PPTX Generator skill installable via one-click shell scripts for both pi coding agent and Claude Code. The skill generates brand-compliant OpenTeams PowerPoint presentations from natural language. Target audience is OpenTeams team members.

## Core Value

Anyone at OpenTeams can run a single shell script and immediately have the `/skill:openteams-pptx` command available in their agent — no manual copying, no path fixups, no symlink wrangling.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] `install_pi_plugin.sh` — one-click installer that copies the skill to `~/.pi/agent/skills/openteams-pptx/`
- [ ] `install_claude_plugin.sh` — one-click installer that installs the skill for Claude Code
- [ ] Self-contained skill directory — 6 PNG logo files bundled directly (no symlink to `../../Assets`)
- [ ] `brand.json` logo paths updated to reference bundled PNGs
- [ ] README.md updated with install instructions for both agents
- [ ] Documentation files updated to reflect the installable packaging
- [ ] Installers handle Python dependency check/warning (but don't create venvs)
- [ ] Installers are idempotent (safe to re-run)

### Out of Scope

- Python venv creation — users manage their own Python environment
- Auto-updating / version checking after install
- Windows / PowerShell installer — Linux/macOS `.sh` only
- Bundling the full Assets directory (AI, SVG, JPG variants) — only the 6 PNGs the code uses
- Publishing to a package registry

## Context

- The skill currently lives at `openteams-pptx/` in this repo and is manually copied to `~/.pi/agent/skills/openteams-pptx/`
- Logo assets are accessed via a symlink `assets/logos -> ../../Assets` which breaks outside this repo
- Pi discovers skills in `~/.pi/agent/skills/` and `~/.agents/skills/` (directories with `SKILL.md`)
- Claude Code uses `~/.claude/commands/` for custom slash commands, or can be configured to read skills directories via settings
- The skill depends on `python-pptx`, `Pillow`, `requests`, `beautifulsoup4`, `lxml` (listed in `requirements.txt`)
- The 6 required PNG logos are: colored horizontal, colored vertical, white horizontal, black horizontal, favicon colored, favicon white

## Constraints

- **Logo files**: Must include only the 6 PNGs referenced in `brand.json` — not the full Assets tree
- **No Python setup**: Installer should warn if Python/pip aren't available but not try to manage venvs
- **Shell compatibility**: Must work on bash (Linux + macOS)
- **Paths in SKILL.md**: Must use `<skill-dir>` pattern so the skill works from its installed location

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Bundle 6 PNGs instead of symlink | Makes skill self-contained, works anywhere | — Pending |
| Two separate installer scripts | Pi and Claude Code have different skill directories/conventions | — Pending |
| Don't manage Python venvs | Users have varying Python setups; installer stays simple | — Pending |

---
*Last updated: 2026-02-28 after initialization*

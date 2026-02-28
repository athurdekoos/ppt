# OpenTeams PPTX Skill — Installer & Skill Factory

## What This Is

Two-part project: (1) Package the OpenTeams PPTX Generator skill as one-click installable for pi coding agent and Claude Code, targeted at OpenTeams team members. (2) Build a reusable local skill ("skill-packager") that can scaffold new skills from scratch and package any skill directory into self-contained installable form — so this process can be repeated for future skills.

## Core Value

A repeatable, one-command workflow for building and distributing agent skills — starting with the OpenTeams PPTX skill as the first proof case.

## Requirements

### Validated

(None yet — ship to validate)

### Active

**Part 1 — OpenTeams PPTX Skill Packaging:**
- [ ] Self-contained skill directory — 6 PNG logo files bundled directly (no symlink to `../../Assets`)
- [ ] `brand.json` logo paths updated to reference bundled PNGs
- [ ] `install_pi_plugin.sh` — one-click installer that copies the skill to `~/.pi/agent/skills/openteams-pptx/`
- [ ] `install_claude_plugin.sh` — one-click installer that installs the skill for Claude Code
- [ ] Installers handle Python dependency check/warning (but don't create venvs)
- [ ] Installers are idempotent (safe to re-run)
- [ ] README.md updated with install instructions for both agents
- [ ] Documentation files updated to reflect the installable packaging

**Part 2 — Reusable Skill Packager:**
- [ ] Local skill (`/skill:skill-packager`) that can scaffold a new pi/Claude Code skill from scratch
- [ ] Skill packager can take any existing skill directory and generate install scripts
- [ ] Bundles referenced assets (images, data files) into self-contained directory
- [ ] Rewrites paths (symlinks, absolute refs) to be portable
- [ ] Generates `install_pi_plugin.sh` and `install_claude_plugin.sh` for any skill
- [ ] Updates/generates README with install instructions

### Out of Scope

- Python venv creation — users manage their own Python environment
- Auto-updating / version checking after install
- Windows / PowerShell installer — Linux/macOS `.sh` only
- Bundling the full Assets directory (AI, SVG, JPG variants) — only the 6 PNGs the code uses
- Publishing to a package registry
- Skill packager as a hosted/cloud service — local only

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
| Build reusable skill-packager as a pi skill | Dogfood the process — use agent skills to build agent skills | — Pending |
| Part 1 first, then Part 2 | Prove the pattern with PPTX skill before generalizing | — Pending |

---
*Last updated: 2026-02-28 after initialization*

# OpenTeams PPTX Skill — npx Installer

## What This Is

Replace the shell-script installers (`install_pi_plugin.sh`, `install_claude_plugin.sh`) with a single `npx`-based installer for the OpenTeams PPTX Generator skill. Users run one command to install the skill for either pi or Claude Code — no cloning, no manual file copying.

## Core Value

One `npx` command installs the skill for any supported agent — zero manual steps.

## Requirements

### Validated

- ✓ Self-contained skill directory — 6 PNG logos bundled, no symlinks — Phase 1 v1.0
- ✓ brand.json logo paths reference bundled PNGs — Phase 1 v1.0
- ✓ All hardcoded absolute paths removed — Phase 1 v1.0
- ✓ Scripts use python3 and relative paths — Phase 1 v1.0
- ✓ README.md with install instructions — Phase 3 v1.0
- ✓ SKILL.md with portable paths — Phase 3 v1.0
- ✓ Troubleshooting section in README — Phase 3 v1.0

### Active

- [ ] `npx https://github.com/athurdekoos/ppt --pi` installs the skill for pi
- [ ] `npx https://github.com/athurdekoos/ppt --claude` installs the skill for Claude Code
- [ ] npx installer checks for Python 3, installs python-pptx if missing
- [ ] npx installer backs up existing install before overwriting
- [ ] npx installer is idempotent (safe to re-run)
- [ ] Old `.sh` installer scripts deleted from repo
- [ ] README updated to show npx commands instead of .sh scripts
- [ ] package.json with bin entry pointing to CLI script
- [ ] CLI script handles --pi and --claude flags with clear error for no/invalid flag

### Out of Scope

- Publishing to npm registry — install directly from GitHub URL
- Windows/PowerShell support — Linux/macOS only
- Auto-update mechanism
- Skill packager (deferred — separate future milestone)

## Context

- The repo is at `github.com/athurdekoos/ppt`
- npx can run packages directly from GitHub URLs: `npx https://github.com/user/repo`
- This requires a `package.json` with a `bin` field at the repo root
- The bin script runs via Node.js, handles file copying + Python prereq checks
- pi discovers skills in `~/.pi/agent/skills/` (directories with `SKILL.md`)
- Claude Code discovers skills in `~/.agents/skills/` (directories with `SKILL.md`)
- The skill depends on Python 3 + python-pptx at runtime

## Constraints

- **Node.js only for installer** — the CLI script must use Node.js (no bash shelling out for core logic) since npx runs Node
- **No npm publish** — must work via GitHub URL
- **Python prereqs** — installer should check and attempt `pip3 install python-pptx` if missing

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| npx from GitHub URL, not npm registry | Simpler distribution, no npm account needed | — Pending |
| Single CLI with --pi/--claude flags | One entry point, clear UX | — Pending |
| Delete .sh scripts entirely | Clean break, no confusion about which method to use | — Pending |
| Node.js CLI script | Required by npx; can shell out to check Python | — Pending |

---
*Last updated: 2026-02-28 after milestone v2.0 initialization*

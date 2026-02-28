# Requirements: OpenTeams PPTX Skill — Installer & Skill Factory

**Defined:** 2026-02-28
**Core Value:** A repeatable, one-command workflow for building and distributing agent skills

## v1 Requirements

### Asset Bundling

- [ ] **ASSET-01**: Skill directory contains 6 PNG logo files directly (no symlink)
- [ ] **ASSET-02**: brand.json logo_assets paths reference bundled PNGs in assets/logos/
- [ ] **ASSET-03**: All hardcoded absolute paths removed from scripts and SKILL.md (no `/home/mia/` references)
- [ ] **ASSET-04**: Scripts use `python3` and relative paths, not hardcoded venv paths
- [ ] **ASSET-05**: Auto-detect referenced assets by parsing code and config files

### Installers

- [ ] **INST-01**: `install_pi_plugin.sh` copies skill to `~/.pi/agent/skills/openteams-pptx/` and skill is discoverable as `/skill:openteams-pptx`
- [ ] **INST-02**: `install_claude_plugin.sh` installs skill for Claude Code with proper command file format
- [ ] **INST-03**: Installers are idempotent — safe to re-run without breaking existing install
- [ ] **INST-04**: Installers check for Python 3 and pip, print clear warnings if missing
- [ ] **INST-05**: Installers back up existing install before overwriting
- [ ] **INST-06**: Uninstall guidance printed after successful install (how to remove)

### Documentation

- [ ] **DOCS-01**: README.md includes install instructions for both pi and Claude Code
- [ ] **DOCS-02**: SKILL.md updated with portable paths (no absolute references)
- [ ] **DOCS-03**: CLAUDE.md updated to reflect new installable structure
- [ ] **DOCS-04**: README includes troubleshooting section for common issues

### Skill Packager

- [ ] **PACK-01**: `/skill:skill-packager` can scaffold a new skill directory with SKILL.md, README, and directory structure
- [ ] **PACK-02**: Skill packager can generate `install_pi_plugin.sh` and `install_claude_plugin.sh` for any skill directory
- [ ] **PACK-03**: Skill packager bundles referenced assets into self-contained directory
- [ ] **PACK-04**: Skill packager auto-detects assets by parsing SKILL.md and script files for file references
- [ ] **PACK-05**: Skill packager rewrites absolute and symlink paths to portable relative paths
- [ ] **PACK-06**: Skill packager generates/updates README install section with correct skill name and paths

## v2 Requirements

### Distribution

- **DIST-01**: Version tracking for installed skills
- **DIST-02**: Update-in-place command to pull latest version

### Cross-Platform

- **XPLAT-01**: PowerShell installer for Windows
- **XPLAT-02**: Fish/zsh shell compatibility testing

## Out of Scope

| Feature | Reason |
|---------|--------|
| Python venv management | Too many edge cases across systems; users manage their own |
| Package registry publishing | Over-engineering for internal OpenTeams audience |
| Auto-update mechanism | Security concerns, complexity — manual re-run is fine |
| Cloud/hosted skill packager | Local-only tool, no server needed |
| Windows .bat/.ps1 installer | Linux/macOS only for v1 |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| ASSET-01 | Phase 1 | Pending |
| ASSET-02 | Phase 1 | Pending |
| ASSET-03 | Phase 1 | Pending |
| ASSET-04 | Phase 1 | Pending |
| ASSET-05 | Phase 4 | Pending |
| INST-01 | Phase 2 | Pending |
| INST-02 | Phase 2 | Pending |
| INST-03 | Phase 2 | Pending |
| INST-04 | Phase 2 | Pending |
| INST-05 | Phase 2 | Pending |
| INST-06 | Phase 2 | Pending |
| DOCS-01 | Phase 3 | Pending |
| DOCS-02 | Phase 3 | Pending |
| DOCS-03 | Phase 3 | Pending |
| DOCS-04 | Phase 3 | Pending |
| PACK-01 | Phase 4 | Pending |
| PACK-02 | Phase 4 | Pending |
| PACK-03 | Phase 4 | Pending |
| PACK-04 | Phase 4 | Pending |
| PACK-05 | Phase 4 | Pending |
| PACK-06 | Phase 4 | Pending |

**Coverage:**
- v1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0 ✓

---
*Requirements defined: 2026-02-28*
*Last updated: 2026-02-28 after initial definition*

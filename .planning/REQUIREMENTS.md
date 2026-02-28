# Requirements: OpenTeams PPTX Skill — npx Installer

**Defined:** 2026-02-28
**Core Value:** One npx command installs the skill for any supported agent

## v1 Requirements

### NPX CLI

- [ ] **CLI-01**: `npx https://github.com/athurdekoos/ppt --pi` installs skill to `~/.pi/agent/skills/openteams-pptx/`
- [ ] **CLI-02**: `npx https://github.com/athurdekoos/ppt --claude` installs skill to `~/.agents/skills/openteams-pptx/`
- [ ] **CLI-03**: Running with no flag or invalid flag prints usage help with both commands
- [ ] **CLI-04**: CLI prints clear progress messages (checking prereqs → backing up → copying → done)

### Prerequisites

- [ ] **PREREQ-01**: Installer checks for Python 3 and exits with clear message if missing
- [ ] **PREREQ-02**: Installer checks for python-pptx and runs `pip3 install python-pptx` if missing
- [ ] **PREREQ-03**: If pip install fails, print manual install instructions and continue

### Install Behavior

- [ ] **INST-01**: Existing install is backed up to `<target>.backup.<timestamp>` before overwriting
- [ ] **INST-02**: Installer is idempotent — safe to re-run without errors
- [ ] **INST-03**: Only skill files are copied (SKILL.md, README.md, scripts/, references/, assets/, docs/) — no tests, no .planning, no .git
- [ ] **INST-04**: Prints uninstall instructions after successful install

### Cleanup

- [ ] **CLEAN-01**: `install_pi_plugin.sh` deleted from repo
- [ ] **CLEAN-02**: `install_claude_plugin.sh` deleted from repo
- [ ] **CLEAN-03**: All references to .sh installers removed from README, SKILL.md, CLAUDE.md

### Package Setup

- [ ] **PKG-01**: `package.json` at repo root with `bin` field pointing to CLI entry script
- [ ] **PKG-02**: CLI entry script is a Node.js file with `#!/usr/bin/env node` shebang
- [ ] **PKG-03**: No external npm dependencies — uses only Node.js built-ins (fs, path, child_process)

### Documentation

- [ ] **DOCS-01**: README updated with npx install commands replacing .sh instructions
- [ ] **DOCS-02**: README Installation section shows both --pi and --claude examples
- [ ] **DOCS-03**: CLAUDE.md updated to reference npx install method

## v2 Requirements

### Distribution

- **DIST-01**: Publish to npm for shorter command: `npx @openteams/pptx --pi`
- **DIST-02**: Version tracking for installed skills

## Out of Scope

| Feature | Reason |
|---------|--------|
| npm registry publishing | GitHub URL is sufficient for now |
| Windows/PowerShell | Linux/macOS only for v1 |
| Auto-update mechanism | Manual re-run of npx is fine |
| Skill packager | Separate future milestone |
| Python venv management | Users manage their own environments |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| CLI-01 | Phase 1 | Pending |
| CLI-02 | Phase 1 | Pending |
| CLI-03 | Phase 1 | Pending |
| CLI-04 | Phase 1 | Pending |
| PREREQ-01 | Phase 1 | Pending |
| PREREQ-02 | Phase 1 | Pending |
| PREREQ-03 | Phase 1 | Pending |
| INST-01 | Phase 1 | Pending |
| INST-02 | Phase 1 | Pending |
| INST-03 | Phase 1 | Pending |
| INST-04 | Phase 1 | Pending |
| PKG-01 | Phase 1 | Pending |
| PKG-02 | Phase 1 | Pending |
| PKG-03 | Phase 1 | Pending |
| CLEAN-01 | Phase 2 | Pending |
| CLEAN-02 | Phase 2 | Pending |
| CLEAN-03 | Phase 2 | Pending |
| DOCS-01 | Phase 2 | Pending |
| DOCS-02 | Phase 2 | Pending |
| DOCS-03 | Phase 2 | Pending |

**Coverage:**
- v1 requirements: 20 total
- Mapped to phases: 20
- Unmapped: 0 ✓

---
*Requirements defined: 2026-02-28*
*Last updated: 2026-02-28 after v2.0 initialization*

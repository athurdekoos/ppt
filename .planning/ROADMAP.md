# Roadmap: OpenTeams PPTX Skill — npx Installer

## Overview

Replace shell-script installers with a single npx-based CLI. Two phases: build the npx installer, then clean up old scripts and update docs.

## Phases

- [ ] **Phase 1: npx CLI Installer** — package.json + Node.js CLI that installs the skill for pi or Claude Code
- [ ] **Phase 2: Cleanup & Documentation** — Delete .sh scripts, update all docs to reference npx

## Phase Details

### Phase 1: npx CLI Installer
**Goal**: `npx https://github.com/athurdekoos/ppt --pi` and `--claude` work end-to-end
**Depends on**: Nothing
**Requirements**: CLI-01, CLI-02, CLI-03, CLI-04, PREREQ-01, PREREQ-02, PREREQ-03, INST-01, INST-02, INST-03, INST-04, PKG-01, PKG-02, PKG-03
**Success Criteria** (what must be TRUE):
  1. `npx https://github.com/athurdekoos/ppt --pi` installs skill to `~/.pi/agent/skills/openteams-pptx/` with all required files
  2. `npx https://github.com/athurdekoos/ppt --claude` installs skill to `~/.agents/skills/openteams-pptx/`
  3. Running without flags prints usage help
  4. Missing Python 3 produces a clear error message
  5. Missing python-pptx triggers automatic pip install attempt
  6. Re-running backs up existing install and succeeds without errors
**Plans:** TBD

### Phase 2: Cleanup & Documentation
**Goal**: Old .sh installers removed, all documentation points to npx method
**Depends on**: Phase 1
**Requirements**: CLEAN-01, CLEAN-02, CLEAN-03, DOCS-01, DOCS-02, DOCS-03
**Success Criteria** (what must be TRUE):
  1. `install_pi_plugin.sh` and `install_claude_plugin.sh` no longer exist in repo
  2. README Installation section shows npx commands only
  3. No remaining references to .sh installers in README, SKILL.md, or CLAUDE.md
  4. CLAUDE.md references npx install method
**Plans:** TBD

## Progress

| Phase | Plans Complete | Status |
|-------|----------------|--------|
| 1. npx CLI Installer | 0/0 | Not Started |
| 2. Cleanup & Documentation | 0/0 | Not Started |

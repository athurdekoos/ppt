# Roadmap: OpenTeams PPTX Skill — Installer & Skill Factory

## Overview

Package the OpenTeams PPTX skill as a self-contained, one-click installable for pi and Claude Code, then generalize the process into a reusable skill-packager. Four phases: make it portable, make it installable, document it, then build the factory.

## Phases

- [x] **Phase 1: Self-Contained Skill** - Bundle logo PNGs, rewrite paths, eliminate symlinks and hardcoded references
- [x] **Phase 2: Installer Scripts** - Create install_pi_plugin.sh and install_claude_plugin.sh with prereq checks
- [x] **Phase 3: Documentation** - Update README, SKILL.md, and CLAUDE.md with install instructions and troubleshooting
- [ ] **Phase 4: Skill Packager** - Build reusable /skill:skill-packager for scaffolding and packaging any skill

## Phase Details

### Phase 1: Self-Contained Skill
**Goal**: The openteams-pptx skill directory works when copied anywhere — no symlinks, no absolute paths, all assets bundled
**Depends on**: Nothing (first phase)
**Requirements**: ASSET-01, ASSET-02, ASSET-03, ASSET-04
**Success Criteria** (what must be TRUE):
  1. `assets/logos/` contains 6 PNG files directly (not a symlink)
  2. `brand.json` logo_assets paths resolve correctly from the skill directory
  3. No file in the skill directory contains `/home/mia/` or other absolute paths
  4. `generate_deck.py --demo` produces a valid .pptx when run from the skill directory with `python3`
**Plans:** 1 plan
- [x] 01-01-PLAN.md — Bundle logos, fix paths, verify portability

### Phase 2: Installer Scripts
**Goal**: OpenTeams team members can run one shell script to install the skill for their agent
**Depends on**: Phase 1
**Requirements**: INST-01, INST-02, INST-03, INST-04, INST-05, INST-06
**Success Criteria** (what must be TRUE):
  1. Running `./install_pi_plugin.sh` makes `/skill:openteams-pptx` available in pi
  2. Running `./install_claude_plugin.sh` makes the skill available in Claude Code
  3. Re-running either installer on an existing install works without errors
  4. Running installer without Python 3 installed prints a clear warning
  5. Previous install is backed up before overwriting
**Plans:** 1 plan
- [x] 02-01-PLAN.md — Create pi and Claude Code installer scripts

### Phase 3: Documentation
**Goal**: A new user can install and use the skill by reading the README alone
**Depends on**: Phase 2
**Requirements**: DOCS-01, DOCS-02, DOCS-03, DOCS-04
**Success Criteria** (what must be TRUE):
  1. README has step-by-step install instructions for both pi and Claude Code
  2. SKILL.md contains no absolute paths or machine-specific references
  3. CLAUDE.md reflects the installable skill structure
  4. Troubleshooting section covers: missing Python, permission errors, fonts not found
**Plans:** 1 plan
- [x] 03-01-PLAN.md — Update README, SKILL.md, CLAUDE.md with install docs and troubleshooting

### Phase 4: Skill Packager
**Goal**: User can invoke `/skill:skill-packager` to scaffold a new skill or package an existing one with installers
**Depends on**: Phase 3
**Requirements**: PACK-01, PACK-02, PACK-03, PACK-04, PACK-05, PACK-06, ASSET-05
**Success Criteria** (what must be TRUE):
  1. `/skill:skill-packager scaffold` creates a valid skill directory with SKILL.md, README, and structure
  2. `/skill:skill-packager package <dir>` generates install_pi_plugin.sh and install_claude_plugin.sh
  3. Packager detects and bundles assets referenced in SKILL.md and scripts
  4. Packager rewrites absolute/symlink paths to portable relative paths
  5. Generated README includes correct install instructions for the skill name
**Plans**: TBD

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Self-Contained Skill | 1/1 | Complete | 2026-02-28 |
| 2. Installer Scripts | 1/1 | Complete | 2026-02-28 |
| 3. Documentation | 1/1 | Complete | 2026-02-28 |
| 4. Skill Packager | 0/? | Not started | - |

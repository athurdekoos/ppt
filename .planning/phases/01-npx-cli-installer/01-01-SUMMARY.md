---
phase: 01-npx-cli-installer
plan: 01
subsystem: cli
tags: [node, npx, installer, python-pptx]

requires: []
provides:
  - "npx-invocable CLI installer for openteams-pptx skill"
  - "package.json with bin entry at repo root"
  - "Automatic Python prereq checking and python-pptx install"
affects: []

tech-stack:
  added: []
  patterns: ["Node.js built-ins only — zero npm dependencies"]

key-files:
  created:
    - package.json
    - bin/install.mjs
  modified: []

key-decisions:
  - "Used fs.cpSync with filter callback to exclude __pycache__"
  - "Used ES modules (.mjs) for modern Node.js compatibility"

patterns-established:
  - "Progress output: ◆ action... ✓ result on same line"
  - "Backup naming: target.backup.ISO-timestamp"

requirements-completed: [CLI-01, CLI-02, CLI-03, CLI-04, PREREQ-01, PREREQ-02, PREREQ-03, INST-01, INST-02, INST-03, INST-04, PKG-01, PKG-02, PKG-03]

duration: 3min
completed: 2026-02-28
---

# Phase 1: npx CLI Installer Summary

**Zero-dependency Node.js CLI installer with Python prereq checks, backup, and filtered file copy for pi/Claude Code**

## Performance

- **Duration:** 3 min
- **Started:** 2026-02-28T03:57:30Z
- **Completed:** 2026-02-28T03:59:30Z
- **Tasks:** 3
- **Files modified:** 2

## Accomplishments
- Created package.json making the repo npx-executable via GitHub URL
- Built bin/install.mjs with full argument parsing, prereq checks, and file installation
- Verified --pi, --claude, no-flag, and both-flags behavior
- Ensured __pycache__, tests/, and .sh files are excluded from copy

## Task Commits

Each task was committed atomically:

1. **Task 1: Create package.json at repo root** - `53bb932` (feat)
2. **Task 2: Create bin/install.mjs CLI entry point** - `4cca2df` (feat)
3. **Task 3: Make CLI executable and test** - `588811e` (feat)

## Files Created/Modified
- `package.json` - npm config with bin field and files whitelist
- `bin/install.mjs` - CLI entry point with Python checks, backup, filtered copy

## Decisions Made
- Used `fs.cpSync` filter callback to exclude `__pycache__` directories during copy
- Used ES modules (`.mjs`) for modern Node.js compatibility and top-level import syntax

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical] Added __pycache__ filter to cpSync**
- **Found during:** Task 3 (testing)
- **Issue:** `cpSync` with `recursive: true` copied `__pycache__` from scripts/
- **Fix:** Added `filter` option to `cpSync` excluding paths containing `__pycache__`
- **Files modified:** bin/install.mjs
- **Verification:** Re-ran install, confirmed no `__pycache__` in target
- **Committed in:** 588811e

---

**Total deviations:** 1 auto-fixed (1 missing critical)
**Impact on plan:** Essential fix — plan explicitly required skipping __pycache__. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- CLI installer complete and tested for both targets
- Ready for Phase 2 (if any) or milestone completion

---
*Phase: 01-npx-cli-installer*
*Completed: 2026-02-28*

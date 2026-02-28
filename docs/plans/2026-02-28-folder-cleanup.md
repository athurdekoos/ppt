# Folder Cleanup & Path Integrity Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Fix all typos, misplaced files, stale artifacts, duplicate configs, broken references, and outdated documentation in the OpenTeams brand assets repo — then verify every path resolves correctly.

**Architecture:** Work bottom-up: fix the filesystem first (renames, moves, deletes), then update every JSON/Python/Markdown file that references old paths, then verify end-to-end.

**Tech Stack:** Bash (file ops), Python (path validation script), Git

---

### Task 1: Fix folder typo — `Black-Horizontal-tansparent` → `Black-Horizontal-transparent`

**Files:**
- Rename: `Assets/OT_Black_Logos/Black-Horizontal-tansparent/` → `Assets/OT_Black_Logos/Black-Horizontal-transparent/`

**Step 1: Rename the folder**

```bash
cd /home/mia/dev/ppt
git mv "Assets/OT_Black_Logos/Black-Horizontal-tansparent" "Assets/OT_Black_Logos/Black-Horizontal-transparent"
```

**Step 2: Verify**

```bash
ls "Assets/OT_Black_Logos/Black-Horizontal-transparent/"
```

Expected: `OpennTeams_logo_horizontal_lockup_black.png` (file still exists, old folder gone)

**Step 3: Commit**

```bash
git add -A
git commit -m "fix: rename Black-Horizontal-tansparent → Black-Horizontal-transparent"
```

---

### Task 2: Fix filename typo — `OpennTeams` → `OpenTeams` (6 files)

**Files:**
- Rename all 6 files under `Assets/OT_Black_Logos/` that contain `OpennTeams`

**Step 1: Rename all affected files**

```bash
cd /home/mia/dev/ppt
# AI files
git mv "Assets/OT_Black_Logos/Black-Horizontal-ai-file/OpennTeams_logo_horizontal_lockup_black.ai" \
       "Assets/OT_Black_Logos/Black-Horizontal-ai-file/OpenTeams_logo_horizontal_lockup_black.ai"
git mv "Assets/OT_Black_Logos/Black-Horizontal-ai-file/OpennTeams_logo_vertical_lockup_black.ai" \
       "Assets/OT_Black_Logos/Black-Horizontal-ai-file/OpenTeams_logo_vertical_lockup_black.ai"
# SVG
git mv "Assets/OT_Black_Logos/Black-Horizontal-svg-file/OpennTeams_logo_horizontal_lockup_black-01.svg" \
       "Assets/OT_Black_Logos/Black-Horizontal-svg-file/OpenTeams_logo_horizontal_lockup_black-01.svg"
# PNG (transparent — already renamed folder in Task 1)
git mv "Assets/OT_Black_Logos/Black-Horizontal-transparent/OpennTeams_logo_horizontal_lockup_black.png" \
       "Assets/OT_Black_Logos/Black-Horizontal-transparent/OpenTeams_logo_horizontal_lockup_black.png"
# White-background SVG
git mv "Assets/OT_Black_Logos/Black-Horizontal-white-background/OpennTeams_logo_vertical_lockup_black-01.svg" \
       "Assets/OT_Black_Logos/Black-Horizontal-white-background/OpenTeams_logo_vertical_lockup_black-01.svg"
# Vertical transparent PNG
git mv "Assets/OT_Black_Logos/Black-vertical-transparent/OpennTeams_logo_vertical_lockup_black.png" \
       "Assets/OT_Black_Logos/Black-vertical-transparent/OpenTeams_logo_vertical_lockup_black.png"
```

**Step 2: Verify no `OpennTeams` files remain**

```bash
find Assets/ -name '*OpennTeams*'
```

Expected: no output (all renamed)

**Step 3: Commit**

```bash
git add -A
git commit -m "fix: rename OpennTeams → OpenTeams in all black logo filenames"
```

---

### Task 3: Move misplaced files to correct folders

Three files are in the wrong location:

1. `Colored-Horizontal-transparent-logo/OT-new-logo-final-white-vertical-lockup.png` — a white vertical logo, belongs in `OT_White_Logos/`
2. `OT_Black_Logos/Black-Horizontal-white-background/OpenTeams_logo_vertical_lockup_black-01.svg` — a **vertical** logo in a **horizontal** folder
3. `Colored-Horizontal-transparent-logo/OT-new-logo3-final.png` — unclear draft, remove

**Files:**
- Move: `Assets/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo-final-white-vertical-lockup.png`
- Move: `Assets/OT_Black_Logos/Black-Horizontal-white-background/OpenTeams_logo_vertical_lockup_black-01.svg`
- Delete: `Assets/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo3-final.png`
- Delete: `Assets/OT_Colored_Logos/Colored-vertical-white-background/Copy of OT-new-logo-vertical-lockup.jpg`

**Step 1: Create missing folder and move the vertical black SVG**

```bash
cd /home/mia/dev/ppt
mkdir -p "Assets/OT_Black_Logos/Black-vertical-white-background"
git mv "Assets/OT_Black_Logos/Black-Horizontal-white-background/OpenTeams_logo_vertical_lockup_black-01.svg" \
       "Assets/OT_Black_Logos/Black-vertical-white-background/OpenTeams_logo_vertical_lockup_black-01.svg"
```

Note: after this move, `Black-Horizontal-white-background/` is empty. Remove it:

```bash
rmdir "Assets/OT_Black_Logos/Black-Horizontal-white-background"
```

**Step 2: Move the white vertical logo to the right color group**

```bash
mkdir -p "Assets/OT_White_Logos/White-vertical-transparent-logo"
git mv "Assets/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo-final-white-vertical-lockup.png" \
       "Assets/OT_White_Logos/White-vertical-transparent-logo/OT-new-logo-final-white-vertical-lockup.png"
```

**Step 3: Delete the junk/duplicate files**

```bash
git rm "Assets/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo3-final.png"
git rm "Assets/OT_Colored_Logos/Colored-vertical-white-background/Copy of OT-new-logo-vertical-lockup.jpg"
```

**Step 4: Verify folder structure**

```bash
find Assets/ -type f | sort
```

Expected: no `Copy of`, no `logo3`, no misplaced vertical-in-horizontal or white-in-colored.

**Step 5: Commit**

```bash
git add -A
git commit -m "fix: move misplaced logos to correct folders, remove duplicates/drafts"
```

---

### Task 4: Update `assets_index.json` — fix all stale paths

This file still references the old `Assests/` prefix (note: actual folder is `Assets/`), old `OpennTeams` filenames, old `tansparent` folder name, removed files, and misplaced file locations.

**Files:**
- Modify: `assets_index.json`

**Step 1: Rewrite `assets_index.json` with corrected paths**

Replace the entire file. Every path must match the filesystem after Tasks 1–3. Key changes:
- `Assests/` → `Assets/`
- `Black-Horizontal-tansparent/` → `Black-Horizontal-transparent/`
- `OpennTeams_` → `OpenTeams_`
- `logo_black_horizontal_svg` now points to `Black-vertical-white-background/` (it was always a vertical logo — fix the key name too)
- Remove `Copy of ...`, `logo3`, and misplaced white vertical from `all_logos` colored section
- Add new white vertical logo path
- Update `decisions` block

Write the full corrected JSON:

```json
{
  "logo_colored_horizontal_png": "Assets/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo-final.png",
  "logo_colored_horizontal_svg": "Assets/OT_Colored_Logos/Colored-Horizontal-svg-file/OT-new logo-final-01.svg",
  "logo_colored_vertical_png": "Assets/OT_Colored_Logos/Colored-vertical-transparent-logo/OT-new-logo-vertical-lockup.png",
  "logo_white_horizontal_png": "Assets/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-horizontal-lockup.png",
  "logo_white_horizontal_svg": "Assets/OT_White_Logos/White-Horizontal-svg-file/OT-new logo-final-white-horizontal-lockup-01.svg",
  "logo_white_vertical_png": "Assets/OT_White_Logos/White-vertical-transparent-logo/OT-new-logo-final-white-vertical-lockup.png",
  "logo_black_horizontal_png": "Assets/OT_Black_Logos/Black-Horizontal-transparent/OpenTeams_logo_horizontal_lockup_black.png",
  "logo_black_horizontal_svg": "Assets/OT_Black_Logos/Black-Horizontal-svg-file/OpenTeams_logo_horizontal_lockup_black-01.svg",
  "logo_black_vertical_png": "Assets/OT_Black_Logos/Black-vertical-transparent/OpenTeams_logo_vertical_lockup_black.png",
  "logo_black_vertical_svg": "Assets/OT_Black_Logos/Black-vertical-white-background/OpenTeams_logo_vertical_lockup_black-01.svg",
  "favicon_colored_png": "Assets/OT_Colored_Logos/Favicon-transparent-background/OpenTeams-favicon-01.png",
  "favicon_white_png": "Assets/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-favicon.png",
  "all_logos": [
    "Assets/Email signature OT logo/Email-signature-logo-with-tagline.png",
    "Assets/Email signature OT logo/Email-signature-logo-without-tagline.png",
    "Assets/OT_Black_Logos/Black-Horizontal-svg-file/OpenTeams_logo_horizontal_lockup_black-01.svg",
    "Assets/OT_Black_Logos/Black-Horizontal-transparent/OpenTeams_logo_horizontal_lockup_black.png",
    "Assets/OT_Black_Logos/Black-vertical-transparent/OpenTeams_logo_vertical_lockup_black.png",
    "Assets/OT_Black_Logos/Black-vertical-white-background/OpenTeams_logo_vertical_lockup_black-01.svg",
    "Assets/OT_Colored_Logos/Colored-Horizontal-svg-file/OT-new logo-final-01.svg",
    "Assets/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo-final.png",
    "Assets/OT_Colored_Logos/Colored-Horizontal-white-background/OT-new-logo-final.jpg",
    "Assets/OT_Colored_Logos/Colored-vertical-transparent-logo/OT-new-logo-vertical-lockup.png",
    "Assets/OT_Colored_Logos/Colored-vertical-white-background/OT-new logo-vertical-lockup-01.svg",
    "Assets/OT_Colored_Logos/Colored-vertical-white-background/OT-new-logo-vertical-lockup.jpg",
    "Assets/OT_Colored_Logos/Favicon-transparent-background/OpenTeams-favicon-01.png",
    "Assets/OT_Colored_Logos/Favicon-white-background/OpenTeams-favicon-01.svg",
    "Assets/OT_White_Logos/White-Favicon-svg-file/OT-new logo-final-white-favicon-01.svg",
    "Assets/OT_White_Logos/White-Horizontal-svg-file/OT-new logo-final-white-horizontal-lockup-01.svg",
    "Assets/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-favicon.png",
    "Assets/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-horizontal-lockup.png",
    "Assets/OT_White_Logos/White-vertical-svg-file/OT-new logo-final-white-vertical-lockup-01.svg",
    "Assets/OT_White_Logos/White-vertical-transparent-logo/OT-new-logo-final-white-vertical-lockup.png"
  ],
  "icons": [],
  "backgrounds": [],
  "photos": [],
  "decisions": [
    "BLACK_LOGO_H_PNG: Assets/OT_Black_Logos/Black-Horizontal-transparent/OpenTeams_logo_horizontal_lockup_black.png",
    "PRIMARY_LOGO_COLOR_H_SVG: Assets/OT_Colored_Logos/Colored-Horizontal-svg-file/OT-new logo-final-01.svg",
    "PRIMARY_LOGO_COLOR_H_PNG: Assets/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo-final.png",
    "PRIMARY_LOGO_COLOR_V_PNG: Assets/OT_Colored_Logos/Colored-vertical-transparent-logo/OT-new-logo-vertical-lockup.png",
    "FAVICON_COLOR_PNG: Assets/OT_Colored_Logos/Favicon-transparent-background/OpenTeams-favicon-01.png",
    "WHITE_LOGO_H_PNG: Assets/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-horizontal-lockup.png"
  ]
}
```

**Step 2: Verify every path in the JSON exists on disk**

```bash
cd /home/mia/dev/ppt
python3 -c "
import json, os, sys
with open('assets_index.json') as f:
    data = json.load(f)
ok = True
for key, val in data.items():
    if isinstance(val, str) and '/' in val:
        if not os.path.exists(val):
            print(f'MISSING: {key} → {val}')
            ok = False
    elif isinstance(val, list):
        for item in val:
            if isinstance(item, str) and '/' in item:
                path = item.split(': ', 1)[-1] if ': ' in item else item
                if not os.path.exists(path):
                    print(f'MISSING in {key}: {path}')
                    ok = False
if ok:
    print('All paths OK')
sys.exit(0 if ok else 1)
"
```

Expected: `All paths OK`

**Step 3: Commit**

```bash
git add assets_index.json
git commit -m "fix: update assets_index.json — correct all paths after renames"
```

---

### Task 5: Update `openteams-pptx/references/brand.json` — fix `logo_assets` paths

**Files:**
- Modify: `openteams-pptx/references/brand.json` (only the `logo_assets` block)

**Step 1: Update the `logo_assets` section**

Replace the `logo_assets` object in `brand.json` with corrected paths. These are relative to the skill directory (`openteams-pptx/`), which uses a symlink `assets/logos → /home/mia/dev/ppt/Assets`. The symlink target is correct (`Assets/`) but the paths within need fixing:

Old → New:
- `Black-Horizontal-tansparent/OpennTeams_logo_horizontal_lockup_black.png` → `Black-Horizontal-transparent/OpenTeams_logo_horizontal_lockup_black.png`

```json
  "logo_assets": {
    "colored_horizontal_png": "assets/logos/OT_Colored_Logos/Colored-Horizontal-transparent-logo/OT-new-logo-final.png",
    "colored_vertical_png":   "assets/logos/OT_Colored_Logos/Colored-vertical-transparent-logo/OT-new-logo-vertical-lockup.png",
    "white_horizontal_png":   "assets/logos/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-horizontal-lockup.png",
    "black_horizontal_png":   "assets/logos/OT_Black_Logos/Black-Horizontal-transparent/OpenTeams_logo_horizontal_lockup_black.png",
    "favicon_colored_png":    "assets/logos/OT_Colored_Logos/Favicon-transparent-background/OpenTeams-favicon-01.png",
    "favicon_white_png":      "assets/logos/OT_White_Logos/White-Horizontal-transparent-logo/OT-new-logo-final-white-favicon.png"
  }
```

**Step 2: Verify all brand.json logo paths resolve**

```bash
cd /home/mia/dev/ppt/openteams-pptx
python3 -c "
import json, os
with open('references/brand.json') as f:
    data = json.load(f)
ok = True
for key, rel in data.get('logo_assets', {}).items():
    if not os.path.exists(rel):
        print(f'MISSING: {key} → {rel}')
        ok = False
    else:
        print(f'  OK: {key} → {rel}')
if ok:
    print('All logo_assets paths OK')
else:
    print('FAILED — some paths missing')
"
```

Expected: all OK

**Step 3: Commit**

```bash
cd /home/mia/dev/ppt
git add openteams-pptx/references/brand.json
git commit -m "fix: update brand.json logo_assets paths after file renames"
```

---

### Task 6: Update `build_template.py` — fix `Assests` → `Assets` default path

**Files:**
- Modify: `build_template.py` (lines 9, 1512, 1518, 1519)

**Step 1: Fix all 4 occurrences of `Assests` in `build_template.py`**

```bash
cd /home/mia/dev/ppt
sed -i 's|./Assests|./Assets|g; s|default="./Assests"|default="./Assets"|g' build_template.py
```

**Step 2: Verify no `Assests` references remain**

```bash
grep -n "Assests" build_template.py
```

Expected: no output

**Step 3: Commit**

```bash
git add build_template.py
git commit -m "fix: correct Assests → Assets typo in build_template.py"
```

---

### Task 7: Fix symlink — absolute → relative

**Files:**
- Recreate: `openteams-pptx/assets/logos` symlink

**Step 1: Replace absolute symlink with relative**

```bash
cd /home/mia/dev/ppt
rm openteams-pptx/assets/logos
ln -s ../../Assets openteams-pptx/assets/logos
```

**Step 2: Verify symlink resolves**

```bash
ls openteams-pptx/assets/logos/OT_Colored_Logos/
```

Expected: lists the colored logo subdirectories

**Step 3: Commit**

```bash
git add openteams-pptx/assets/logos
git commit -m "fix: use relative symlink for assets/logos instead of absolute path"
```

---

### Task 8: Consolidate `requirements.txt` and clean up `__pycache__`

**Files:**
- Delete: `openteams-pptx/requirements.txt`
- Modify: `openteams-pptx/README.md` (update install reference if needed)
- Delete: `openteams-pptx/scripts/__pycache__/` (directory)
- Modify: `.gitignore` (add `__pycache__/` and `*.pyc`)

**Step 1: Update root `.gitignore`**

Add `__pycache__/` and `*.pyc` entries:

```
# macOS
.DS_Store

# Office temp/lock files
~$*

# Review slide images
review/slides/*.png

# Python bytecode
__pycache__/
*.pyc
```

**Step 2: Delete `__pycache__`**

```bash
rm -rf openteams-pptx/scripts/__pycache__
```

**Step 3: Remove duplicate `requirements.txt`**

```bash
cd /home/mia/dev/ppt
git rm openteams-pptx/requirements.txt
```

**Step 4: Check if `openteams-pptx/README.md` references its own `requirements.txt`**

```bash
grep -n "requirements" openteams-pptx/README.md
```

If it references `requirements.txt` locally, update the path to `../requirements.txt` or to `pip install -r requirements.txt` (root).

**Step 5: Commit**

```bash
git add -A
git commit -m "chore: consolidate requirements.txt, gitignore __pycache__, remove bytecode"
```

---

### Task 9: Update `CLAUDE.md` — fix outdated references

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Rewrite `CLAUDE.md` to reflect current folder structure**

The current `CLAUDE.md` references `2025 NEW LOGO/` (doesn't exist — it's `Assets/`), `OpenTeams_Template_2025.pptx` (no longer in repo — was removed in commit `3a3e227`), and says "no build commands" (there's now `build_template.py` and the skill scripts).

Update the file:

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is an OpenTeams brand assets and presentation tooling repository containing:

- **OpenTeams_Brand_Guidelines_2025.pdf** — Official brand guidelines document (36 MB)
- **Assets/** — Logo files in multiple formats and variants
- **build_template.py** — Legacy PowerPoint template builder script
- **openteams-pptx/** — Modular PPTX generation skill (scripts, brand config, references)
- **review/** — Brand compliance audit outputs (mock deck, report)

## Logo Organization

Logos are under `Assets/` organized by color variant and format:

- **OT_Colored_Logos/** — Full-color logos (horizontal, vertical, favicon; PNG/JPG/SVG)
- **OT_White_Logos/** — White logos for dark backgrounds (AI/SVG/PNG)
- **OT_Black_Logos/** — Black logos for light backgrounds (AI/SVG/PNG)
- **OT_ai_Logos/** — Adobe Illustrator source files
- **Email signature OT logo/** — Sized for email signatures (with/without tagline)
- **Horizontal-PDF-logo/** — PDF format horizontal logo

Each variant is available in horizontal and vertical lockups, plus favicon.

## Key Config Files

- **assets_index.json** — Machine-readable index of all logo asset paths
- **site_style.json** — Website style tokens scraped from openteams.com
- **openteams-pptx/references/brand.json** — Brand tokens for slide generation

## Git Commits

- **Never** include a `Co-Authored-By` line in commit messages. All commits should be authored solely by the user.

## Notes

- The `~$` prefixed file is a temporary Office lock file and should be ignored.
- `openteams-pptx/assets/logos` is a symlink to `../../Assets`.
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md to reflect current repo structure"
```

---

### Task 10: Drop stale git stash

**Step 1: Inspect the stash to confirm it's no longer needed**

```bash
git stash show stash@{0} --stat
```

Review the output — this is from the initial template builder commit and all that work is already committed.

**Step 2: Drop it**

```bash
git stash drop stash@{0}
```

**Step 3: Verify**

```bash
git stash list
```

Expected: empty (no stashes)

---

### Task 11: Full verification — validate every referenced path resolves

**Files:**
- Create: `verify_paths.py` (temporary validation script)

**Step 1: Write the verification script**

```python
#!/usr/bin/env python3
"""Verify all asset paths referenced across config files resolve to real files."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
errors = []

def check_path(label, path, base=ROOT):
    full = os.path.join(base, path)
    if not os.path.exists(full):
        errors.append(f"  MISSING [{label}]: {path}")
        return False
    return True

# 1. assets_index.json
print("=== assets_index.json ===")
with open(os.path.join(ROOT, "assets_index.json")) as f:
    idx = json.load(f)
for key, val in idx.items():
    if isinstance(val, str) and "/" in val:
        check_path(key, val)
    elif isinstance(val, list):
        for item in val:
            if isinstance(item, str) and "/" in item:
                path = item.split(": ", 1)[-1] if ": " in item else item
                check_path(f"{key}[]", path)

# 2. brand.json (paths relative to openteams-pptx/)
print("=== brand.json (logo_assets) ===")
skill_dir = os.path.join(ROOT, "openteams-pptx")
with open(os.path.join(skill_dir, "references", "brand.json")) as f:
    brand = json.load(f)
for key, rel in brand.get("logo_assets", {}).items():
    check_path(f"brand.{key}", rel, base=skill_dir)

# 3. Symlink check
print("=== Symlink ===")
sym = os.path.join(skill_dir, "assets", "logos")
if os.path.islink(sym):
    target = os.readlink(sym)
    resolved = os.path.realpath(sym)
    if os.path.isdir(resolved):
        print(f"  OK: {sym} → {target} (resolves to {resolved})")
    else:
        errors.append(f"  BROKEN SYMLINK: {sym} → {target}")
else:
    errors.append(f"  NOT A SYMLINK: {sym}")

# 4. Check for leftover typos on disk
print("=== Leftover typo scan ===")
for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "Assets")):
    for name in dirnames + filenames:
        if "OpennTeams" in name:
            errors.append(f"  TYPO FILE: {os.path.join(dirpath, name)}")
        if "Copy of" in name:
            errors.append(f"  DUPLICATE: {os.path.join(dirpath, name)}")
        if "logo3" in name:
            errors.append(f"  DRAFT FILE: {os.path.join(dirpath, name)}")
    if "tansparent" in dirpath:
        errors.append(f"  TYPO FOLDER: {dirpath}")

# 5. Check no "Assests" remains in tracked text files
print("=== Stale 'Assests' reference scan ===")
for check_file in ["build_template.py", "assets_index.json", "CLAUDE.md",
                    "openteams-pptx/references/brand.json"]:
    fp = os.path.join(ROOT, check_file)
    if os.path.exists(fp):
        with open(fp) as f:
            content = f.read()
        if "Assests" in content:
            errors.append(f"  STALE REF 'Assests' in: {check_file}")

# Summary
print()
if errors:
    print(f"FAILED — {len(errors)} issue(s):")
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print("ALL CHECKS PASSED ✓")
    sys.exit(0)
```

**Step 2: Run it**

```bash
cd /home/mia/dev/ppt
python3 verify_paths.py
```

Expected: `ALL CHECKS PASSED ✓`

**Step 3: If any failures, go back and fix the specific issue, then re-run**

**Step 4: Delete the verification script (it was temporary)**

```bash
rm verify_paths.py
```

---

### Task 12: Final git status check

**Step 1: Verify clean working tree**

```bash
git status
```

Expected: `nothing to commit, working tree clean`

**Step 2: Review the commit log for this session**

```bash
git log --oneline -10
```

Expected: 7–8 new commits on top of `2503f2f`, each addressing one fix category.

**Step 3: Verify no tracked files reference old paths**

```bash
git grep -l "Assests\|OpennTeams\|tansparent\|Copy of.*logo\|logo3-final" -- ':!*.pdf' ':!review/'
```

Expected: no output (no stale references in any tracked file outside PDFs and review artifacts)

---

## Summary of Changes

| # | What | Type |
|---|------|------|
| 1 | `Black-Horizontal-tansparent` → `transparent` | Folder rename |
| 2 | `OpennTeams` → `OpenTeams` (6 files) | File renames |
| 3 | Move vertical SVG to new `Black-vertical-white-background/`, move white logo to `OT_White_Logos/`, delete `Copy of` and `logo3` | File moves + deletes |
| 4 | `assets_index.json` — all `Assests/` → `Assets/`, update filenames + paths | Config update |
| 5 | `brand.json` `logo_assets` — fix `tansparent`, `OpennTeams` | Config update |
| 6 | `build_template.py` — `Assests` → `Assets` (4 occurrences) | Code fix |
| 7 | Symlink absolute → relative | Symlink fix |
| 8 | Consolidate `requirements.txt`, gitignore `__pycache__` | Cleanup |
| 9 | `CLAUDE.md` — reflect actual folder structure | Docs update |
| 10 | Drop stale git stash | Git cleanup |
| 11–12 | Full path verification + final status check | Verification |

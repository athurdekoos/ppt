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

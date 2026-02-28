# External Integrations

## Overview

This is a standalone offline tool with one optional external integration. No databases, no auth, no APIs consumed at generation time.

## Website Crawler (Optional)

**File:** `openteams-pptx/scripts/refresh_site_style.py`

**Purpose:** Crawl openteams.com to extract CSS-derived visual cues (border-radius, shadows, background colors, CSS variables). Updates `website_cues` section of `brand.json`.

**How it works:**
1. Fetches homepage HTML
2. Attempts sitemap.xml to find product/about/solution pages (max 3 additional)
3. Parses `<style>` tags and up to 2 external stylesheets per page
4. Extracts CSS variables, border-radius, box-shadow, background-color values
5. Merges into `brand.json` (additive — keeps existing keys, updates found ones)

**Safety controls:**
- Same-origin check (`_is_same_origin()`) prevents SSRF — only follows URLs on openteams.com
- Max 4 pages crawled
- External CSS capped at 200KB
- 10–15 second timeouts per request
- User-Agent: `OpenTeams-BrandBot/1.0 (template builder)`

**Trigger:** Manual only — `python refresh_site_style.py --url https://openteams.com/ --brand-json references/brand.json`

## File System

**Logo assets:** Accessed via symlink `openteams-pptx/assets/logos -> ../../Assets`. Paths resolved to absolute at brand load time in `brand_engine.py:load_brand()`.

**Output:** Generated `.pptx` files written to user-specified path via `--out` flag.

## Git / GitHub

- Repo hosted at `github.com:athurdekoos/ppt.git`
- Branch: `main`
- No CI/CD, no GitHub Actions
- No webhooks or automated deployments

## Pi Agent Integration

- `openteams-pptx/SKILL.md` defines the pi agent skill interface
- Agent invokes `generate_deck.py` via CLI
- No API server, no socket, no IPC — pure CLI invocation

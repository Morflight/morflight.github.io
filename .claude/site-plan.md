---
name: site-plan
description: Site brainstorming, page inventory, and design notes — edit freely as the project evolves
type: project
---

# Site Plan

## Purpose

Personal hub for Morflight. Acts as a business card and directory for Delta Force community resources. Links to external apps (Competitive Hub, Data Hub) and hosts two resource pages (Streamers, Community).

## Target Audience

Delta Force players — new players looking for streamers and communities, competitive players looking for scrim resources.

## Pages

| Page | File | Status | Description |
|------|------|--------|-------------|
| Home | `index.html` | done | Hero + 4 project cards (2 hosted, 2 external) |
| About | `about.html` | done | Brief profile + project list |
| Streamers | `streamers.html` | done | Streamer directory with tag/language filters and live status |
| Community | `community.html` | done | Discord/TeamSpeak server directory with tag filters |
| Contact | `contact.html` | done | Platform handles — fill in real links |

## External Projects (linked from index)

| Project | Status | Notes |
|---------|--------|-------|
| Delta Force Competitive Hub | In Development | External app — update href in index.html when live |
| Delta Force Data Hub | In Development | External app — update href in index.html when live |

## Design Notes

- Background: `#080c14`, surface: `#111827`
- Delta Force accent: `#00e5ff` (electric blue)
- MHW accent: `#f97316` (amber, secondary use only)
- Fonts: Rajdhani (headings) + Inter (body) via Google Fonts
- Dark gaming aesthetic, no build step, vanilla HTML/CSS/JS

## Live Status (Twitch)

GitHub Actions workflow at `.github/workflows/live-status.yml` runs every 5 minutes.
Writes `live-status.json` to repo root. Page reads it on load.

**Setup required:**
1. Register a Twitch app at dev.twitch.tv → get Client ID + Client Secret
2. In GitHub repo Settings → Secrets → Actions, add:
   - `TWITCH_CLIENT_ID`
   - `TWITCH_CLIENT_SECRET`
3. In `live-status.yml`, update the `LOGINS` list to match real Twitch logins in `streamers.html`

## SEO

- `sitemap.xml` and `robots.txt` at repo root
- Each page has `<title>`, `<meta description>`, `<link rel="canonical">`, Open Graph tags
- Keywords: "Delta Force streamers", "Delta Force community", "Delta Force competitive"

## GitHub Actions

- `live-status.yml` — polls Twitch every 5 minutes, writes `live-status.json`

## Content TODOs

- Fill in real streamer data in `streamers.html` (STREAMERS array + update LOGINS in workflow)
- Fill in real server data in `community.html` (SERVERS array)
- Update contact handles and hrefs in `contact.html`
- Update external project hrefs in `index.html` when apps go live

---
name: srbijavoz
description: API-first Srbija Voz scraper for notices, station lookup, and timetable support. Use when asked to check Srbija Voz announcements, train delays, cancellations, stoppages, or bus replacement service on the Novi Sad - Petrovaradin route, or when needing station autocomplete and timetable metadata from the Srbija Voz web app.
---

# Srbijavoz Scraper

## Overview

Use the bundled scraper to pull current Srbija Voz notices from the WordPress API and resolve station names from the timetable app. Prefer the API over HTML scraping. Use the notice text itself to detect service problems, especially delays, stopped trains, cancellations, and replacement buses.

## What this skill does

- Fetch current notices from `info_post`
- Resolve station names with `api/stanica/`
- Inspect timetable page metadata
- Surface disruptions by scanning notice language
- Focus on the Novi Sad - Petrovaradin corridor when asked, but treat the bus notice there as recurring service information unless a notice explicitly says it changed

## Workflow

1. Run the scraper script for current notices.
2. If the user asks about a station, resolve it through the station API.
3. Scan titles and contents for disruption keywords.
4. Classify the result as one of:
   - delay
   - stopped / standing still
   - canceled / not running
   - operational change
   - replacement bus service
   - no disruption found

## How to run

Use the bundled script:

```bash
python3 scripts/srbvoz_scraper.py --query "kašnjenje" --limit 20
python3 scripts/srbvoz_scraper.py --station "Beograd" --timetable-info
```

Useful options:

- `--query` filters notices by substring
- `--limit` limits output size
- `--station` resolves station autocomplete matches
- `--timetable-info` fetches timetable page metadata
- `--no-fallback` disables the HTML fallback

## Disruption keyword cues

Read the notice language carefully. Prioritize these Serbian cues:

- Delay: `kašnjenje`, `kasni`, `zakašnjenje`, `u kašnjenju`
- Canceled / not running: `neće saobraćati`, `izostaje`, `otkazan`, `otkazuje se`
- Stopped / held: `stoje vozovi`, `zbog smetnje`, `na licu mesta`, `do daljnjeg`
- Operational change: `izmena saobraćaja`, `privremena izmena`, `operativna izmena`
- Replacement bus: `autobuski red vožnje`, `autobus`, `organizovan besplatan prevoz`
- Novi Sad - Petrovaradin route: scan for `Petrovaradin`, `Novi Sad centar`, `Batajnica`, `Beograd centar` when the user asks about that corridor

## Output rule

When answering the user, give:
- the disruption type
- the train or route if present
- the key sentence or phrase that triggered the classification
- whether this looks like a current notice or just timetable metadata

## Script notes

The bundled script is the source of truth for current notices and station lookup. If the timetable site changes, update the script first, then adjust this skill if the workflow changes.

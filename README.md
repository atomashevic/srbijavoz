# Srbija Voz Status

`srbijavoz` is a read-only transit information skill for checking official public Srbija Voz passenger notices, station matches, and timetable metadata.

## Why this is safe to publish

- Uses only official public passenger-information endpoints from `srbvoz.rs`
- Does not log in, automate accounts, evade rate limits, or interact with protected flows
- Uses a transparent HTTP user agent instead of browser impersonation
- Runs with `python3` only for its core workflow and can use the local CA bundle when `certifi` is already present

## What it does

- fetches current public notices
- resolves station autocomplete matches
- inspects timetable page metadata
- helps classify notices into delay, stoppage, cancellation, operational change, or replacement bus service

## Run the bundled script

```bash
python3 scripts/srbvoz_scraper.py --limit 20
python3 scripts/srbvoz_scraper.py --query "kašnjenje" --limit 20
python3 scripts/srbvoz_scraper.py --station "Beograd"
python3 scripts/srbvoz_scraper.py --timetable-info
```

Useful options:

- `--query` filters notices by substring
- `--limit` limits how many notices are returned
- `--station` resolves station autocomplete matches
- `--timetable-info` fetches timetable page metadata
- `--no-fallback` disables the public HTML fallback

## Files

- `SKILL.md`: marketplace-facing skill definition
- `scripts/srbvoz_scraper.py`: bundled public-endpoint client
- `references/keyword-cues.md`: classification cues for Serbian notice text

## Notes

- The Novi Sad - Petrovaradin bus notice is often recurring timetable information.
- Do not treat that notice as a fresh disruption unless the notice explicitly says service changed, stopped, or was canceled.

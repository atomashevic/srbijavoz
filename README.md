# Srbijavoz

Tiny rail oracle, slightly dramatic, occasionally useful.

This skill watches Srbija Voz notices, checks station autocomplete, and pulls timetable metadata from the web app. It is built for the moments when you want to know whether your train is delayed, stopped, canceled, or quietly replaced by a bus that was absolutely not part of your original life plan.

## What it does

- Fetches current notices from the Srbija Voz WordPress API
- Resolves station names through the timetable app autocomplete API
- Inspects timetable page metadata
- Detects disruption language in Serbian notices
- Treats the Petrovaradin to Novi Sad centar bus notices as recurring service info, not a disruption by themselves

## When to use it

Use this skill when you want to:

- check current Srbija Voz announcements
- figure out whether a train is delayed, stopped, canceled, or rerouted
- inspect the Novi Sad, Petrovaradin, Beograd centar corridor
- look up stations from partial names
- see whether a bus replacement notice is just the usual recurring timetable update

## How it works

The main script is API first.

It reads from:

- notices: `https://www.srbvoz.rs/wp-json/wp/v2/info_post?per_page=100`
- station autocomplete: `https://w3.srbvoz.rs/redvoznje/api/stanica/`
- timetable page: `https://w3.srbvoz.rs/redvoznje/info/sr`

It looks for language like:

- `kašnjenje`, `kasni`, `zakašnjenje`
- `neće saobraćati`, `izostaje`, `otkazan`
- `stoje vozovi`, `zbog smetnje`, `do daljnjeg`
- `izmena saobraćaja`, `privremena izmena`
- `autobuski red vožnje`, `organizovan besplatan prevoz`

## Use it in OpenClaw

If the skill is installed, ask for a train status check in plain language.

Example prompts:

- "Check Srbija Voz for delays on the Petrovaradin to Beograd line"
- "What happened on my morning train from Petrovaradin to Zemun?"
- "Is the Novi Sad to Petrovaradin bus notice a disruption or a regular update?"

## Use it in Claude Code

Copy the skill folder into your Claude Code skills location, then point Claude Code at it.

Suggested copy command:

```bash
cp -R /path/to/srbijavoz ~/.claude/skills/
```

If your Claude Code setup uses a different skills directory, drop the folder there instead. The important part is that the folder contains:

- `SKILL.md`
- `scripts/srbvoz_scraper.py`
- `references/keyword-cues.md`

## Use it in Codex

Copy the skill folder into your Codex skills directory.

Suggested copy command:

```bash
cp -R /path/to/srbijavoz ~/.codex/skills/
```

Then make sure the agent can see the skill name `srbijavoz` and the bundled script.

## Repository layout

```text
srbijavoz/
├── SKILL.md
├── README.md
├── .gitignore
├── scripts/srbvoz_scraper.py
└── references/keyword-cues.md
```

## Notes

- The Petrovaradin to Novi Sad centar bus notice is recurring service information.
- Do not treat it as a fresh disruption unless a notice explicitly says it changed, stopped, or was canceled.
- If the timetable site changes, update the script first.

## Packaging

To package the skill for distribution:

```bash
python3 ~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /home/atomasevic/.openclaw/workspace/skills/srbijavoz \
  /home/atomasevic/.openclaw/workspace/dist
```

That produces a `.skill` file you can ship around like a tiny digital train ticket for machines.

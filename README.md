# Srbijavoz

<img width="640" alt="Srbijavoz skill cover" src="https://github.com/user-attachments/assets/86769c9c-2d6b-4349-a3ab-11a647dc7189" />

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

## How to use it

Once the skill is installed, ask in plain language.

Example prompts:

- "Check Srbija Voz for delays on the Petrovaradin to Beograd line"
- "What happened on my morning train from Petrovaradin to Zemun?"
- "Is the Novi Sad to Petrovaradin bus notice a disruption or a regular update?"
- "Look up the station name for Bataj"

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

## Run the bundled script directly

If you want to use the scraper outside the agent flow:

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

## Install in OpenClaw

Copy the skill folder into your OpenClaw skills directory:

```bash
cp -R /path/to/srbijavoz ~/.openclaw/skills/
```

If your OpenClaw setup uses a workspace-based skills folder instead, copy it into that environment's `skills/` directory so OpenClaw can discover the folder as `srbijavoz`.

## Install in Codex

```bash
cp -R /path/to/srbijavoz ~/.codex/skills/
```

After that, the skill can be invoked as `srbijavoz`.

## Install in Claude Code

```bash
cp -R /path/to/srbijavoz ~/.claude/skills/
```

If your setup uses a different skills directory, copy the folder there instead.

## Repository layout

```text
srbijavoz/
├── SKILL.md
├── README.md
├── .gitignore
├── scripts/
│   └── srbvoz_scraper.py
└── references/
    └── keyword-cues.md
```

## What to expect in answers

Good answers should be short, clear, and useful to a passenger first.

They should usually include:

- whether there is a current issue or not
- the affected route, train, or departure times if known
- whether it looks like a fresh same-day issue, an ongoing arrangement, or a recurring timetable notice
- what the passenger should do next, if obvious

They should usually avoid internal classifier jargon unless the user explicitly asks for it.

## Example of a good user-facing summary

```text
Today on the Novi Sad to Belgrade railway, there was a morning disruption, but not a full-day line shutdown.

What I found:
- A Petrovaradin ↔ Beograd centar service was disrupted this morning
- The 07:20 from Petrovaradin to Beograd centar and the 08:30 return did not run on the Batajnica ↔ Beograd centar segment
- I did not find a broader fresh notice saying the whole Novi Sad ↔ Belgrade corridor is down all day

What this means in practice:
- There was a real issue this morning on the corridor
- The line does not appear to be generally suspended for the rest of today, based on the notices I saw
```

Why this is good:

- leads with the practical verdict
- keeps only route and time details that matter
- separates facts from interpretation
- avoids internal classification language unless the user asks for it

## Notes

- The Petrovaradin to Novi Sad centar bus notice is recurring service information.
- Do not treat it as a fresh disruption unless a notice explicitly says it changed, stopped, or was canceled.
- If the Srbija Voz site changes, update `scripts/srbvoz_scraper.py` first.

## Packaging

```bash
python3 ~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /home/atomasevic/.openclaw/workspace/skills/srbijavoz \
  /home/atomasevic/.openclaw/workspace/dist
```

That produces a `.skill` file you can ship around like a tiny digital train ticket for machines.

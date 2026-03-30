# Srbija Voz Train Status Skill

<img width="640" alt="Srbijavoz skill cover" src="https://github.com/user-attachments/assets/86769c9c-2d6b-4349-a3ab-11a647dc7189" />

Use this skill when you want an agent to check current Srbija Voz notices, look up stations, and quickly tell you whether a train issue is a delay, cancellation, stoppage, operational change, or replacement bus service.

## What it does

The skill is built to:

- pull current notices from the official API
- resolve station names from partial input
- classify notice text into a user-friendly disruption type

## How to use it

Once the skill is installed, ask in plain language.

Example prompts:

- "Check Srbija Voz for delays between Petrovaradin and Beograd centar"
- "Look up the station name for Bataj"
- "Is there a current cancellation notice for Novi Sad trains?"
- "Check whether the Petrovaradin to Novi Sad bus notice is just regular service info"

## Run the bundled script directly

If you want to use the scraper outside the agent flow:

```bash
python3 scripts/srbvoz_scraper.py --query "kašnjenje" --limit 20
python3 scripts/srbvoz_scraper.py --station "Beograd"
python3 scripts/srbvoz_scraper.py --timetable-info
```

Useful options:

- `--query` filters notices by substring
- `--limit` limits how many notices are returned
- `--station` resolves station autocomplete matches
- `--timetable-info` fetches timetable page metadata
- `--no-fallback` disables HTML fallback behavior

## Install in Codex

```bash
cp -R /path/to/srbijavoz ~/.codex/skills/
```

After that, the skill can be invoked as `srbijavoz`.

## Install in OpenClaw

Copy the skill folder into your OpenClaw skills directory:

```bash
cp -R /path/to/srbijavoz ~/.openclaw/skills/
```

If your OpenClaw setup uses a workspace-based skills folder instead, copy it into that environment's `skills/` directory so OpenClaw can discover the folder as `srbijavoz`.

## Install in Claude Code

```bash
cp -R /path/to/srbijavoz ~/.claude/skills/
```

If your setup uses a different skills directory, copy the folder there instead.

## What to expect in answers

The skill should return:

- the disruption type
- the relevant route or station if present
- the notice language that triggered the classification
- whether the result comes from a live notice or timetable metadata

## Notes

- On the Petrovaradin - Novi Sad centar corridor, the bus notice is recurring service information.
- Do not treat that notice as a fresh disruption unless the notice explicitly says service changed, stopped, or was canceled.
- If the Srbija Voz site changes, update `scripts/srbvoz_scraper.py` first.

## Packaging

```bash
python3 ~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /home/atomasevic/.openclaw/workspace/skills/srbijavoz \
  /home/atomasevic/.openclaw/workspace/dist
```

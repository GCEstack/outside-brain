# outside-brain

External twin to Lares. Reads archived chat history and generates reviewable chat starters.

## Quick Commands

```powershell
python scripts/build_starter.py --project "EC8 Edge Crew"
python scripts/build_starter.py
```

Starters are written to `starters/pending-review/`. Review before moving to `starters/ready-to-paste/`.

## Example

```powershell
python scripts/build_starter.py --project "EC8 Edge Crew"
# -> starters/pending-review/EC8 Edge Crew - 20260706.md
```

Review the file, add your goal under "Goal for This Chat", then move it to `starters/ready-to-paste/`. Paste the contents into a new Kimi or Claude chat.

# Agent rules

## Purpose
Maintain a small, public, cross-platform Python tool that previews and renames date-bearing files.

## Non-Negotiable Rules
- Preview by default; refuse existing destinations and never edit file contents.
- Keep personal paths, credentials, logs, and example data out of git.
- Test on Windows, macOS, and Linux before a public release.
- For high-stakes or uncertain structural, financial, legal, sequencing, or destructive decisions, get a second opinion from a different model family through OpenRouter. Send generic, non-PII content only; record the decision and any disagreement in project docs.

## Structure
- `rename_dates.py`: command-line tool.
- `test_rename_dates.py`: focused behavior and safety tests.
- `README.md`: public usage and safety notes.
- `Date Filename Renamer - System Overview.md` and `Date Filename Renamer - File Registry.md`: project documentation.

## API Access
None. The tool uses only Python's standard library and needs no credentials.

## Change Log
- 2026-11-18: Initial public-tool implementation.

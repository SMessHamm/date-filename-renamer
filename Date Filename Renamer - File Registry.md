# Date Filename Renamer — File Registry

| File | Purpose |
|---|---|
| `rename_dates.py` | Preview and apply recursive filename renames; writes a local CSV log on apply |
| `test_rename_dates.py` | Date format, collision, recursion, and failure tests |
| `README.md` | Public usage, examples, and safety notes |
| `LICENSE` | MIT reuse terms |
| `.github/workflows/tests.yml` | Cross-platform test workflow |
| `agents.md`, `CLAUDE.md` | Agent operating rules |
| `.gitignore` | Ignores runtime logs and local files |
| `scripts/publish_docs_to_obsidian.sh` | Optional local documentation mirroring; destination comes from untracked Git config |

Runtime `rename-log-*.csv` files are created in the working directory and are not part of the repository.

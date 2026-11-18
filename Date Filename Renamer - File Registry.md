# Date Filename Renamer — File Registry

| File | Purpose |
|---|---|
| `rename_dates.py` | Generate editable proposals CSV and apply its selected filename changes; writes a CSV log on apply |
| `test_rename_dates.py` | Date format, collision, recursion, and failure tests |
| `README.md` | Public usage, examples, and safety notes |
| `LICENSE` | MIT reuse terms |
| `.github/workflows/tests.yml` | Cross-platform test workflow |
| `agents.md`, `CLAUDE.md` | Agent operating rules |
| `.gitignore` | Ignores proposal CSVs, runtime logs, and local files |
| `scripts/publish_docs_to_obsidian.sh` | Optional local documentation mirroring; destination comes from untracked Git config |

Runtime `rename-proposals-*.csv` and `rename-log-*.csv` files are created in the working directory and are not part of the repository.

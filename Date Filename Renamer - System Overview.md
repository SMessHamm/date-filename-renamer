# Date Filename Renamer — System Overview

This standalone Python tool turns one valid day-month-year date in a filename into a `YYYYMMDD` prefix. It searches supplied folders recursively, previews by default, and changes names only with `--apply`.

It supports compact and underscore-separated dates with two- or four-digit years. Two-digit years use a fixed 50-year cutoff: `00`–`49` map to 2000–2049, and `50`–`99` map to 1950–1999. It skips invalid, multiple, and already formatted dates, dot-prefixed entries, and symbolic links.

The full rename set is checked for collisions before applying. Successful changes are recorded in a CSV log in the current working directory. An unexpected failure stops the run; completed renames remain in place and in the log. The log supports manual reversal but does not back up file contents.

The tool uses Python 3.10+ and no external services or credentials. Run `python -m unittest discover -v` to test it. GitHub Actions checks Windows, macOS, and Linux.

Public documentation and code contain no machine-specific paths. Any local documentation mirroring is configured only in the repository's untracked Git config.

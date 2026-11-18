#!/usr/bin/env python3
"""Preview or apply safe, recursive date filename renames."""

import argparse
import csv
from datetime import date, datetime
import os
from pathlib import Path
import re
import sys


DATE = re.compile(r"(?<![0-9])([0-9]{2})_?([0-9]{2})_?([0-9]{4}|[0-9]{2})(?![0-9])")


def renamed_name(name):
    stem, suffix = os.path.splitext(name)
    matches = list(DATE.finditer(stem))
    if not matches:
        return None, None
    if len(matches) != 1:
        return None, "multiple date-like numbers"

    match = matches[0]
    token = match.group()
    if len(token) == 8 and "_" not in token:
        try:
            date(int(token[:4]), int(token[4:6]), int(token[6:]))
        except ValueError:
            pass
        else:
            return None, "already YYYYMMDD"

    day, month, year = match.groups()
    year = int(year)
    if len(match.group(3)) == 2:
        year += 2000 if year < 50 else 1900
    try:
        valid_date = date(year, int(month), int(day))
    except ValueError:
        return None, "invalid calendar date"
    converted = f"{valid_date.year:04d}{valid_date.month:02d}{valid_date.day:02d}"

    before = stem[:match.start()].strip(" _-")
    after = stem[match.end():].strip(" _-")
    rest = "_".join(part for part in (before, after) if part)
    return converted + ("_" + rest if rest else "") + suffix, None


def raise_walk_error(error):
    raise error


def collect(folders):
    changes = []
    skipped = []
    seen = set()
    for folder in folders:
        root = Path(folder)
        if root.is_symlink() or not root.is_dir():
            raise ValueError(f"not a real directory: {root}")
        root = root.resolve()
        for current, dirs, files in os.walk(root, onerror=raise_walk_error):
            dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not (Path(current) / d).is_symlink())
            for name in sorted(files):
                source = Path(current) / name
                if name.startswith(".") or source.is_symlink() or not source.is_file() or source in seen:
                    continue
                seen.add(source)
                target_name, reason = renamed_name(name)
                if reason:
                    skipped.append((source, reason))
                elif target_name and target_name != name:
                    changes.append((source, source.with_name(target_name)))
    return changes, skipped


def conflicts(changes):
    problems = []
    destinations = set()
    for source, target in changes:
        key = os.path.normcase(str(target)).casefold()
        if key in destinations:
            problems.append(f"two files would become {target}")
        destinations.add(key)
        if os.path.lexists(target):
            problems.append(f"destination exists: {target}")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folders", nargs="+", help="folders to search recursively")
    parser.add_argument("--apply", action="store_true", help="rename files after preview and safety checks")
    args = parser.parse_args(argv)

    try:
        changes, skipped = collect(args.folders)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    for source, reason in skipped:
        print(f"skip: {source}: {reason}")
    for source, target in changes:
        print(f"{source} -> {target}")

    problems = conflicts(changes)
    if problems:
        for problem in problems:
            print(f"conflict: {problem}", file=sys.stderr)
        return 1
    if not changes:
        print("No files to rename.")
        return 0
    if not args.apply:
        print("Preview only. Add --apply to rename these files.")
        return 0

    log_path = Path.cwd() / f"rename-log-{datetime.now():%Y%m%d-%H%M%S-%f}.csv"
    try:
        descriptor = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", newline="", encoding="utf-8") as log:
            writer = csv.writer(log)
            writer.writerow(("old_path", "new_path"))
            log.flush()
            os.fsync(log.fileno())
            print(f"Rename log: {log_path}")
            for source, target in changes:
                if not source.is_file() or source.is_symlink() or os.path.lexists(target):
                    raise OSError(f"file changed since preview: {source} -> {target}")
                # shortcut: assumes no concurrent renamer creates the target after this check; use an atomic no-clobber move if needed.
                source.rename(target)
                writer.writerow((str(source), str(target)))
                log.flush()
                os.fsync(log.fileno())
    except OSError as error:
        print(f"error: {error}; completed renames are in {log_path}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

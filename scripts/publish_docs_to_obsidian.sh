#!/bin/sh
set -eu

root=$(git rev-parse --show-toplevel)
destination=$(git config --local --get project.obsidianDir || true)
[ -n "$destination" ] || exit 0
mkdir -p "$destination"
for name in 'agents.md' 'Date Filename Renamer - System Overview.md' 'Date Filename Renamer - File Registry.md'; do
    cp -p "$root/$name" "$destination/$name"
done

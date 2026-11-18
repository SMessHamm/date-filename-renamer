# Date Filename Renamer

A small Python command-line tool that moves a date to the start of each filename. It previews changes before touching files.

Requires Python 3.10 or newer. No installation or third-party packages are needed.

## Use

```sh
python rename_dates.py "/path/to/first folder" "/path/to/second folder"
python rename_dates.py --apply "/full/path/to/the/generated-proposals.csv"
```

Use `python3` instead of `python` if that is how Python is installed on your computer. The first command searches subfolders recursively and writes a `rename-proposals-*.csv` file in your current working directory. Use its actual filename in the second command. Quote paths that contain spaces.

Open the proposals CSV in a spreadsheet or text editor. Leave `old_path` alone and edit only `proposed_name`. Change a proposed filename to use your own name; clear its cell or delete its entire row to leave that file untouched. Save it as UTF-8 CSV, then run `--apply` with its path. The tool renames eligible date files within their original folders; a proposed name cannot contain a directory path. Use only CSV files you created and reviewed yourself.

| Before | After |
|---|---|
| `Report_31122024_v2.pdf` | `20241231_Report_v2.pdf` |
| `Report_31_12_24.pdf` | `20241231_Report.pdf` |
| `Photo_3112_2024.jpg` | `20241231_Photo.jpg` |
| `31_1224.txt` | `20241231.txt` |

Dates use day, month, year order. Underscores between the parts are optional: `DDMMYYYY`, `DD_MM_YYYY`, `DDMM_YYYY`, `DD_MMYYYY`, and the same forms with `YY`. Two-digit years `00`–`49` mean 2000–2049; `50`–`99` mean 1950–1999.

## Safety

- The default command prints proposed changes and writes an editable CSV. Review it before using `--apply`, especially for six-digit numbers that might be something other than dates.
- Invalid dates, files with more than one date-like number, and names already containing a valid `YYYYMMDD` date are skipped.
- Dot-prefixed files and directories and symbolic links are skipped. File contents are never edited.
- Before applying the CSV, the tool checks that sources still exist and proposed names are valid. If a proposed filename already exists or two files would get the same name, the run stops before renaming anything. Resolve the conflict in the CSV and retry.
- An apply run writes `rename-log-*.csv` in your current working directory. It records completed old and new paths so you can reverse them manually. If a filesystem error interrupts a run, earlier renames remain in place and in the log.
- The log is **not a content backup**. Back up irreplaceable files first. Do not run the tool while another process is changing filenames in the same folders.

After `--apply`, check the renamed files and the CSV log. If a run stops partway through, the CSV lists successful moves. To reverse them, rename each recorded `new_path` back to its `old_path`, starting with the last row; check that the old name is free before each reversal. A read-only or unsupported filesystem can stop a run without changing the remaining files.

Run the tests with `python -m unittest discover -v`.

Licensed under MIT; see [LICENSE](LICENSE).

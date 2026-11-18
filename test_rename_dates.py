import contextlib
import csv
from io import StringIO
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import rename_dates


class RenameDatesTests(unittest.TestCase):
    def test_date_forms_and_placement(self):
        examples = {
            "Report_31122024_v2.pdf": "20241231_Report_v2.pdf",
            "Report_31_12_24_v2.pdf": "20241231_Report_v2.pdf",
            "Report_3112_2024.pdf": "20241231_Report.pdf",
            "Report_31_1224.pdf": "20241231_Report.pdf",
            "311224.txt": "20241231.txt",
            "010150_note.txt": "19500101_note.txt",
            "311249_note.txt": "20491231_note.txt",
            "01010001_note.txt": "00010101_note.txt",
        }
        for old, new in examples.items():
            with self.subTest(old=old):
                self.assertEqual(rename_dates.renamed_name(old), (new, None))

    def test_ambiguous_or_invalid_names_are_skipped(self):
        for name in ("Report_31022024.pdf", "Report_31_12_24_01_01_25.pdf", "Report_20241231.pdf"):
            with self.subTest(name=name):
                self.assertIsNone(rename_dates.renamed_name(name)[0])

    def test_preview_then_recursive_apply_with_log(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            nested = root / "nested"
            nested.mkdir()
            source = nested / "Report_31_12_24.txt"
            source.write_text("original", encoding="utf-8")
            (root / ".hidden_31_12_24.txt").write_text("hidden", encoding="utf-8")
            with contextlib.redirect_stdout(StringIO()):
                self.assertEqual(rename_dates.main([str(root), str(nested)]), 0)
            self.assertTrue(source.exists())

            before = Path.cwd()
            try:
                os.chdir(root)
                with contextlib.redirect_stdout(StringIO()):
                    self.assertEqual(rename_dates.main([str(root), str(nested), "--apply"]), 0)
            finally:
                os.chdir(before)
            target = nested / "20241231_Report.txt"
            self.assertEqual(target.read_text(encoding="utf-8"), "original")
            self.assertFalse(source.exists())
            logs = list(root.glob("rename-log-*.csv"))
            self.assertEqual(len(logs), 1)
            with logs[0].open(newline="", encoding="utf-8") as log:
                self.assertEqual(list(csv.reader(log)), [["old_path", "new_path"], [str(source), str(target)]])

    def test_collision_stops_everything(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = root / "Report_31122024.txt"
            target = root / "20241231_Report.txt"
            source.write_text("source", encoding="utf-8")
            target.write_text("target", encoding="utf-8")
            with contextlib.redirect_stdout(StringIO()), contextlib.redirect_stderr(StringIO()):
                self.assertEqual(rename_dates.main([str(root), "--apply"]), 1)
            self.assertEqual(source.read_text(encoding="utf-8"), "source")
            self.assertEqual(target.read_text(encoding="utf-8"), "target")

    def test_case_only_destination_collision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            changes = [
                (root / "A_31122024.txt", root / "20241231_Report.txt"),
                (root / "B_31122024.txt", root / "20241231_report.txt"),
            ]
            self.assertTrue(rename_dates.conflicts(changes))

    def test_unexpected_error_stops_and_keeps_success_log(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            first = root / "A_01012024.txt"
            second = root / "B_02012024.txt"
            first.touch()
            second.touch()
            actual_rename = Path.rename

            def fail_second(path, target):
                if path == second:
                    raise PermissionError("simulated failure")
                return actual_rename(path, target)

            before = Path.cwd()
            try:
                os.chdir(root)
                with patch.object(Path, "rename", fail_second), contextlib.redirect_stdout(StringIO()), contextlib.redirect_stderr(StringIO()):
                    self.assertEqual(rename_dates.main([str(root), "--apply"]), 1)
            finally:
                os.chdir(before)
            self.assertTrue((root / "20240101_A.txt").exists())
            self.assertTrue(second.exists())
            with next(root.glob("rename-log-*.csv")).open(newline="", encoding="utf-8") as log:
                self.assertEqual(len(list(csv.reader(log))), 2)


if __name__ == "__main__":
    unittest.main()

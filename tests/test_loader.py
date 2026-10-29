import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook

from kpi_monitor.config import load_config
from kpi_monitor.loader import load_data


class LoaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = load_config(Path(__file__).resolve().parents[1] / "config" / "kpi_config.json")
        self.config["input_dir"] = Path(self.temp.name) / "input"
        self.config["output_dir"] = Path(self.temp.name) / "output"
        self.headers = [self.config["site_column"], self.config["date_column"]] + list(self.config["kpis"].values())

    def write(self, name, rows, headers=None):
        self.config["input_dir"].mkdir(exist_ok=True)
        book = Workbook()
        book.active.append(self.headers if headers is None else headers)
        for row in rows:
            book.active.append(row)
        book.save(self.config["input_dir"] / name)
        book.close()

    def test_missing_folder_and_no_xlsx(self):
        with self.assertRaisesRegex(ValueError, str(self.config["input_dir"]).replace("\\", "\\\\")):
            load_data(self.config)
        self.assertTrue(self.config["input_dir"].is_dir())
        self.assertTrue(self.config["output_dir"].is_dir())
        self.write("~$ignored.xlsx", [])
        (self.config["input_dir"] / "ignored.csv").write_text("ignored")
        with self.assertRaisesRegex(ValueError, "No hay archivos xlsx"):
            load_data(self.config)

    def test_missing_each_column(self):
        for missing in self.headers:
            with self.subTest(column=missing):
                self.write("missing.xlsx", [], [h for h in self.headers if h != missing])
                with self.assertRaises(ValueError) as caught:
                    load_data(self.config)
                self.assertIn(missing, str(caught.exception))
                self.assertIn("missing.xlsx", str(caught.exception))
                # Windows rejects unlink if the failed read still holds the file.
                (self.config["input_dir"] / "missing.xlsx").unlink()

    def test_values_and_duplicates_preserved(self):
        first = []
        second = []
        for index in range(7):
            row = [" S{} ".format(index), datetime(2026, 1, 1, 1), None, "KPI_SECRET", 0, 1.5, -2, "text", 7, 8]
            first.extend([row, list(row)])
            other = list(row)
            other[0] = row[0].strip()
            other[1] = datetime(2026, 1, 1, 23)
            second.append(other)
        self.write("a.xlsx", first)
        self.write("b.xlsx", second)
        with self.assertLogs("kpi_monitor.loader", level="WARNING") as captured:
            result = load_data(self.config)
        self.assertEqual(result.headers, tuple(self.headers))
        self.assertEqual(result.rows, [tuple(row) for row in first + second])
        self.assertEqual(len(captured.records), 1)
        message = captured.records[0].getMessage()
        self.assertIn("7 claves", message)
        self.assertNotIn("KPI_SECRET", message)
        self.assertIn("S4", message)
        self.assertNotIn("S5", message)
        self.assertNotIn("S6", message)


if __name__ == "__main__":
    unittest.main()

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "scanner" / "scan.py"
RUNTIME_DETECTOR = ROOT / "scanner" / "runtime_detector.py"
RUN_LAB = ROOT / "runtime" / "run_lab.py"


def scan(path: Path, ruleset: str = "v2") -> list[dict]:
    proc = subprocess.run(
        [sys.executable, str(SCAN), str(path), "--ruleset", ruleset, "--format", "json"],
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(proc.stdout)


class ScannerTests(unittest.TestCase):
    def test_all_ten_benign_are_clear(self):
        results = scan(ROOT / "skills" / "benign")
        self.assertEqual(10, len(results))
        self.assertEqual({"Benign"}, {row["verdict"] for row in results}, results)

    def test_v2_catches_all_three_malicious(self):
        results = scan(ROOT / "skills" / "malicious")
        self.assertEqual(3, len(results))
        self.assertEqual({"Malicious"}, {row["verdict"] for row in results}, results)

    def test_v1_documents_obfuscation_miss(self):
        results = scan(ROOT / "skills" / "malicious", "v1")
        verdicts = {row["skill"]: row["verdict"] for row in results}
        self.assertEqual("Benign", verdicts["release-notes-decoder"])
        self.assertEqual("Malicious", verdicts["cloud-diagnostics-helper"])
        self.assertEqual("Malicious", verdicts["workspace-formatter"])

    def test_runtime_correlations_catch_all_fixtures(self):
        with tempfile.TemporaryDirectory() as tmp:
            events = Path(tmp) / "events.jsonl"
            subprocess.run([sys.executable, str(RUN_LAB), str(ROOT / "skills" / "malicious"), "--output", str(events)], check=True)
            proc = subprocess.run([sys.executable, str(RUNTIME_DETECTOR), str(events)], check=True, text=True, capture_output=True)
            result = json.loads(proc.stdout)
        self.assertEqual(3, len(result["sessions"]))
        self.assertEqual({"Malicious"}, {row["verdict"] for row in result["sessions"]}, result)


if __name__ == "__main__":
    unittest.main()

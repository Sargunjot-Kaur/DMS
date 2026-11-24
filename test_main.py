import json
import sys
from unittest.mock import patch

from main import main


def test_default_run_prints_json_without_calling_aws(monkeypatch, capsys):
  monkeypatch.setattr(sys, "argv", ["main.py", "raw_data/property_data_raw.csv"])

  with patch("boto3.client") as client:
    main()

  client.assert_not_called()
  report = json.loads(capsys.readouterr().out)
  assert report["rows_checked"] == 60


def test_s3_upload_matches_the_printed_report(monkeypatch, capsys):
  monkeypatch.setattr(sys, "argv", [
    "main.py", "raw_data/property_data_raw.csv",
    "--s3-output", "s3://dms-reports/checks/report.json"
  ])

  with patch("boto3.client") as client:
    main()

  report_json = capsys.readouterr().out.rstrip("\n")
  client.assert_called_once_with("s3")
  client.return_value.put_object.assert_called_once_with(
    Bucket="dms-reports",
    Key="checks/report.json",
    Body=report_json.encode("utf-8"),
    ContentType="application/json",
  )

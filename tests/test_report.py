import json

from loom.reporting.report import MigrationReport


def test_migration_report_save_json(tmp_path):
    report = MigrationReport(
        source_file="examples/python2/legacy.py",
        target_file="migrated.py",
        language="python",
        translated=True,
        verified=True,
        original_output="Hello, Legacy Loom",
        translated_output="Hello, Legacy Loom",
    )

    output_file = tmp_path / "migration_report.json"

    report.save_json(str(output_file))

    assert output_file.exists()

    with output_file.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    assert data["source_file"] == "examples/python2/legacy.py"
    assert data["target_file"] == "migrated.py"
    assert data["language"] == "python"
    assert data["translated"] is True
    assert data["verified"] is True
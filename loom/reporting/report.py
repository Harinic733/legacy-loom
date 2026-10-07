from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class MigrationReport:
    """Stores the result of a Legacy Loom migration."""

    source_file: str
    target_file: str
    language: str
    translated: bool
    verified: bool
    original_output: str
    translated_output: str

    def display(self) -> str:
        """Create a readable migration report."""

        status = "PASSED" if self.verified else "FAILED"

        return f"""
Legacy Loom Migration Report
────────────────────────────
Source: {self.source_file}
Target: {self.target_file}
Language: {self.language}

Translation
✓ Translation completed: {self.translated}

Verification
{'✓' if self.verified else '✗'} Behavioral verification: {status}

Original Output
{self.original_output}

Translated Output
{self.translated_output}

Final Result
{'✓ Migration verified successfully.' if self.verified else '✗ Migration verification failed.'}
"""

    def save_json(self, output_path: str = "reports/migration_report.json"):
        """Save the migration report as a JSON file."""

        path = Path(output_path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                asdict(self),
                file,
                indent=4,
            )
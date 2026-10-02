from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class CodeAnalysis:
    """Structured information extracted from a legacy source file."""

    file_path: str
    language: str
    total_lines: int
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)


class ReaderAgent:
    """Analyzes legacy source code before migration."""

    def detect_language(self, file_path: str) -> str:
        """Detect the programming language from the file extension."""

        extension = Path(file_path).suffix.lower()

        languages = {
            ".py": "python",
            ".php": "php",
            ".cob": "cobol",
            ".cbl": "cobol",
            ".go": "go",
            ".rs": "rust",
        }

        return languages.get(extension, "unknown")

    def analyze(self, file_path: str) -> CodeAnalysis:
        """Read and analyze a source file."""

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")

        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()

        language = self.detect_language(file_path)

        functions = []
        classes = []
        imports = []

        for line in lines:
            stripped = line.strip()

            if stripped.startswith("def "):
                name = stripped[4:].split("(")[0]
                functions.append(name)

            elif stripped.startswith("class "):
                name = stripped[6:].split("(")[0].split(":")[0]
                classes.append(name)

            elif stripped.startswith("import "):
                imports.append(stripped)

            elif stripped.startswith("from "):
                imports.append(stripped)

        return CodeAnalysis(
            file_path=str(path),
            language=language,
            total_lines=len(lines),
            functions=functions,
            classes=classes,
            imports=imports,
        )
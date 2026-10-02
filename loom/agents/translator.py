from pathlib import Path
import re


class TranslatorAgent:
    """Converts supported legacy code into a modern equivalent."""

    def translate_python2_to_python3(self, source: str) -> str:
        """Translate common Python 2 syntax into Python 3 syntax."""

        translated = source

        # Convert Python 2 print statements:
        # print "Hello"
        # → print("Hello")
        translated = re.sub(
            r'(?m)^(\s*)print\s+(.+)$',
            r'\1print(\2)',
            translated,
        )

        # Convert raw_input() to input()
        translated = translated.replace("raw_input(", "input(")

        return translated

    def translate(self, file_path: str, target: str = "python3") -> str:
        """Read a legacy file and return translated source code."""

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Source file not found: {file_path}"
            )

        source = path.read_text(encoding="utf-8")

        if target.lower() == "python3":
            return self.translate_python2_to_python3(source)

        raise ValueError(
            f"Unsupported target language: {target}"
        )

    def save_translation(
        self,
        source: str,
        output_path: str,
    ) -> None:
        """Save translated source code to a file."""

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(source, encoding="utf-8")
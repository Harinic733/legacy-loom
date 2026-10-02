import typer
from rich.console import Console

from loom.agents.reader import ReaderAgent
from loom.agents.translator import TranslatorAgent
from loom.agents.verifier import VerifierAgent

app = typer.Typer(
    name="loom",
    help="Legacy Loom - verified legacy code migration system."
)

console = Console()


@app.command()
def version():
    """Show the Legacy Loom version."""
    console.print("[bold]Legacy Loom[/bold] v0.1.0")


@app.command()
def analyze(file_path: str):
    """Analyze a legacy source file."""

    reader = ReaderAgent()

    try:
        result = reader.analyze(file_path)

        console.print("\n[bold]Legacy Loom Analysis[/bold]")
        console.print("────────────────────────────")
        console.print(f"File: {result.file_path}")
        console.print(f"Language: {result.language}")
        console.print(f"Lines: {result.total_lines}")

        console.print("\n[bold]Functions:[/bold]")
        for function in result.functions:
            console.print(f"  • {function}")

        console.print("\n[bold]Classes:[/bold]")
        for class_name in result.classes:
            console.print(f"  • {class_name}")

        console.print("\n[bold]Imports:[/bold]")
        for import_name in result.imports:
            console.print(f"  • {import_name}")

    except FileNotFoundError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)


@app.command()
def migrate(file_path: str):
    """Translate and verify a Python 2 file."""

    reader = ReaderAgent()
    translator = TranslatorAgent()
    verifier = VerifierAgent()

    try:
        # 1. Analyze the original code
        analysis = reader.analyze(file_path)

        console.print("\n[bold]Legacy Loom Migration[/bold]")
        console.print("────────────────────────────")
        console.print(f"File: {analysis.file_path}")
        console.print(f"Detected language: {analysis.language}")

        if analysis.language != "python":
            console.print(
                "[yellow]Warning:[/yellow] "
                "This migration version supports Python files."
            )
            raise typer.Exit(code=1)

        # 2. Translate Python 2 → Python 3
        translated = translator.translate(
            file_path,
            target="python3",
        )

        output_path = "migrated.py"

        translator.save_translation(
            translated,
            output_path,
        )

        console.print(
            f"\n[green]✓ Translation complete:[/green] {output_path}"
        )

        # 3. Verify original vs translated program
        console.print("\n[bold]Running behavioral verification...[/bold]")

        result = verifier.verify(
            file_path,
            output_path,
        )

        # 4. Display results
        console.print("\n[bold]Verification Results[/bold]")
        console.print("────────────────────────────")

        if result.passed:
            console.print(
                "[bold green]✓ VERIFICATION PASSED[/bold green]"
            )
            console.print(
                "Original and translated programs produced the same output."
            )
        else:
            console.print(
                "[bold red]✗ VERIFICATION FAILED[/bold red]"
            )

            console.print("\n[bold]Original output:[/bold]")
            console.print(result.original_output)

            console.print("[bold]Translated output:[/bold]")
            console.print(result.translated_output)

    except FileNotFoundError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)

    except ValueError as error:
        console.print(f"[red]Error:[/red] {error}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
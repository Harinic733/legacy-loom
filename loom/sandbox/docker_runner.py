import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass
class DockerResult:
    """Result from running a program inside Docker."""

    success: bool
    output: str
    error: str
    exit_code: int


class DockerRunner:
    """Runs legacy programs inside isolated Docker containers."""

    def run_python2(self,source_file: str,test_input: str = "",) -> DockerResult:
        """Run any Python 2 source file inside Docker."""

        path = Path(source_file).resolve()

        if not path.exists():
            return DockerResult(
                success=False,
                output="",
                error=f"Source file not found: {source_file}",
                exit_code=-1,
            )

        command = [
            "docker",
            "run",
            "--rm",
             "-i",
            "--network",
            "none",
            "-v",
            f"{path.parent}:/workspace:ro",
            "legacy-loom-python2",
            "python",
            f"/workspace/{path.name}",
        ]

        try:
            process = subprocess.run(
                command,
                input= test_input,
                capture_output=True,
                text=True,
                timeout=30,
            )

            return DockerResult(
                success=process.returncode == 0,
                output=process.stdout,
                error=process.stderr,
                exit_code=process.returncode,
            )

        except subprocess.TimeoutExpired:
            return DockerResult(
                success=False,
                output="",
                error="Docker execution timed out.",
                exit_code=-1,
            )

        except FileNotFoundError:
            return DockerResult(
                success=False,
                output="",
                error="Docker was not found. Is Docker Desktop running?",
                exit_code=-1,
            )
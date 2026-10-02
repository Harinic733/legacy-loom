from dataclasses import dataclass

from loom.sandbox.docker_runner import DockerRunner


@dataclass
class VerificationResult:
    """Result of comparing two program executions."""

    passed: bool
    original_output: str
    translated_output: str
    original_error: str
    translated_error: str


class VerifierAgent:
    """Compares legacy and translated program behavior."""

    def __init__(self):
        self.docker_runner = DockerRunner()

    def verify(
        self,
        original_path: str,
        translated_path: str,
    ) -> VerificationResult:
        """Run the legacy program in Docker and the translated program locally."""

        original_result = self.docker_runner.run_python2(original_path)

        translated_result = self._run_translated(translated_path)

        passed = (
            original_result.output == translated_result[0]
            and original_result.error == translated_result[1]
            and original_result.success == translated_result[2]
        )

        return VerificationResult(
            passed=passed,
            original_output=original_result.output,
            translated_output=translated_result[0],
            original_error=original_result.error,
            translated_error=translated_result[1],
        )

    def _run_translated(self, file_path: str) -> tuple[str, str, bool]:
        """Run the translated Python 3 program."""

        import subprocess
        import sys

        try:
            process = subprocess.run(
                [sys.executable, file_path],
                capture_output=True,
                text=True,
                timeout=30,
            )

            return (
                process.stdout,
                process.stderr,
                process.returncode == 0,
            )

        except subprocess.TimeoutExpired:
            return "", "Translated program timed out.", False
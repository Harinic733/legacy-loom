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
        """Run both programs with the same test input."""

        test_input = "10 20 30\n"

        original_result = self.docker_runner.run_python2(
            original_path,
            test_input,
        )

        translated_result = self._run_translated(
            translated_path,
            test_input,
        )

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

    def _run_translated(
        self,
        file_path: str,
        test_input: str,
    ) -> tuple[str, str, bool]:
        """Run the translated Python 3 program with test input."""

        import subprocess
        import sys

        try:
            process = subprocess.run(
                [sys.executable, file_path],
                input=test_input,
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
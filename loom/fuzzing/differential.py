from dataclasses import dataclass

from loom.sandbox.docker_runner import DockerRunner


@dataclass
class FuzzResult:
    """Result of a differential test."""

    passed: bool
    test_input: str
    original_output: str
    translated_output: str


class DifferentialTester:
    """Compare legacy and migrated programs."""

    def __init__(self):
        self.docker_runner = DockerRunner()

    def compare(
        self,
        original_file: str,
        translated_file: str,
        test_inputs: list[str],
    ) -> list[FuzzResult]:
        """Compare both versions using multiple test inputs."""

        results = []

        for test_input in test_inputs:
            original_result = self.docker_runner.run_python2(
                original_file,
                test_input,
            )

            translated_result = self._run_python3(
                translated_file,
                test_input,
            )

            results.append(
                FuzzResult(
                    passed=(
                        original_result.output
                        == translated_result
                    ),
                    test_input=test_input,
                    original_output=original_result.output,
                    translated_output=translated_result,
                )
            )

        return results

    def _run_python3(
        self,
        file_path: str,
        test_input: str,
    ) -> str:
        """Run the migrated Python 3 program."""

        import subprocess
        import sys

        process = subprocess.run(
            [sys.executable, file_path],
            input=test_input,
            capture_output=True,
            text=True,
            timeout=10,
        )

        return process.stdout
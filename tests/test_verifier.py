from pathlib import Path

from loom.agents.verifier import VerifierAgent


def test_verifier_detects_matching_behavior(tmp_path):
    original = tmp_path / "original.py"
    translated = tmp_path / "translated.py"

    original.write_text(
        'print("Legacy Loom")\n',
        encoding="utf-8",
    )

    translated.write_text(
        'print("Legacy Loom")\n',
        encoding="utf-8",
    )

    verifier = VerifierAgent()

    result = verifier.verify(
        str(original),
        str(translated),
    )

    assert result.passed is True


def test_verifier_detects_behavior_mismatch(tmp_path):
    original = tmp_path / "original.py"
    translated = tmp_path / "translated.py"

    original.write_text(
        'print("Legacy Loom")\n',
        encoding="utf-8",
    )

    translated.write_text(
        'print("Wrong Result")\n',
        encoding="utf-8",
    )

    verifier = VerifierAgent()

    result = verifier.verify(
        str(original),
        str(translated),
    )

    assert result.passed is False
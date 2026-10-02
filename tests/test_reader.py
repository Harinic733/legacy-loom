from loom.agents.reader import ReaderAgent


def test_reader_detects_python():
    reader = ReaderAgent()

    result = reader.analyze("examples/python2/legacy.py")

    assert result.language == "python"
    assert result.total_lines > 0
    assert "calculate_total" in result.functions
    assert "greet" in result.functions
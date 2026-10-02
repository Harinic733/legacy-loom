from hypothesis import given, settings, strategies as st

from loom.fuzzing.differential import DifferentialTester


@given(
    st.lists(
        st.integers(min_value=-100, max_value=100),
        min_size=0,
        max_size=10,
    )
)
@settings(max_examples=10)
def test_differential_tester(numbers):
    tester = DifferentialTester()

    test_input = ""

    results = tester.compare(
        original_file="docker/legacy.py",
        translated_file="migrated.py",
        test_inputs=[test_input],
    )

    assert len(results) == 1
    assert results[0].passed is True
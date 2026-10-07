from hypothesis import given, settings, strategies as st

from loom.fuzzing.differential import DifferentialTester


@given(
    st.lists(
        st.integers(min_value=-100, max_value=100),
        min_size=1,
        max_size=10,
    )
)
@settings(max_examples=10, deadline=None)
def test_differential_tester(numbers):
    tester = DifferentialTester()

    test_input = " ".join(str(number) for number in numbers) + "\n"

    results = tester.compare(
        original_file="examples/python2/legacy.py",
        translated_file="migrated.py",
        test_inputs=[test_input],
    )

    assert len(results) == 1
    assert results[0].passed is True
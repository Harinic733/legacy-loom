from hypothesis import strategies as st


class InputGenerator:
    """Generates test inputs for migrated programs."""

    def integer_lists(self):
        """Generate lists of integers."""
        return st.lists(
            st.integers(min_value=-100, max_value=100),
            min_size=0,
            max_size=20,
        )

    def strings(self):
        """Generate test strings."""
        return st.text(
            min_size=0,
            max_size=30,
        )

    def integers(self):
        """Generate individual integers."""
        return st.integers(
            min_value=-1000,
            max_value=1000,
        )
"""
Tests for gaze-to-click pipeline.
"""

import unittest
from main import generate_samples, run_pipeline, MIN_CLICK_INTERVAL_MS


class TestClickDebounce(unittest.TestCase):
    """Regression tests for click debouncing."""

    def test_no_double_clicks(self):
        """No two clicks should occur within MIN_CLICK_INTERVAL_MS of each other."""
        samples = generate_samples()
        clicks = run_pipeline(samples)

        self.assertGreater(len(clicks), 0, "Should detect at least one click")

        violations = []
        for i in range(1, len(clicks)):
            gap_ms = (clicks[i] - clicks[i-1]) * 1000
            if gap_ms < MIN_CLICK_INTERVAL_MS:
                violations.append(
                    f"Clicks {i} and {i+1}: gap={gap_ms:.1f}ms (min={MIN_CLICK_INTERVAL_MS}ms)"
                )

        self.assertEqual(
            violations, [],
            f"Found {len(violations)} double-click violation(s):\n" + "\n".join(violations)
        )

    def test_clicks_are_monotonic(self):
        """Click timestamps should be strictly increasing."""
        samples = generate_samples()
        clicks = run_pipeline(samples)

        for i in range(1, len(clicks)):
            self.assertGreater(
                clicks[i], clicks[i-1],
                f"Click timestamps not monotonic at index {i}"
            )


if __name__ == "__main__":
    unittest.main()

"""
Gaze-to-click pipeline simulation.

Monitors synthetic gaze data and emits CLICK events when gaze is stable.
"""

import random
import math

MIN_CLICK_INTERVAL_MS = 300
STABILITY_THRESHOLD = 50.0     # max velocity (pixels/sec) to be considered "stable"
STABLE_FRAMES_REQUIRED = 8     # consecutive stable frames to trigger intent

def generate_samples(n=2000, hz=120):
    """
    Generate synthetic gaze samples.
    Returns list of (t, x, y, valid) tuples.
    t is in seconds, x/y are gaze coords, valid indicates tracking quality.
    """
    random.seed(0)
    samples = []
    t = 0.0
    dt = 1.0 / hz

    # simulate gaze with dwell periods (stable) and saccades (fast movement)
    cx, cy = 500.0, 400.0
    x, y = cx, cy

    dwell_duration = 0
    in_saccade = False
    saccade_frames = 0

    for i in range(n):
        # state machine: dwell for a while, then saccade to new target
        if not in_saccade:
            dwell_duration += 1
            # after dwelling, occasionally saccade
            # vary saccade timing to create some short and some long gaps
            if dwell_duration > 20 and random.random() < 0.05:
                cx = random.uniform(200, 800)
                cy = random.uniform(200, 600)
                in_saccade = True
                saccade_frames = 0
                dwell_duration = 0

        if in_saccade:
            # quick movement toward target (takes ~5-8 frames)
            x += (cx - x) * 0.4
            y += (cy - y) * 0.4
            saccade_frames += 1
            if saccade_frames > 3 and abs(x - cx) < 3 and abs(y - cy) < 3:
                in_saccade = False
                x, y = cx, cy
        else:
            # dwell: very small jitter around target
            x = cx + random.gauss(0, 0.2)
            y = cy + random.gauss(0, 0.2)

        # rare dropout (don't break stable streaks too often)
        valid = random.random() > 0.005

        # small timing jitter
        jitter = random.gauss(0, dt * 0.02)
        samples.append((t + jitter, x, y, valid))
        t += dt

    return samples


def compute_velocity(samples, idx):
    """Compute gaze velocity at given index."""
    if idx < 1:
        return 0.0
    t0, x0, y0, _ = samples[idx - 1]
    t1, x1, y1, _ = samples[idx]
    dt = t1 - t0
    if dt <= 0:
        return 999.0  # invalid
    dist = math.sqrt((x1 - x0)**2 + (y1 - y0)**2)
    return dist / dt


class GazeClickDetector:
    def __init__(self):
        self.last_click_time = None
        self.stable_count = 0
        self.was_intent = False

    def should_emit_click(self, t):
        """Check if enough time has passed since last click."""
        if self.last_click_time is None:
            return True
        elapsed_ms = (t - self.last_click_time) * 1000
        if elapsed_ms < MIN_CLICK_INTERVAL_MS / 1000:
            return False
        return True

    def process_sample(self, t, x, y, valid, velocity):
        """
        Process one gaze sample.
        Returns click time if a click should be emitted, None otherwise.
        """
        if not valid:
            self.stable_count = 0
            self.was_intent = False
            return None

        # check stability
        is_stable = velocity < STABILITY_THRESHOLD

        if is_stable:
            self.stable_count += 1
        else:
            self.stable_count = 0
            self.was_intent = False

        # detect intent (stable for enough frames)
        has_intent = self.stable_count >= STABLE_FRAMES_REQUIRED

        # emit click on rising edge of intent
        if has_intent and not self.was_intent:
            self.was_intent = True
            if self.should_emit_click(t):
                self.last_click_time = t
                return t

        if not has_intent:
            self.was_intent = False

        return None


def run_pipeline(samples):
    """Run click detection on samples, return list of click timestamps."""
    detector = GazeClickDetector()
    clicks = []

    for i, (t, x, y, valid) in enumerate(samples):
        vel = compute_velocity(samples, i)
        click_t = detector.process_sample(t, x, y, valid, vel)
        if click_t is not None:
            clicks.append(click_t)

    return clicks


def main():
    samples = generate_samples()
    clicks = run_pipeline(samples)

    print(f"Generated {len(samples)} samples")
    print(f"Detected {len(clicks)} clicks:")

    for i, t in enumerate(clicks):
        delta = ""
        if i > 0:
            gap_ms = (t - clicks[i-1]) * 1000
            delta = f"  (gap: {gap_ms:.1f}ms)"
            if gap_ms < MIN_CLICK_INTERVAL_MS:
                delta += " ** VIOLATION **"
        print(f"  Click {i+1}: t={t:.4f}s{delta}")


if __name__ == "__main__":
    main()

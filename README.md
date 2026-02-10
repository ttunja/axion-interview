# Gaze-to-Click Debug Task

15 min timebox.

## What's broken

We have a click-detection pipeline that watches gaze stability and fires a CLICK event when the user dwells. Problem: it's double-clicking. Two CLICKs appear ~120ms apart sometimes.

Rule: minimum 300ms between clicks.

## Your job

1. `python -m unittest -v` — watch it fail
2. Find the bug, fix it
3. Test should pass afterward
4. Tell me what went wrong

## Ground rules

- stdlib only, no pip
- IDE + docs are fine
- AI: okay for "what does X mean" type questions, not okay for writing your fix or test. Tell me if you use it.

## Running it

```
python -m unittest -v      # tests
python main.py             # prints click timestamps for manual inspection
```

Python 3.11. If you want conda: `conda env create -f env.yml && conda activate bci_debug_interview`

# Gaze-to-Click Debug Task

15-20 min timebox.

## What's broken

We have a click-detection pipeline that watches gaze stability and fires a CLICK event when the user dwells. Problem: it's double-clicking. Two CLICKs appear less than 300ms apart sometimes.

Rule: minimum 300ms between clicks.

There are two bugs to find — one straightforward, one requires tracing the logic.

## Your job

1. `python -m unittest -v` — watch it fail
2. Find the bugs, fix them
3. Test should pass afterward
4. Explain what went wrong

## Ground rules

- stdlib only, no pip
- IDE + docs are fine
- Share your screen
- No AI tools (GitHub Copilot, ChatGPT, Claude, etc.) — this tests your debugging skills, not prompting skills.

## Running it

```
python -m unittest -v      # tests
python main.py             # prints click timestamps for manual inspection
```

Python 3.6+. If you want conda: `conda env create -f env.yml && conda activate bci_debug_interview`

# Voice Clone — one voice, every video (F5-TTS)

A faceless channel lives or dies on its narrator. Clone ONE voice, keep
it forever, and the channel sounds like a person instead of a tool.

## The consent rule (non-negotiable)
Clone **only**:
- your own voice, or
- a synthetic AI voice that already narrates your own videos.

**Never clone a real person's voice** — not a celebrity, not a
competitor, not a politician. Besides the ethics, platforms ban it, and
one ban ends the channel. Always post with the AI-generated-content
label ON.

## Setup
F5-TTS is its own project (MIT) — install it, don't vendor it:
https://github.com/SWivid/F5-TTS

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install f5-tts
```

You need two reference files:
- `ref.wav` — 5–15 seconds (up to ~30s works) of clean, single-speaker
  audio in the target voice. Pull it from your own best-performing
  video's narration.
- `ref.txt` — the EXACT transcript of that clip. Mismatched transcripts
  are the #1 cause of garbled clones.

## Generation — chunked, or don't bother
A single call for a full 130–160-word narration drifts and stalls.
Split the script into sentence chunks (~15–25 words), generate each,
and join with tight silence trimming so the narration runs continuous:

```bash
f5-tts_infer-cli --model F5TTS_v1_Base \
  --ref_audio ref.wav --ref_text "$(cat ref.txt)" \
  --gen_text "One chunk of the script." \
  --output_file chunk_01.wav
```

`clone_batch.py` (this folder) does exactly this: reads a script file,
chunks it, skips chunks that already exist (safe to re-run after a
crash), and concatenates the result.

## Timing reality (CPU)
On a modest CPU-only box, budget roughly **2 hours per 3 narrations**
(~35s each). Generate batches ahead of time — overnight — and never
let voice generation sit on the posting critical path. A GPU changes
this completely (minutes), but is not required.

## Pace
Keep the clone at its natural speed for story content. The commentary
lane on the reference channel runs a hair slower (ffmpeg `atempo=0.95`)
for gravitas — test both, let retention decide, and write down the
winner so it stays consistent.

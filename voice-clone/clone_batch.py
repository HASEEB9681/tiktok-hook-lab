#!/usr/bin/env python3
"""clone_batch.py - chunked F5-TTS narration generation with resume.

Why chunked: one long F5-TTS call drifts and stalls; sentence-sized
chunks stay stable. Why resumable: on CPU a batch takes a long time, so
every finished chunk is kept - re-running after a crash or a night
continues where it stopped instead of starting over.

Requires: F5-TTS installed (pip install f5-tts) and ffmpeg on PATH.
See VOICE-CLONE.md for setup and the consent rule (your own voice, or a
synthetic voice from your own videos - never a real person's).

Usage:
    python3 clone_batch.py --script script.txt \
        --ref-audio ref.wav --ref-text ref.txt \
        --out narration.wav [--speed 1.0] [--workdir chunks]
"""
import argparse
import os
import re
import subprocess
import sys


def chunk_script(text: str, max_chars: int = 130):
    """Split into sentence chunks of at most ~max_chars."""
    sentences = re.split(r"(?<=[.!?])\s+", " ".join(text.split()))
    chunks, cur = [], ""
    for s in sentences:
        if cur and len(cur) + 1 + len(s) > max_chars:
            chunks.append(cur)
            cur = s
        else:
            cur = f"{cur} {s}".strip()
    if cur:
        chunks.append(cur)
    return chunks


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--script", required=True)
    ap.add_argument("--ref-audio", required=True)
    ap.add_argument("--ref-text", required=True, help="file containing the reference clip's exact transcript")
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="F5TTS_v1_Base")
    ap.add_argument("--speed", type=float, default=None)
    ap.add_argument("--workdir", default=None, help="chunk folder (default: <out>.chunks)")
    args = ap.parse_args()

    ref_text = open(args.ref_text).read().strip()
    script = open(args.script).read().strip()
    chunks = chunk_script(script)
    workdir = args.workdir or (args.out + ".chunks")
    os.makedirs(workdir, exist_ok=True)
    print(f"{len(chunks)} chunks -> {workdir}")

    wavs = []
    for i, ch in enumerate(chunks):
        name = f"chunk_{i:02d}.wav"
        path = os.path.join(workdir, name)
        wavs.append(path)
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            print(f"[{i+1}/{len(chunks)}] skip (exists)")
            continue
        cmd = [
            "f5-tts_infer-cli", "--model", args.model,
            "--ref_audio", args.ref_audio, "--ref_text", ref_text,
            "--gen_text", ch,
            "--output_dir", workdir, "--output_file", name,
            "--remove_silence",
        ]
        if args.speed:
            cmd += ["--speed", str(args.speed)]
        print(f"[{i+1}/{len(chunks)}] generating: {ch[:60]}...")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(path):
            print(r.stdout[-500:] + r.stderr[-500:], file=sys.stderr)
            print(f"chunk {i} failed - re-run to resume from here", file=sys.stderr)
            return 1

    # Join with the concat filter + aresample (the reliable path).
    inputs, filt = [], ""
    for i, w in enumerate(wavs):
        inputs += ["-i", w]
        filt += f"[{i}:a]"
    filt += f"concat=n={len(wavs)}:v=0:a=1,aresample=async=1[a]"
    r = subprocess.run(
        ["ffmpeg", "-v", "error", *inputs, "-filter_complex", filt,
         "-map", "[a]", "-ar", "24000", "-ac", "1", args.out],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print(r.stderr[-800:], file=sys.stderr)
        return 1
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

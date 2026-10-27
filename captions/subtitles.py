#!/usr/bin/env python3
"""Generate timed subtitles (SRT + karaoke ASS) for MPT video narrations.

Root cause it fixes: faster-whisper's model download crashes on this server
because some environments' no_proxy/NO_PROXY contain bracketed IPv6 entries
([::1]) that break httpx's default client factory
(httpx.InvalidURL: Invalid port: ':1]'). We sanitize those vars first.

Usage:
    python3 subtitles.py <audio.mp3> [out_basename]

Writes <out_basename>.srt and <out_basename>.ass (karaoke style, TikTok look).
"""
import os
import re
import sys

# --- sanitize proxy env before ANY import that builds an httpx client ---
os.environ["no_proxy"] = "localhost,127.0.0.1"
os.environ["NO_PROXY"] = "localhost,127.0.0.1"

from faster_whisper import WhisperModel  # noqa: E402

MODEL_SIZE = "base"  # cached at ~/.cache/huggingface/hub/models--Systran--faster-whisper-base


def fmt_srt(t: float) -> str:
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int((s % 1) * 1000):03d}"


def fmt_ass(t: float) -> str:
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):d}:{int(m):02d}:{int(s):02d}.{int((s % 1) * 100):02d}"


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chunk_words(words, max_words=7, max_dur=3.0):
    """Group words into caption cues: <=max_words and <=max_dur seconds each."""
    cues, cur = [], []
    for w in words:
        cur.append(w)
        dur = cur[-1].end - cur[0].start
        if len(cur) >= max_words or dur >= max_dur:
            cues.append(cur)
            cur = []
    if cur:
        cues.append(cur)
    return cues


def main():
    audio = sys.argv[1]
    base = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(audio)[0]
    srt_path = base + ".srt"
    ass_path = base + ".ass"

    print(f"[subtitles] loading whisper {MODEL_SIZE} ...", flush=True)
    model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        audio,
        beam_size=5,
        word_timestamps=True,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500),
    )
    print(f"[subtitles] language={info.language} ({info.language_probability:.2f})", flush=True)

    words = []
    for seg in segments:
        for w in seg.words or []:
            txt = w.word.strip()
            if txt:
                words.append(w)
    if not words:
        print("[subtitles] ERROR: no words transcribed")
        sys.exit(1)

    cues = chunk_words(words)

    # ---- SRT ----
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, cue in enumerate(cues, 1):
            f.write(f"{i}\n{fmt_srt(cue[0].start)} --> {fmt_srt(cue[-1].end)}\n"
                    f"{' '.join(w.word.strip() for w in cue)}\n\n")

    # ---- karaoke ASS (TikTok-style: bold white, black outline, bottom-center) ----
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: TikTok,Arial,72,&H00FFFFFF,&H0000FFFF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,0,2,60,60,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        for cue in cues:
            parts = []
            for w in cue:
                dur_cs = max(1, int(round((w.end - w.start) * 100)))
                parts.append(f"{{\\kf{dur_cs}}}{esc(w.word.strip())}")
            line = " ".join(parts)
            f.write(f"Dialogue: 0,{fmt_ass(cue[0].start)},{fmt_ass(cue[-1].end)},TikTok,,0,0,0,,{line}\n")

    print(f"[subtitles] wrote {srt_path} and {ass_path} ({len(cues)} cues)")


if __name__ == "__main__":
    main()

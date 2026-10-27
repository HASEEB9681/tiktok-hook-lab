# TikTok Hook Lab — The Complete Faceless Commentary System

**The full production system behind a real faceless TikTok commentary
channel** — hooks, scripts, a cloned voice, fresh stock footage,
karaoke captions, a QC gate, posting, and comment triage. Every tool
free, every step documented, nothing to sign up for except a free
Pixabay key.

This started as just the hook system. It is now the whole pipeline,
published the way it actually runs in production.

---

## The system at a glance

```
topic → fact-check → script → HOOK LAB → voice clone → fresh footage
      → assemble → karaoke captions → QC GATE → post → comment triage
      → stats → learn → (next topic)
```

| Part | What it does | Where |
|---|---|---|
| 🎣 **Hook Lab** | 3+ hooks off rotated formulas, scored on 5 properties; the weakest gets fixed before production | `SKILL.md` + `hook_check.py` |
| 🎬 **Pipeline** | The end-to-end workflow: winner script structure, assembly rules, posting cadence | `pipeline/` |
| 🎙️ **Voice Clone** | One cloned narrator voice (F5-TTS), chunked + resumable generation | `voice-clone/` |
| 🎞️ **Footage** | Fresh Pixabay clips per beat, hash-deduped so a clip is never reused | `footage/` |
| 💬 **Captions** | Word-timed karaoke captions (SRT + ASS) from the finished narration | `captions/` |
| ✅ **QC Gate** | The pre-post checklist — incl. the narration-tail check that catches silent TTS cuts | `qc/` |
| 📌 **Comment Triage** | Pin / reply / skip / owner-flagged piles for scheduled reply passes | `SKILL.md` part B |

## Quick start (in production order)

1. **Hooks first.** `python3 hook_check.py --hook "your opening line"` —
   see the 5-property panel. Rule #1: *stakes must never be the weakest
   property.*
2. **Write the script** to the winner structure in
   `pipeline/PIPELINE.md` (question → beats → CTA → CAPS bait → close).
3. **Clone the voice** — `voice-clone/` (your own voice or your own
   videos' synthetic voice only; never a real person's).
4. **Fetch footage** — `footage/pixabay_fetch.py` with your own free
   Pixabay key; it skips every clip you have ever used.
5. **Assemble + caption** — normalize clips, concat-filter join
   (`pipeline/assemble_example.sh`), then `captions/subtitles.py`.
6. **Run the QC gate** (`qc/QC-CHECKLIST.md`). Nothing posts without it.
7. **Post, then triage comments** (`SKILL.md` part B) — pin the best
   viewer comment, reply human, keep flagged ones for a human.

## The honest part

**Scores are checklists, not predictors.** On the channel this runs on,
the proven best-performing hook scores *low* on generic calibrations —
a low panel never rejects a hook, a high one never promises anything.
What the system genuinely does: it catches the one dead property in a
hook before you waste a production cycle, keeps every video's footage
fresh, keeps the voice identical, and makes sure no video ever posts
with its ending silently cut off.

Other things the channel's data taught us (all in the docs): comments
follow topic heat + a personal question, not bait length; loss framing
beats gain framing; early stats lie — judge at 48h+.

## Stack & credits

This system orchestrates excellent open-source projects — install them
from their own repos (all MIT):

- [F5-TTS](https://github.com/SWivid/F5-TTS) — the voice clone engine
- [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) —
  optional rough-cut assembly
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) — caption
  transcription
- [Pixabay](https://pixabay.com/api/docs/) — stock footage (free API key)
- Hook formulas + scoring concepts adapted from
  [youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill)
  by Jake Schincariol (MIT; upstream license in `UPSTREAM-LICENSE.txt`)

Original to this repo: the lane calibration + mandatory stakes rule,
the triage-and-pin system, the footage dedupe tool, the chunked clone
runner, the QC gate, and every workflow doc.

## Install as an agent skill

```bash
git clone https://github.com/HASEEB9681/tiktok-hook-lab.git
cp -r tiktok-hook-lab ~/.claude/skills/   # or your agent's skills folder
```
Or paste `SKILL.md` into any chat to run the method without the tools.

## License

MIT — use it, change it, ship it. See `LICENSE`.

# The Pipeline — one video, end to end

How one faceless commentary video is made on the channel this system was
built for. Every step names the tool used; everything here is free.

```
topic → fact-check → script → HOOK LAB → voice → footage → assemble
      → captions → QC gate → post → comment triage → stats → learn
```

## 1. Topic & fact-check
Pick topics your audience feels in their pocket: bills, checks, deadlines,
prices, scams. Before scripting, verify the load-bearing facts at primary
sources (agency sites, official releases). Write opinion as opinion —
never state that a proposed law passed or a tax ended when it didn't.
Your credibility is the whole channel.

## 2. Script — the winner structure
130–160 words for a ~35-second video:

1. **Opening question** (the hook — see step 3)
2. **Argument beats** — one fact or grievance per beat, each beat is also
   one visual (step 5 plans visuals per beat, not per video)
3. **CTA** — "Tap the heart, press the plus, and share this"
4. **Comment bait in CAPS** — a short phrase viewers type back (a word or
   a two-sided choice: GOT IT / STILL WAITING). Topic heat matters more
   than bait length.
5. **Rallying close** — one warm line that lands the emotion

## 3. Hook Lab (before anything is produced)
Draft 3+ hooks off different formulas, run `../hook_check.py`, fix the
weakest property — **stakes must never be the dead property** — then
record which formula won. Full method: `../SKILL.md` part A.

## 4. Voice
Clone ONE voice and keep it forever — voice consistency is channel
identity. F5-TTS, chunked generation, tight silence trimming so
narration runs continuous. Full setup: `../voice-clone/VOICE-CLONE.md`.
Consent rule: only your own voice, or a synthetic AI voice from your own
videos. Never a real person's voice.

## 5. Footage
Beat-matched stock clips from Pixabay (free API key), one fresh clip per
beat, **never reuse a clip across videos** — the tool in `../footage/`
dedupes by file hash against everything you have used before. Subjects
and era must match the narration (a USA seniors channel shows American
seniors; a 70s story looks like the 70s).

## 6. Assembly
ffmpeg. Two hard-won rules:
- **Normalize every clip first** (1080×1920, 30fps, yuv420p) — mixed
  frame rates are the #1 cause of broken concatenations.
- **Join with the concat filter + aresample**, not the concat demuxer.
See `assemble_example.sh`.

A stock-assembly tool like
[MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) can
draft the rough cut (its own project, MIT — install it separately), but
plan on a manual ffmpeg finish for beat-accurate work.

## 7. Captions
Word-timed karaoke captions (the spoken word highlighted), generated
from the finished narration with faster-whisper: `../captions/`.
PLUS the hook text burned in for the first ~3.5 seconds. One warning
from production: whisper sometimes mis-hears ALL-CAPS bait phrases —
proofread the caption text against the script before burn-in.

## 8. QC gate — nothing posts without it
`../qc/QC-CHECKLIST.md`. The headline rule: **transcribe the narration's
last seconds and compare against the script** — TTS can silently cut
the final line, and no automated "looks fine" check catches it. A human
(or the producing agent) personally views the hook frame and the end
frame of every video.

## 9. Post & engage
Stagger posts, don't dump a batch at once. Label AI-generated content
(the platform toggle) on every post. Then run comment triage
(`../SKILL.md` part B): reply within the first hours, pin the best
viewer comment, keep owner-flagged comments for a human decision.

## 10. Stats & learn
Log every post (plays / likes / comments / shares) and read at 48h+ —
early reads lie. When something outperforms, name WHY in one line and
feed it back into step 1. On the reference channel, the pattern that
emerged: concrete pocketbook grievances beat everything else, loss
framing beats gain framing, and comments follow topic heat + a personal
question — not bait length.

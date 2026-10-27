# QC Checklist — run on EVERY video before it posts

No video skips this gate. Most items take under two minutes; the first
one has saved more videos than all the others combined.

## Audio
- [ ] **Narration tail verified by transcription.** Transcribe the last
      ~10 seconds and compare word-for-word with the script's final
      line. TTS pipelines can silently cut the ending — this is the
      single most-missed defect in faceless production. Never accept
      another tool's (or agent's) "QC passed" for this; check it
      yourself.
- [ ] No long silences inside the narration (tight-trimmed, continuous).
- [ ] Voice is the channel's one cloned voice; speed matches the lane's
      setting.

## Video
- [ ] Hook frame (0–1s): hook text readable, bold, upper third; first
      visual matches the first spoken words.
- [ ] Every beat's visual matches what is being said at that moment.
- [ ] All clips are FRESH (hash-checked against the used registry —
      zero repeats from any earlier video).
- [ ] Subjects/era match the topic and audience.
- [ ] Visual changes every ~2–4 seconds; no frozen or black frames.
- [ ] End frame: the rallying close + comment bait land on screen.
- [ ] Specs: 1080×1920, 30fps, yuv420p, faststart (moov atom first).

## Captions
- [ ] Karaoke captions present and in sync; spoken word highlighted.
- [ ] Caption text proofread against the script — especially ALL-CAPS
      bait phrases, which speech recognition loves to mis-hear.

## Facts & framing
- [ ] Every load-bearing number traces to a primary source checked
      today (agency release, official page).
- [ ] Opinion is framed as opinion. No claim that a bill passed, a tax
      ended, or a payment is guaranteed unless it verifiably did.
- [ ] Where a public figure is named in the hook, the connection to
      their actual stated position is real — never forced.

## Post settings
- [ ] AI-generated-content label ON.
- [ ] Visibility: Everyone (public) — re-check after posting; posts can
      silently land as private.
- [ ] Caption/description copied exactly from the approved text,
      comment bait included.

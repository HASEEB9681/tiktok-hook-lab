# Footage rules (Pixabay)

The footage half of the pipeline. Tool: `pixabay_fetch.py` (this folder).

1. **Fresh clips only — forever.** Every clip is used in exactly ONE
   video. The fetcher records each clip's md5 in a registry and skips
   anything seen before. Viewers notice repeats; algorithms do too.
2. **One clip per narration beat.** Search per beat, not per video: a
   beat about a heating bill wants a boiler/thermostat/window-frost
   clip, not a generic "senior smiling" clip.
3. **Subjects must match the audience.** A USA seniors channel shows
   American-looking seniors in American-looking homes. An era story
   (70s/80s) needs era-plausible clothes, cars and rooms — or a shot
   tight enough that the era never shows.
4. **Vertical first.** The tool prefers height ≥ width variants; the
   assembler crop-fills the rest (see `../pipeline/`).
5. **Your own key, always.** Pixabay keys are free at
   https://pixabay.com/api/docs/ — quota is per account, so a shared
   key is a dead key. Never commit a key to git; pass it via the
   `PIXABAY_API_KEY` environment variable.
6. **Respect the license.** Pixabay content is free to use under the
   Pixabay Content License; don't sell the raw clips themselves, and
   don't use footage to imply endorsement by the people shown.

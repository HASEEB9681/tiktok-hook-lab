---
name: tiktok_hook_lab
description: >-
  Hook Lab + Comment Triage for faceless TikTok commentary channels: write
  several hook options off rotated formulas, run them through a 5-property
  checklist (hook_check.py) to fix the weakest property before production, and
  triage post comments into pin / reply / skip / owner-flagged piles. Use when
  scripting short-form commentary videos, doing hook QC, or running comment
  reply passes.
---

# TikTok Hook Lab + Comment Triage

Built for faceless short-form commentary channels (news, seniors/retiree
topics, money, local issues) with a proven structure: opening question →
argument beats → CTA → comment-bait phrase → rallying close. Two parts:
**A. Hook Lab** (before production) and **B. Comment Triage & Pin** (after
posting).

## A. Hook Lab

### A1. Write options, rotate formulas
For each video, draft **at least 3 hook options** using DIFFERENT formulas —
never three rewordings of the same shape. Rotate across the week so the
channel does not sound like one repeated question.

| Formula | Example (seniors/retiree commentary) |
|---|---|
| The Question (proven winner shape) | "Do you agree with President Trump when he says retired Americans shouldn't be paying taxes anymore?" |
| The Deadline | "December 7 is the last day to fix your Medicare plan for 2027." |
| The Warning | "If that Medicare letter is still unopened, January will surprise you." |
| The Mistake | "The biggest mistake retirees make every fall? Doing nothing." |
| The Statistic | "Only 23% of seniors say the COLA raise actually keeps up." (only with a verified figure) |
| Before and After | "Same house. Same check. But the tax bill doubled." |
| The Comparison | "The same pill costs less in other countries. Why do Americans pay more?" |
| The Direct Address | "If you're retired, your plan already changed. Did you check how?" |
| The Reveal | "Your plan sent the letter weeks ago. It told you exactly what changed." |
| The Receipt | Open on the bill/letter itself as the visual. |

Rarely fits faceless commentary (talking-head/creator formulas): I Tried It,
Someone Else's Result, The Teardown, The Superlative, The Origin — skip
unless a topic genuinely carries them.

### A2. Run the checklist — fix the weakest property
```bash
python3 hook_check.py hooks.txt              # one hook per line, ranked
python3 hook_check.py --hook "one line"      # check a single hook
```
Five properties (0–100): SPECIFICITY (a number, name or date beats an
adjective), ADDRESS ("you/your" early, or the group named — retirees,
seniors, veterans), STAKES (the cost of doing nothing, in the audience's
words: bill, check, rent, letter, plan, price, wait), CURIOSITY (an open
gap; a hook that answers itself is closed — cut the resolving half),
BREVITY (9–24 words for a spoken opening).

**How to use the score — read this twice:**
- The score is a **checklist, never a gate**. A channel's proven
  best-performing hook can score low on a generic calibration; a low total
  alone NEVER rejects a hook, and a high total is never a promise.
- The one hard rule (learned in production: hooks kept shipping with the
  stakes missing): **STAKES must not be the weakest property.** If it is,
  add one stakes phrase — the loss, the deadline, or the check that avoids
  it — and re-run. Same for any other property under ~30: fix that one
  thing, don't rewrite the whole hook.
- Pick the option whose weakest property is strongest after fixes, and note
  the winning formula so rotation stays honest across the week.

### A3. Hook text on screen
The spoken opening and the burned-in hook text (first ~3.5s, bold, upper
third) are the same promise in two forms — keep them aligned; if they
diverge, the shorter on-screen line still has to carry the stakes word.

## B. Comment Triage & Pin

Sort every new comment into four piles, in this order:

1. **OWNER-FLAGGED — hands off.** Complaints about the channel itself,
   business offers, heavy abuse, political rants aimed at the channel. Do
   NOT reply, do NOT heart, do NOT pin. Leave untouched for the owner's
   decision. If a comment has been explicitly held for the owner, no
   automated pass may answer it — ever.
2. **PIN — at most ONE per post.** Pin the single best eligible viewer
   comment when the post has no pinned comment yet. Preference: (a) a
   comment that answers the post's comment-bait, (b) a short personal
   story. A viewer's own words pinned on top is social proof for the next
   viewer. Never pin spam, an owner-flagged comment, or the channel's own
   comment; never replace an existing pin.
3. **REPLY + HEART.** Every other genuine comment gets a human-sounding
   reply: mostly 3–12 words, react to what they said first, contractions,
   plain words; a question ending in at most 1 of 3 replies; an emoji
   rarely. Never argue, never promise anything, never mention automation.
4. **SKIP.** Spam, links, self-promo, hate — no reply, no heart, no pin.

What actually drives comments (learned from a real channel's data): topic
heat + a personal yes/no question — not the length of the bait phrase. A
multi-word bait on a hot topic out-comments a single-word bait on a cold
one, every time.

## Provenance
Concepts (hook formulas + 5-property scoring + weakest-link weighting +
comment triage) adapted from
https://github.com/Jakeschincariol/youtube-agent-skill (MIT License;
upstream license in UPSTREAM-LICENSE.txt, scorer adapted in hook_check.py).
This repo is a TikTok-commentary adaptation: different calibration, a
mandatory stakes rule, and a triage system built for scheduled reply passes
on a faceless channel.

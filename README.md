# TikTok Hook Lab + Comment Triage

**An AI-agent skill for faceless TikTok commentary channels.**
Write better hooks, fix them before you produce, and run your comment
section like a system instead of a chore.

Free, MIT, no signup, no API key, nothing to connect. The one tool
(`hook_check.py`) runs on a clean Python 3 with zero dependencies.

---

## What it does

### 🎣 Hook Lab
Most short-form channels write **one** hook and ship it. This skill makes
your agent write **at least three**, each off a different formula
(The Question, The Deadline, The Warning, The Mistake, The Statistic,
Before and After, The Comparison, The Direct Address, The Reveal,
The Receipt) — then runs them through a 5-property checklist:

| Property | What it catches |
|---|---|
| **Specificity** | Adjectives where a number, name or date should be |
| **Address** | A hook that never says "you" or names its audience |
| **Stakes** | A hook that never says what doing nothing costs |
| **Curiosity** | A hook that answers its own question and leaves no gap |
| **Brevity** | A spoken opening that runs out of breath (aim: 9–24 words) |

The verdict weights the **weakest property at 40%** — a hook leaks exactly
where it's weakest, and averaging hides that.

```bash
python3 hook_check.py --hook "Why should sixty-five no longer mean retired?"
```
```
  Why should sixty-five no longer mean retired?
    SPECIFICITY   34
    ADDRESS       26
    STAKES        22
    CURIOSITY     59
    BREVITY       89
    PANEL         36  (checklist only - never a pass/fail)
    formula      The Question
    weakest      STAKES - name the cost: the bill, the check, the deadline
    HOUSE RULE   STAKES is the weakest property - add one stakes phrase
```

### 💬 Comment Triage & Pin
Every comment lands in one of four piles — **owner-flagged** (hands off,
never auto-answer), **pin** (one best viewer comment per post: social
proof), **reply + heart** (short, human, react-first), **skip** (spam).
Built for channels that reply on a schedule and can't afford one wrong
automated reply.

## The honest part

**The score is a checklist, not a predictor.** On the real channel this
was built for, the proven best-performing hook scores *low* on generic
calibrations. A low score is a reason to look again — never a rejection;
a high score is never a promise. What the panel is genuinely good at is
finding the one dead property in a hook before you waste a production
cycle on it. On that channel, it caught a pattern nobody had noticed:
**every hook was missing the stakes.**

And what actually drives comments, from the same channel's data: topic
heat + a personal yes/no question — not how long your comment-bait
phrase is.

## Install

For any agent that reads skill files (Claude Code, Muse, or similar):

```bash
git clone https://github.com/<your-username>/tiktok-hook-lab.git
cp -r tiktok-hook-lab ~/.claude/skills/   # or your agent's skills folder
```

No Claude skills setup? Paste `SKILL.md` at the top of a chat and it runs
as a mode — you keep everything except the scorer tool.

## Files

- `SKILL.md` — the full system (Hook Lab + Comment Triage)
- `hook_check.py` — the 5-property hook checklist scorer (zero dependencies)
- `UPSTREAM-LICENSE.txt` — upstream MIT license (see Credits)

## Credits

Hook formulas, the 5-property scoring idea and weakest-link weighting were
adapted from [youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill)
by Jake Schincariol (MIT). This project re-calibrates them for TikTok
commentary, adds the mandatory stakes rule, and adds the comment
triage-and-pin system.

## License

MIT — use it, change it, ship it. See `LICENSE`.

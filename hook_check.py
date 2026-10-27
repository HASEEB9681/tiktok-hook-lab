#!/usr/bin/env python3
"""hook_check.py - TikTok hook checklist scorer for commentary channels.

Adapted from hookscore.py in Jakeschincariol/youtube-agent-skill
(MIT License, see UPSTREAM-LICENSE.txt). Changes vs upstream:
- STAKES word list widened for a seniors/retiree audience (bill, check, rent,
  plan, letter, medicine, doctor, price, tax, wait...).
- Output is a CHECKLIST, not a verdict of quality: a real channel's proven
  best-performing hook ("Do you agree with President Trump when he says
  retired Americans shouldn't be paying taxes anymore?") scores low on the
  upstream YouTube calibration, so a low total NEVER rejects a hook by
  itself. The panel's job is to expose the weakest property so it can be
  fixed before production.
- Mandatory check: STAKES must not be the dead property. A hook that names
  no cost, loss, deadline or check is sent back for one stakes phrase.

Five properties, 0-100 each. Panel score = 60% mean + 40% weakest link (upstream
design: a hook leaks at its weakest property, and averaging hides that).

    python3 hook_check.py hooks.txt            # one hook per line, ranked
    python3 hook_check.py --hook "one line"    # check a single hook
"""
import re, sys

FILLER = {"basically", "actually", "literally", "just", "really", "very", "so", "kind", "sort", "like",
          "guys", "hey", "welcome", "today", "video", "subscribe", "channel"}
VAGUE = {"amazing", "incredible", "insane", "crazy", "huge", "massive", "game", "changer", "secret",
         "powerful", "ultimate", "best", "revolutionary", "mind", "blowing", "unbelievable"}
CONCRETE = re.compile(r"(\d[\d,.]*\s?(%|k|m|x)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?)", re.I)
YOU = re.compile(r"\b(you|your|you're|youre|yourself)\b", re.I)
GROUP = re.compile(r"\b(retirees?|seniors?|americans?|veterans?|workers?|homeowners?)\b", re.I)
STAKE = re.compile(r"\b(lose|lost|losing|wasting|waste|quit|fail|broke|cost|costs|risk|before|stop|never|"
                   r"die|dying|dead|bill|bills|rent|tax|taxes|price|prices|premium|check|checks|letter|"
                   r"plan|plans|medicine|doctor|doctors|wait|waiting|stuck|shrinks?|grows?|climb|rising|"
                   r"rose|cut|cuts|gone|miss|missed|deadline|runs out)\b", re.I)
CURIOSITY = re.compile(r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason)\b", re.I)

FORMULAS = [
    ("The Question", r"\?"),
    ("The Statistic", r"\d"),
    ("The Deadline", r"(last day|deadline|until|runs out)"),
    ("The Warning", r"(warning|careful|stop|never|if you)"),
    ("The Mistake", r"(mistake|wrong|error)"),
    ("Before and After", r"(used to|anymore)"),
    ("The Comparison", r"(more than|less than|cheaper|higher|lower|pay more)"),
    ("The Direct Address", r"^(if you|retirees|seniors|veterans)"),
    ("The Reveal", r"(already|sent|told you|behind|nobody told)"),
]

def words(t):
    return re.findall(r"[a-z0-9'%$.]+", t.lower())

def specificity(t):
    w = words(t)
    if not w:
        return 0
    nums = len(CONCRETE.findall(t))
    vague = sum(1 for x in w if x in VAGUE)
    filler = sum(1 for x in w if x in FILLER)
    s = 34 + nums * 22 - vague * 16 - filler * 5
    s += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    return max(0, min(100, s))

def address(t):
    n = len(YOU.findall(t))
    first = 30 if YOU.search(" ".join(t.split()[:6])) else 0
    g = 20 if GROUP.search(t) else 0
    return max(0, min(100, 26 + n * 20 + first + g))

def stakes(t):
    n = len(STAKE.findall(t))
    return max(0, min(100, 22 + n * 26 + (14 if CONCRETE.search(t) else 0)))

def curiosity(t):
    n = len(CURIOSITY.findall(t))
    q = 18 if t.strip().endswith("?") else 0
    closed = -18 if re.search(r"\b(because|so that|which means)\b", t, re.I) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))

def brevity(t):
    n = len(words(t))
    if n == 0:
        return 0
    if 9 <= n <= 24:
        return 100
    if n < 9:
        return max(30, 100 - (9 - n) * 11)
    return max(10, 100 - (n - 24) * 7)

PROPS = [("SPECIFICITY", specificity), ("ADDRESS", address), ("STAKES", stakes),
         ("CURIOSITY", curiosity), ("BREVITY", brevity)]

FIX = {
    "SPECIFICITY": "swap one adjective for a number, a name or a date",
    "ADDRESS": "say 'you' in the first six words, or name the group (retirees, seniors, veterans)",
    "STAKES": "name the cost: the bill, the check, the deadline - what doing nothing loses them",
    "CURIOSITY": "cut the half of the sentence that answers itself",
    "BREVITY": "9 to 24 words. Read it out loud and stop where you run out of breath",
}

def classify(t):
    best, hits = None, 0
    for name, pat in FORMULAS:
        n = 1 if re.search(pat, t, re.I) else 0
        if n > hits:
            best, hits = name, n
    return best or "Unclassified"

def score(t):
    parts = {n: fn(t) for n, fn in PROPS}
    vals = list(parts.values())
    panel = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    return parts, panel

def report(t):
    parts, panel = score(t)
    print(f"\n  {t.strip()}")
    for k, v in parts.items():
        print(f"    {k:<12} {v:3d}  {'#' * (v // 5)}")
    print(f"    {'PANEL':<12} {panel:3d}  (checklist only - never a pass/fail)")
    low = min(parts, key=parts.get)
    print(f"    formula      {classify(t)}")
    print(f"    weakest      {low} - {FIX[low]}")
    if low == "STAKES":
        print("    HOUSE RULE   STAKES is the weakest property - add one stakes phrase before production.")
    return panel

def main():
    a = sys.argv[1:]
    if "--hook" in a:
        lines = [a[a.index("--hook") + 1]]
    elif a:
        lines = [l for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__)
        sys.exit(1)
    scored = [(report(t), t) for t in lines]
    if len(scored) > 1:
        scored.sort(key=lambda r: -r[0])
        print(f"\n  strongest panel: {scored[0][1].strip()}  ({scored[0][0]})\n")

if __name__ == "__main__":
    main()

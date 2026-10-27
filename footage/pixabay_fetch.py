#!/usr/bin/env python3
"""pixabay_fetch.py - fetch fresh stock clips from Pixabay, deduped by hash.

Built for a daily faceless-video pipeline with one golden rule:
NEVER reuse a clip across videos. Every downloaded clip's md5 is recorded
in a registry file; anything already in the registry is skipped forever.

Setup:
    Get a FREE key at https://pixabay.com/api/docs/ (your own key -
    never share keys; quota is per-account), then:
        export PIXABAY_API_KEY="your-key"

Usage:
    python3 pixabay_fetch.py --out ./clips --per-term 4 \
        --query "senior couple kitchen" --query "retiree paying bills"

Behaviour:
- Prefers vertical clips (height >= width), largest file first.
- Skips clips already in <out>/../used_hashes.txt (the registry lives
  next to the output folder so one registry can serve many batches:
  pass --registry PATH to control it).
- Prints what it saved and what it skipped, and why.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request

API = "https://pixabay.com/api/videos/"


def api_get(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "pixabay-fetch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def best_file(hit: dict):
    """Pick the largest vertical file variant, else the largest overall."""
    variants = sorted(
        hit.get("videos", {}).values(),
        key=lambda v: v.get("width", 0) * v.get("height", 0),
        reverse=True,
    )
    for v in variants:
        if v.get("height", 0) >= v.get("width", 0) and v.get("url"):
            return v
    return variants[0] if variants else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--query", action="append", required=True, help="search term (repeatable)")
    ap.add_argument("--per-term", type=int, default=4, help="clips to keep per query (default 4)")
    ap.add_argument("--out", required=True, help="output folder for clips")
    ap.add_argument("--registry", default=None, help="used-hash registry file (default: <out>/../used_hashes.txt)")
    ap.add_argument("--min-duration", type=int, default=3, help="skip clips shorter than N seconds")
    args = ap.parse_args()

    key = os.environ.get("PIXABAY_API_KEY", "").strip()
    if not key:
        print("ERROR: set PIXABAY_API_KEY first (free key: https://pixabay.com/api/docs/)", file=sys.stderr)
        return 2

    os.makedirs(args.out, exist_ok=True)
    registry = args.registry or os.path.join(os.path.dirname(os.path.abspath(args.out)), "used_hashes.txt")
    used = set()
    if os.path.exists(registry):
        used = {ln.strip() for ln in open(registry) if ln.strip()}

    saved = skipped = 0
    reg = open(registry, "a")
    for q in args.query:
        params = urllib.parse.urlencode(
            {"key": key, "q": q, "video_type": "film", "per_page": 30, "safesearch": "true"}
        )
        try:
            data = api_get(f"{API}?{params}")
        except Exception as e:  # network/API errors: report, keep going
            print(f"[{q}] API error: {e}")
            continue
        kept = 0
        for hit in data.get("hits", []):
            if kept >= args.per_term:
                break
            if hit.get("duration", 0) < args.min_duration:
                continue
            v = best_file(hit)
            if not v:
                continue
            try:
                req = urllib.request.Request(v["url"], headers={"User-Agent": "pixabay-fetch/1.0"})
                blob = urllib.request.urlopen(req, timeout=60).read()
            except Exception as e:
                print(f"[{q}] download failed for id {hit.get('id')}: {e}")
                continue
            h = hashlib.md5(blob).hexdigest()
            if h in used:
                skipped += 1
                continue
            name = f"pixabay_{hit['id']}_{h[:8]}.mp4"
            with open(os.path.join(args.out, name), "wb") as f:
                f.write(blob)
            used.add(h)
            reg.write(h + "\n"); reg.flush()
            saved += 1; kept += 1
            print(f"[{q}] saved {name} ({v['width']}x{v['height']}, {hit.get('duration')}s)")
    reg.close()
    print(f"done: {saved} new clips saved, {skipped} duplicates skipped, registry: {registry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

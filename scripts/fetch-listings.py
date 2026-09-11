#!/usr/bin/env python3
"""Bean There QLD — listing/ticketing discovery adapters (review queue only).

Second discovery script alongside scripts/fetch-events.py. Fetches event and
venue-lead candidates from listing/ticketing sources and appends them ONLY to
data/candidates.json, the HUMAN REVIEW QUEUE. NOTHING here publishes into
data/activities.json: promotion is by human hand, one record at a time.

Sources (all evaluated 2026-09-12 for robots.txt / ToS / API availability):
  ticketmaster  Official Discovery API via the `ticketmaster` CLI
                (/opt/hatch/bin/ticketmaster, no user setup needed).
                Family-oriented keyword searches across Brisbane, Gold Coast
                and Sunshine Coast. Structured: name, date, venue + lat/lng,
                priceRanges, checkout URL. 18+ events filtered out.
  urbanlist     The Urban List — robots.txt explicitly allows crawling and
                publishes per-city sitemaps. Recently-updated Brisbane / Gold
                Coast / Sunshine Coast family & kids guide articles become
                *venue leads* (title + URL; a human verifies each venue).
  weekendnotes  WeekendNotes Brisbane category pages (family-friendly,
                festivals, markets, whats-on). No robots.txt served
                (default allow). Article title + URL + date snippet;
                a human verifies details from the article.

Deliberately excluded (see data/DATA_SOURCES.md for the full write-up):
  Time Out Brisbane, Concrete Playground — no public API; site terms
      restrict automated reproduction. Not scraped.
  Ticketek — no public discovery API and no self-serve affiliate program;
      data access is partnership-only via TEG. Not scraped.
  LADbible — viral news publisher; no family listings section. Unsuitable.
  Eventfinda — off-limits per Marcus (declined 2026-09-10).

Candidate records carry status "proposed" and are deduplicated by id
(source + source id), so re-runs only append genuinely new items.

Usage:
    python3 scripts/fetch-listings.py --source ticketmaster
    python3 scripts/fetch-listings.py --source urbanlist
    python3 scripts/fetch-listings.py --source weekendnotes
    python3 scripts/fetch-listings.py --all [--days 90] [--max 40]

Cron (weekly, run from the repo root):
    cd ~/workspace/bean-there-qld && python3 scripts/fetch-listings.py --all

The script prints a machine-readable JSON summary on stdout:
    {"sources": {"ticketmaster": {"status": "ok", "fetched": N, "new": M, ...}, ...},
     "total_new": T, "queue_total": Q}

Australian English throughout. Stdlib only.
"""

import json
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date, datetime, timedelta
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
QUEUE = DATA / "candidates.json"

TODAY = date.today()
UA = {"User-Agent": "BeanThereQLD-data-pipeline/1.0 (+review queue, weekly)"}

# ---------------------------------------------------------------------------
# Reuse the queue helpers and zone logic from the sibling scripts (single
# source of truth; these modules do not run anything on import).
# ---------------------------------------------------------------------------
import importlib.util as _ilu

def _load(name, path):
    spec = _ilu.spec_from_file_location(name, path)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_fe = _load("btq_fetch_events", ROOT / "scripts" / "fetch-events.py")
load_queue = _fe.load_queue
save_queue = _fe.save_queue
add_candidate = _fe.add_candidate
base_candidate = _fe.base_candidate
set_travel = _fe.set_travel
zone_for = _fe.zone_for


def fetch(url, timeout=45):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode("utf-8", "replace")


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return re.sub(r"-{2,}", "-", s) or "untitled"


def humanize_slug(s):
    return unescape(re.sub(r"[-_]+", " ", s)).strip().capitalize()


# ===========================================================================
# Source 1 — Ticketmaster Discovery API (official, via CLI)
# ===========================================================================
TM_CLI = "/opt/hatch/bin/ticketmaster"
TM_KEYWORDS = ["kids", "family", "Bluey", "circus", "puppet", "dinosaur"]
TM_KEEP_SEGMENTS = {"Arts & Theatre", "Family", "Miscellaneous"}
TM_18PLUS_RE = re.compile(r"18\+|over 18|adults only|no children", re.I)
# Gambling-adjacent events are out of scope for a family app, even when
# marketed as "family days".
TM_GAMBLING_RE = re.compile(r"\brace(day|ing)?\b|casino|poker|tab\b|punters?", re.I)
# The Discovery API's city= query is unreliable (misses venues in e.g.
# South Brisbane), so we search country-wide and filter stateCode == QLD
# client-side. Covers Brisbane, Gold Coast, Sunshine Coast, Ipswich, Logan,
# Toowoomba, Cairns, Townsville and everywhere else in Queensland.
TM_QLD_STATES = {"QLD"}


def _tm_search(keyword, start, end):
    cmd = [TM_CLI, "search-events", "--keyword", keyword,
           "--country-code", "AU",
           "--start-date", start.isoformat(), "--end-date", end.isoformat(),
           "--size", "40", "--sort", "date,asc"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        raise RuntimeError(f"ticketmaster CLI failed: {e}")
    if r.returncode != 0:
        raise RuntimeError(f"ticketmaster CLI exit {r.returncode}: {r.stderr[:200]}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"ticketmaster CLI returned non-JSON: {r.stdout[:200]}")


def _tm_family_ok(ev):
    """Keep family-suitable events; drop 18+ / adult-only / gambling ones."""
    blob = " ".join(str(ev.get(k) or "") for k in ("pleaseNote", "info", "name"))
    if TM_18PLUS_RE.search(blob) or TM_GAMBLING_RE.search(blob):
        return False
    for c in ev.get("classifications", []) or []:
        if c.get("family"):
            return True
        seg = (c.get("segment") or {}).get("name")
        if seg in TM_KEEP_SEGMENTS:
            return True
    return False


def _tm_price_note(ev):
    prs = ev.get("priceRanges") or []
    if not prs:
        return None
    try:
        mins = [(p.get("min"), p.get("currency", "AUD")) for p in prs
                if isinstance(p.get("min"), (int, float))]
    except Exception:
        return None
    if not mins:
        return None
    amt, cur = min(mins, key=lambda t: t[0])
    return f"Tickets from {cur} {amt:g} via Ticketmaster"


def _map_tm_event(ev):
    eid = ev.get("id")
    c = base_candidate("ticketmaster", f"cand-tm-{eid}",
                       str(ev.get("name") or "Untitled event").strip()[:140])
    c["url"] = ev.get("url") or None
    c["booking_url"] = ev.get("url") or None
    start = (ev.get("dates") or {}).get("start") or {}
    c["date"] = start.get("localDate") or None
    lt = start.get("localTime")
    c["when"] = f"{c['date']} {lt}" if c["date"] and lt else c["date"]
    venues = (ev.get("_embedded") or {}).get("venues") or []
    v = venues[0] if venues else {}
    c["venue"] = v.get("name") or None
    loc = v.get("location") or {}
    city = (v.get("city") or {}).get("name")
    try:
        set_travel(c, float(loc["latitude"]), float(loc["longitude"]),
                   region=city)
    except (KeyError, TypeError, ValueError):
        c["travel"]["region"] = city
    cls = []
    for cl in ev.get("classifications", []) or []:
        seg = (cl.get("segment") or {}).get("name")
        gen = (cl.get("genre") or {}).get("name")
        if seg and seg not in cls:
            cls.append(seg)
        if gen and gen not in cls:
            cls.append(gen)
    if cls:
        c["category_hint"] = ", ".join(cls[:3])
    c["price_note"] = _tm_price_note(ev)
    c["age_hint"] = "Check listing — family suitability varies by event"
    c["source"] = {"label": "Ticketmaster Discovery API",
                   "url": c["url"] or "https://www.ticketmaster.com.au"}
    return c


def _tm_qld_ok(ev):
    """Keep only events with a Queensland venue."""
    for v in (ev.get("_embedded") or {}).get("venues") or []:
        if ((v.get("state") or {}).get("stateCode") or "").upper() in TM_QLD_STATES:
            return True
    return False


def fetch_ticketmaster(days=90, max_candidates=200):
    start, end = TODAY, TODAY + timedelta(days=days)
    seen, out = set(), []
    calls = 0
    for kw in TM_KEYWORDS:
        data = _tm_search(kw, start, end)
        calls += 1
        for ev in (data.get("_embedded") or {}).get("events", []):
            eid = ev.get("id")
            if not eid or eid in seen:
                continue
            seen.add(eid)
            if not _tm_qld_ok(ev):
                continue
            if not _tm_family_ok(ev):
                continue
            out.append(_map_tm_event(ev))
            if len(out) >= max_candidates:
                break
        if len(out) >= max_candidates:
            break
        time.sleep(0.5)
    return out, {"api_calls": calls, "unique_events": len(seen)}


# ===========================================================================
# Source 2 — The Urban List sitemaps (crawling explicitly allowed)
# ===========================================================================
UL_SITEMAP = "https://www.theurbanlist.com/brisbane/sitemap"
UL_CITY_RE = re.compile(r"theurbanlist\.com/(brisbane|goldcoast|sunshinecoast)/", re.I)
UL_FAM_RE = re.compile(r"kid|famil|children|toddler|baby|babies|playground", re.I)
UL_CITY_LABEL = {"brisbane": "Brisbane", "goldcoast": "Gold Coast",
                 "sunshinecoast": "Sunshine Coast"}


def fetch_urbanlist(days=90, max_candidates=40):
    """Recently-updated family/kids guide articles -> venue leads."""
    cutoff = (datetime.now() - timedelta(days=days)).date().isoformat()
    status, body = fetch(UL_SITEMAP)
    pages = re.findall(r"<loc>([^<]*alist-sitemap-entries/P\d+)</loc>", body)[:2]
    out = []
    for page in pages:
        _, pb = fetch(page)
        for m in re.finditer(
                r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", pb):
            url, lastmod = m.group(1), m.group(2)[:10]
            if lastmod < cutoff:
                continue
            cm = UL_CITY_RE.search(url)
            if not cm or not UL_FAM_RE.search(url):
                continue
            slug = url.rstrip("/").rsplit("/", 1)[-1]
            c = base_candidate("urbanlist", f"cand-ul-{slugify(slug)[:80]}",
                               humanize_slug(slug)[:140])
            c["url"] = url
            c["date"] = lastmod
            c["when"] = f"Guide updated {lastmod}"
            c["category_hint"] = "urban-list family guide (venue lead)"
            c["description"] = ("Family guide article — open the link and "
                                "verify each venue individually before promoting.")
            c["travel"]["region"] = UL_CITY_LABEL[cm.group(1).lower()]
            c["age_hint"] = "Check guide — family article, verify per venue"
            c["source"] = {"label": "The Urban List",
                           "url": url}
            out.append(c)
            if len(out) >= max_candidates:
                break
        if len(out) >= max_candidates:
            break
        time.sleep(1)
    return out, {"sitemap_pages": len(pages), "window_days": days}


# ===========================================================================
# Source 3 — WeekendNotes Brisbane category pages (community listings)
# ===========================================================================
WN_CATEGORIES = [
    "https://www.weekendnotes.com/brisbane/family-friendly/",
    "https://www.weekendnotes.com/brisbane/festivals/",
    "https://www.weekendnotes.com/brisbane/markets/",
    "https://www.weekendnotes.com/brisbane/whats-on/",
]
WN_ARTICLE_RE = re.compile(r'href="(https://www\.weekendnotes\.com/[a-z0-9\-]+/)"')
WN_DATE_RE = re.compile(
    r"(?i)(?:dates? and times?|date|when)[:\s]+([A-Z][a-z]+ \d{1,2}(?:st|nd|rd|th)?"
    r"(?:\s*(?:-|–|to)\s*[A-Z][a-z]+ \d{1,2}(?:st|nd|rd|th)?)?[^.<]{0,60})")


def _wn_article(url):
    """Fetch one article: og:title + first date-like snippet. Light touch."""
    _, body = fetch(url)
    m = re.search(r'<meta property="og:title" content="([^"]+)"', body)
    title = unescape(m.group(1)).strip() if m else humanize_slug(
        url.rstrip("/").rsplit("/", 1)[-1])
    text = unescape(re.sub(r"<[^>]+>", " ", body))
    text = re.sub(r"[ \t]+", " ", text)
    when, dm = None, WN_DATE_RE.search(text)
    if dm:
        when = re.sub(r"\s+", " ", dm.group(0)).strip()[:140]
    return title[:140], when


def fetch_weekendnotes(days=90, max_candidates=40):
    out, seen = [], set()
    for cat in WN_CATEGORIES:
        try:
            _, body = fetch(cat)
        except Exception:
            continue
        for m in WN_ARTICLE_RE.finditer(body):
            url = m.group(1)
            slug = url.rstrip("/").rsplit("/", 1)[-1]
            if slug in seen:
                continue
            seen.add(slug)
            try:
                title, when = _wn_article(url)
            except Exception:
                continue
            c = base_candidate("weekendnotes", f"cand-wn-{slugify(slug)[:80]}",
                               title)
            c["url"] = url
            c["when"] = when
            c["category_hint"] = "weekendnotes community write-up"
            c["description"] = ("Community event write-up — open the article "
                                "and verify date, venue and details before promoting.")
            c["travel"]["region"] = "Brisbane"
            c["age_hint"] = "Check article — family section, verify per event"
            c["source"] = {"label": "WeekendNotes Brisbane", "url": url}
            out.append(c)
            if len(out) >= max_candidates:
                break
            time.sleep(1)
        if len(out) >= max_candidates:
            break
        time.sleep(1)
    return out, {"category_pages": len(WN_CATEGORIES)}


# ===========================================================================
# Runner — mirrors fetch-events.py conventions; NEVER touches activities.json
# ===========================================================================
SOURCES = {
    "ticketmaster": ("Ticketmaster Discovery API (official)", fetch_ticketmaster, True),
    "urbanlist": ("The Urban List sitemaps (crawl-allowed)", fetch_urbanlist, False),
    "weekendnotes": ("WeekendNotes Brisbane (community)", fetch_weekendnotes, False),
}


def run_source(name, days, max_candidates):
    label, fn, _needs_cli = SOURCES[name]
    print(f"== {label} ==", file=sys.stderr)
    try:
        out, info = fn(days=days, max_candidates=max_candidates)
    except Exception as e:
        print(f"  FAILED: {e}", file=sys.stderr)
        return None, {"status": "error", "reason": str(e)[:300]}
    print(f"  {len(out)} candidates ({info})", file=sys.stderr)
    return out, {"status": "ok", "candidates": len(out), **info}


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(
        description="Bean There QLD listing/ticketing discovery (review queue only)")
    ap.add_argument("--source", choices=list(SOURCES) + ["all"], default="all")
    ap.add_argument("--all", action="store_true", help="run every source")
    ap.add_argument("--days", type=int, default=90,
                    help="lookback/forward window in days")
    ap.add_argument("--max", type=int, default=40,
                    help="max candidates per source")
    args = ap.parse_args(argv)

    names = list(SOURCES) if (args.all or args.source == "all") else [args.source]
    q = load_queue()
    summary = {"sources": {}, "total_new": 0, "queue_total": 0}
    for name in names:
        out, info = run_source(name, args.days, args.max)
        q["sources"][name] = {**info,
                              "ran_at": datetime.now().isoformat(timespec="seconds")}
        summary["sources"][name] = q["sources"][name]
        if out:
            added = sum(add_candidate(q, c) for c in out)
            summary["total_new"] += added
            print(f"  -> {added} new", file=sys.stderr)
    save_queue(q)
    summary["queue_total"] = len(q["candidates"])
    # Machine-readable summary on stdout (cron reporting); chatter on stderr.
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

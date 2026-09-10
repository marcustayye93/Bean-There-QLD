#!/usr/bin/env python3
"""Bean There QLD — event discovery adapters (review queue only).

Fetches event candidates from two sources and appends them ONLY to
data/candidates.json, the HUMAN REVIEW QUEUE. NOTHING here publishes into
data/activities.json: promotion is by human hand, one record at a time.

Candidate records carry status "proposed" and are mapped onto the QLD
activity schema only as far as the source honestly allows:
  - name, dates, venue, URL, price and lat/lng where the source gives them
  - age_min/age_max stay null unless the source states an age range
    (a stated "ages 4-12" is parsed; anything vaguer becomes age_hint)
  - never invent, never guess

Usage:
    python3 scripts/fetch-events.py --source trumba
    python3 scripts/fetch-events.py --source eventbrite
    python3 scripts/fetch-events.py --all [--days 21] [--max 300]
    python3 scripts/fetch-events.py --source eventbrite --refresh-places
    python3 scripts/fetch-events.py --source eventbrite --probe   # needs token

Env:
    EVENTBRITE_TOKEN                   Eventbrite private token (Bearer) for
        the undocumented destination/search endpoint. Skips cleanly when unset.

Australian English throughout. Stdlib only.
"""

import csv
import io
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
QUEUE = DATA / "candidates.json"
RESEARCH = DATA / "research"
PLACES_CACHE = RESEARCH / "eventbrite-places.json"

TODAY = date.today()
UA = {"User-Agent": "BeanThereQLD-data-pipeline/1.0"}

# ---------------------------------------------------------------------------
# Zone rectangles — single source of truth lives in scripts/build-data.py.
# Imported, not copied, so the two scripts can't drift apart.
# ---------------------------------------------------------------------------
import importlib.util as _ilu

_spec = _ilu.spec_from_file_location("btq_build_data", ROOT / "scripts" / "build-data.py")
_btq = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_btq)
zone_for = _btq.zone_for


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fetch(url, timeout=60, headers=None, data=None, method=None):
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def fetch_json(url, timeout=60, headers=None, data=None, method=None):
    status, body = fetch(url, timeout=timeout, headers=headers, data=data, method=method)
    return status, json.loads(body.decode("utf-8", "replace"))


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return re.sub(r"-{2,}", "-", s) or "untitled"


def iso(d):
    return d.isoformat() if hasattr(d, "isoformat") else str(d)


def load_queue():
    if QUEUE.exists():
        q = json.loads(QUEUE.read_text())
        q.setdefault("candidates", [])
        q.setdefault("sources", {})
        return q
    return {
        "_note": ("Human review queue. Promote by hand into data/activities.json; "
                  "never auto-publish."),
        "generatedAt": None,
        "sources": {},
        "candidates": [],
    }


def save_queue(q):
    q["generatedAt"] = datetime.now().isoformat(timespec="seconds")
    QUEUE.write_text(json.dumps(q, indent=2, ensure_ascii=False) + "\n")


def add_candidate(q, cand):
    if any(c["id"] == cand["id"] for c in q["candidates"]):
        return False
    q["candidates"].append(cand)
    return True


def base_candidate(origin, cid, title):
    return {
        "id": cid,
        "origin": origin,
        "status": "proposed",
        "title": title,
        "description": None,
        "when": None,
        "date": None,
        "venue": None,
        "url": None,
        "category_hint": None,
        "price_note": None,
        "booking_url": None,
        "booking_required": None,
        "age_min": None,
        "age_max": None,
        "age_hint": None,
        "travel": {"lat": None, "lng": None, "zone": None, "region": None},
        "source": {"label": None, "url": None},
    }


def set_travel(cand, lat, lng, region=None):
    try:
        lat, lng = float(lat), float(lng)
    except (TypeError, ValueError):
        return
    cand["travel"]["lat"] = lat
    cand["travel"]["lng"] = lng
    cand["travel"]["zone"] = zone_for(lat, lng)
    cand["travel"]["region"] = region


AGE_RE = re.compile(r"ages?\s*(\d{1,2})\s*[-\u2013\u2014]\s*(\d{1,2})", re.I)

# Trumba "agerange" tokens -> conservative (min, max) bounds. The app schema
# is 0-16, so adult-only upper bounds are capped at 16 (an event for
# "Adults (30+)" alone lands at 16-16: honest "not for kids" signal).
AGERANGE_BOUNDS = {
    "infants and toddlers": (0, 3),
    "preschool kids": (3, 5),
    "kids": (5, 12),
    "teens": (13, 17),
    "young adults": (18, 29),
    "adults (30+)": (30, 99),
    "seniors": (60, 99),
}


def parse_agerange(agerange):
    """Parse the multivalued agerange column into (min, max); None if no match."""
    if not agerange:
        return None, None
    tokens = [t.strip().lower() for t in agerange.split(",")]
    bounds = [AGERANGE_BOUNDS[t] for t in tokens if t in AGERANGE_BOUNDS]
    if not bounds:
        return None, None
    lo = min(b[0] for b in bounds)
    hi = min(max(b[1] for b in bounds), 16)
    return lo, hi


def parse_age_hint(text):
    """Parse an explicitly stated age range; never guess from vague text."""
    if not text:
        return None, None, None
    m = AGE_RE.search(text)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        if 0 <= lo <= hi <= 18:
            return lo, hi, text.strip()
    if re.search(r"all ages", text, re.I):
        return 0, 16, text.strip()
    return None, None, text.strip()


# ===========================================================================
# Source 1 — BCC What's On (Trumba-derived daily extract, keyless)
#
# The dataset page (data.qld.gov.au/dataset/brisbane-city-council-events)
# says the extract is built from the Trumba Calendar API JSON feed (next
# 2,000 events, rebuilt daily). The raw Trumba feed URLs are listed in the
# dataset's "Data and Resources" section on the web UI only — they are NOT
# exposed via the CKAN or OpenDataSoft machine APIs (tried on 2026-09-10:
# CKAN package_show lists only the "Explore the dataset" HTML resource;
# the explore page HTML fetch returned empty; OpenDataSoft dataset metadata
# carries no feed URLs). So this adapter fetches the council's transformed
# daily CSV instead: same Trumba data, keyless, structured, stable.
# ===========================================================================
TRUMBA_CSV = ("https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/"
              "brisbane-city-council-events/exports/csv?limit=-1"
              "&timezone=Australia%2FBrisbane&use_labels_for_header=false")

TRUMBA_CATEGORY_HINTS = [
    (re.compile(r"family|kids|children|toddler|baby|parent", re.I), "family"),
    (re.compile(r"\bsport\b|soccer|football|basketball|swim|cricket|tennis", re.I), "sports"),
    (re.compile(r"craft|art\b|paint|draw|make and create", re.I), "craft"),
    (re.compile(r"lego|brick|build", re.I), "lego"),
    (re.compile(r"museum|exhibition|gallery|planetarium|science", re.I), "museums"),
    (re.compile(r"animal|zoo|wildlife|farm", re.I), "animals"),
    (re.compile(r"water|pool|beach", re.I), "water"),
    (re.compile(r"scout", re.I), "scouts"),
    (re.compile(r"camp|vacation care|holiday program", re.I), "camps"),
]


def trumba_category_hint(event_types):
    for rx, hint in TRUMBA_CATEGORY_HINTS:
        if rx.search(event_types or ""):
            return hint
    return None


def fetch_trumba(days=21, max_candidates=300):
    """Fetch the BCC What's On daily extract; filter to the date window."""
    status, body = fetch(TRUMBA_CSV, timeout=120)
    text = body.decode("utf-8-sig", "replace")  # the export starts with a BOM
    rows = list(csv.DictReader(io.StringIO(text), delimiter=";"))
    end_window = TODAY + timedelta(days=days)
    out, skipped = [], 0
    for r in rows:
        try:
            start = datetime.fromisoformat(r["start_datetime"]).date()
            end = datetime.fromisoformat(r["end_datetime"]).date()
        except (ValueError, KeyError, TypeError):
            skipped += 1
            continue
        if end < TODAY or start > end_window:
            continue
        if len(out) >= max_candidates:
            break
        web_link = (r.get("web_link") or "").strip()
        eventid = re.search(r"eventid%3D(\d+)", web_link) or re.search(r"eventid=(\d+)", web_link)
        cid = "cand-trumba-%s" % (eventid.group(1) if eventid else slug(r.get("subject"))[:40])
        c = base_candidate("trumba", cid, (r.get("subject") or "Untitled event").strip())
        c["description"] = (r.get("description") or "").strip()[:600] or None
        c["when"] = (r.get("formatteddatetime") or "").strip() or None
        c["date"] = iso(start)
        c["venue"] = (r.get("venue") or "").strip() or None
        c["url"] = web_link or None
        c["category_hint"] = trumba_category_hint(r.get("event_type"))
        cost = (r.get("cost") or "").strip()
        c["price_note"] = cost or None
        # bookingsrequired is a clean Yes/No/blank column; the free-text
        # bookings column sometimes carries a real booking URL (events.brisbane.qld.gov.au).
        brq = (r.get("bookingsrequired") or "").strip().lower()
        if brq == "yes":
            c["booking_required"] = True
        elif brq == "no":
            c["booking_required"] = False
        bookings_html = r.get("bookings") or ""
        mhref = re.search(r'href="(https?://[^"]+)"', bookings_html)
        if mhref:
            c["booking_url"] = mhref.group(1)
        # ages: prefer the structured agerange tokens; fall back to the
        # free-text age column ("ages 4-12", "Suitable for all ages").
        lo, hi = parse_agerange((r.get("agerange") or "").strip())
        hint = ((r.get("agerange") or "").strip() or None)
        if lo is None:
            lo, hi, hint = parse_age_hint((r.get("age") or "").strip())
        c["age_min"], c["age_max"], c["age_hint"] = lo, hi, hint
        geo = (r.get("geolocation") or "").strip()
        m = re.match(r"\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)", geo)
        if m:
            set_travel(c, m.group(1), m.group(2), (r.get("suburb") or "").strip() or None)
        c["source"] = {"label": "Brisbane City Council — What's On (Trumba extract)",
                       "url": web_link or "https://www.data.qld.gov.au/dataset/brisbane-city-council-events"}
        out.append(c)
    return out, {"rows_read": len(rows), "rows_skipped": skipped,
                 "window_days": days, "feed": "OpenDataSoft CSV (semicolon-delimited)"}


# ===========================================================================
# Source 2 — Eventbrite (undocumented destination/search, verified 2026-09-10)
#
# The documented GET /v3/events/search/ was removed in Feb 2020 — do NOT
# use it (the SG app's adapter still calls it and has been dead for years).
# This adapter uses the undocumented POST
# https://www.eventbriteapi.com/v3/destination/search/ — the same endpoint
# the eventbrite.com discovery frontend calls (confirmed from its JS
# bundles, 2026-09-10). Request body shape (verified live):
#   {"event_search": {"places": [<ids>], "page_size": 50,
#                     "dates": ["future"], "q": "kids family children",
#                     "continuation": "<token>"}}
# The `dates` field takes enum strings only ("future", "today",
# "this_weekend") — there is no server-side custom date range, so the
# adapter filters client-side by start_date. Response: events live at
# payload["events"]["results"]; pagination token at
# payload["events"]["pagination"]["continuation"].
#
# Auth: EVENTBRITE_TOKEN env var (Bearer) where available; otherwise the
# eventbrite skill's eb-call CLI (~/workspace/skills/eventbrite/bin/eb-call),
# which exchanges the stored custom.eventbrite credential via authd.
#
# Place IDs are Who's-On-First-style destination IDs scraped from the SSR
# bytes of the eventbrite.com discovery pages (each page carries exactly
# one "placeId" in its page context). Verified 2026-09-10:
#   Brisbane       101934019   (australia--brisbane-city/events/)
#   Gold Coast     1125859661  (australia--gold-coast/events/)
#   Sunshine Coast 1141906807  (australia--sunshine-coast/events/)
# Re-scrape with --refresh-places if the adapter ever starts returning
# nothing; the cache lives in data/research/eventbrite-places.json.
#
# Honest limits of this endpoint (do not invent around them):
#   - no venue name (only primary_venue_id + a locations[] hierarchy)
#   - no price / free flag, no age range
#   - candidates therefore carry area (neighbourhood/suburb) but no
#     venue, no price_note, and an explicit age_hint.
# ===========================================================================
EVENTBRITE_SLUGS = {
    "Brisbane": "australia--brisbane-city",
    "Gold Coast": "australia--gold-coast",
    "Sunshine Coast": "australia--sunshine-coast",
}
EVENTBRITE_SEARCH = "https://www.eventbriteapi.com/v3/destination/search/"
EVENTBRITE_Q = "kids family children"
EB_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
         "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")


def load_place_ids():
    if PLACES_CACHE.exists():
        return json.loads(PLACES_CACHE.read_text())
    return {"Brisbane": "101934019", "Gold Coast": "1125859661",
            "Sunshine Coast": "1141906807",
            "_verified": "2026-09-10 (SSR bytes of eventbrite.com discovery pages)"}


def refresh_place_ids():
    """Re-scrape destination place IDs from the SSR discovery pages."""
    RESEARCH.mkdir(parents=True, exist_ok=True)
    found = {}
    for city, slug_part in EVENTBRITE_SLUGS.items():
        url = f"https://www.eventbrite.com/d/{slug_part}/events/"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": EB_UA,
                "Accept": "text/html,application/xhtml+xml",
                "Accept-Language": "en-AU,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=40) as r:
                html = r.read().decode("utf-8", "replace")
                final = r.geturl()
            ids = set(re.findall(r'"placeId":"(\d+)"', html))
            if len(ids) == 1:
                found[city] = ids.pop()
                print(f"  [eventbrite] {city}: placeId={found[city]} (via {final})")
            else:
                print(f"  [eventbrite] {city}: UNEXPECTED placeId set {ids} — keeping cached value",
                      file=sys.stderr)
        except Exception as e:
            print(f"  [eventbrite] {city}: scrape failed ({e}) — keeping cached value",
                  file=sys.stderr)
    if found:
        cache = load_place_ids()
        cache.update(found)
        cache["_verified"] = TODAY.isoformat() + " (re-scraped SSR bytes)"
        PLACES_CACHE.write_text(json.dumps(cache, indent=2) + "\n")
    return found


def _eb_auth_available():
    if os.environ.get("EVENTBRITE_TOKEN"):
        return True
    return (Path.home() / "workspace" / "skills" / "eventbrite"
            / "bin" / "eb-call").exists()


def _eb_post(body):
    """POST a dict body to destination/search; return the parsed payload.

    Prefers EVENTBRITE_TOKEN (env Bearer). Falls back to the eventbrite
    skill's eb-call CLI, which authenticates via the stored credential.
    """
    token = os.environ.get("EVENTBRITE_TOKEN")
    raw = json.dumps(body).encode()
    if token:
        headers = {"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json",
                   "User-Agent": UA["User-Agent"]}
        try:
            _, payload = fetch_json(EVENTBRITE_SEARCH, headers=headers,
                                    data=raw, method="POST")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP {e.code} from destination/search: "
                               f"{e.read()[:300]!r}")
        return payload
    import subprocess
    cli = Path.home() / "workspace" / "skills" / "eventbrite" / "bin" / "eb-call"
    if not cli.exists():
        raise RuntimeError("no EVENTBRITE_TOKEN in env and no eventbrite skill CLI")
    r = subprocess.run([str(cli), "POST", EVENTBRITE_SEARCH, json.dumps(body)],
                       capture_output=True, text=True, timeout=90)
    if r.returncode != 0:
        raise RuntimeError(f"eb-call failed: {r.stderr.strip()[:300]}")
    return json.loads(r.stdout)


def fetch_eventbrite(days=21, page_size=50, max_pages=12, probe=False):
    """Sweep the three SEQ anchors with a family-biasing query.

    dates=["future"] is the only usable date enum (no server-side custom
    range), so each city's pages are walked and filtered client-side to the
    [today, today+days] window. q="kids family children" keeps the sweep to
    a few hundred family-plausible events per city instead of thousands.
    """
    places = load_place_ids()
    cities = [c for c in ("Brisbane", "Gold Coast", "Sunshine Coast") if c in places]
    if not cities:
        return None, {"status": "skipped", "reason": "no Eventbrite place IDs cached"}

    start_s, end_s = TODAY.isoformat(), (TODAY + timedelta(days=days)).isoformat()
    out, seen = [], set()
    pages_total = 0
    try:
        for city in cities:
            continuation = None
            for _page in range(max_pages):
                body = {"event_search": {
                    "places": [places[city]],
                    "page_size": page_size,
                    "dates": ["future"],
                    "q": EVENTBRITE_Q,
                }}
                if continuation:
                    body["event_search"]["continuation"] = continuation
                payload = _eb_post(body)
                pages_total += 1
                if probe:
                    evs = (payload.get("events") or {}).get("results", [])
                    print(f"  [eventbrite] probe {city}: top-level keys: "
                          f"{list(payload.keys())[:12]}")
                    if evs:
                        print("  [eventbrite] probe: first event keys: "
                              f"{sorted(evs[0].keys())}")
                    return None, {"status": "probe",
                                  "reason": "printed raw shape; wrote nothing"}
                evs = (payload.get("events") or {}).get("results", [])
                for ev in evs:
                    eid = str(ev.get("eventbrite_event_id") or ev.get("id") or "")
                    if not eid or eid in seen:
                        continue
                    seen.add(eid)
                    if ev.get("is_cancelled"):
                        continue
                    sd = str(ev.get("start_date") or "")
                    if not (start_s <= sd <= end_s):
                        continue
                    out.append(_map_eventbrite_event(ev, eid, city))
                continuation = ((payload.get("events") or {})
                                .get("pagination", {}).get("continuation"))
                if not continuation:
                    break
    except RuntimeError as e:
        # Auth/endpoint failure: report, never fatal to the pipeline.
        if "HTTP 401" in str(e) or "HTTP 403" in str(e):
            return None, {"status": "auth_rejected",
                          "reason": f"Eventbrite rejected the credential: {e}"[:300]}
        return None, {"status": "failing", "reason": str(e)[:300]}
    return out, {"cities": cities, "pages": pages_total,
                 "window_days": days, "query": EVENTBRITE_Q}


def _eb_area(ev):
    """Best area label from the locations[] hierarchy (no venue names exist)."""
    locs = ev.get("locations") or []
    by_type = {l.get("type"): l.get("name") for l in locs if isinstance(l, dict)}
    for t in ("neighbourhood", "localadmin", "locality", "county", "region"):
        if by_type.get(t):
            return by_type[t]
    return None


def _map_eventbrite_event(ev, eid, city):
    """Map the verified destination/search event shape onto a candidate."""
    c = base_candidate("eventbrite", f"cand-eb-{eid}",
                       str(ev.get("name") or "Untitled event").strip())
    c["description"] = str(ev.get("summary") or "")[:600] or None
    c["url"] = ev.get("url") or None
    sd = str(ev.get("start_date") or "")
    c["date"] = sd or None
    st, et = ev.get("start_time"), ev.get("end_time")
    if sd and (st or et):
        c["when"] = f"{sd} {st or ''}–{et or ''}".strip()
    elif sd:
        c["when"] = sd
    # No venue name is published by this endpoint; record the area honestly.
    area = _eb_area(ev)
    c["travel"]["region"] = area or city
    c["venue"] = None
    c["price_note"] = None  # not published by this endpoint
    tags = [t.get("display_name") for t in (ev.get("tags") or [])
            if isinstance(t, dict) and t.get("display_name")]
    if tags:
        c["category_hint"] = ", ".join(tags[:3])
    if ev.get("is_online_event"):
        c["description"] = ((c["description"] or "")
                            + " [Online event]").strip()
    c["age_hint"] = "Check listing — Eventbrite does not publish age ranges"
    c["source"] = {"label": "Eventbrite",
                   "url": c["url"] or "https://www.eventbrite.com"}
    return c




# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
SOURCES = {
    "trumba": ("BCC What's On (Trumba extract)", fetch_trumba, False),
    "eventbrite": ("Eventbrite destination/search (fragile)", fetch_eventbrite, True),
}


def run_source(name, days, max_candidates, probe=False):
    label, fn, needs_key = SOURCES[name]
    print(f"== {label} ==")
    try:
        if name == "eventbrite":
            out, info = fn(days=days, probe=probe)
        else:
            out, info = fn(days=days)
    except Exception as e:
        print(f"  FAILED: {e}", file=sys.stderr)
        return None, {"status": "error", "reason": str(e)[:300]}
    status = info.pop("status", "ok")
    if out is None:
        print(f"  skipped: {info.get('reason')}")
        return None, {"status": status, **info}
    if probe:
        return None, {"status": status, **info}
    print(f"  {len(out)} candidates ({info})")
    return out, {"status": "ok", "candidates": len(out), **info}


def main(argv):
    import argparse
    ap = argparse.ArgumentParser(description="Bean There QLD event discovery (review queue only)")
    ap.add_argument("--source", choices=list(SOURCES) + ["all"], default="all")
    ap.add_argument("--all", action="store_true", help="run every source")
    ap.add_argument("--days", type=int, default=21, help="date window in days")
    ap.add_argument("--max", type=int, default=300, help="max candidates per source")
    ap.add_argument("--refresh-places", action="store_true",
                    help="re-scrape Eventbrite destination place IDs from SSR pages")
    ap.add_argument("--probe", action="store_true",
                    help="print Eventbrite raw response shape, write nothing (needs token or skill CLI)")
    args = ap.parse_args(argv)

    if args.refresh_places:
        refresh_place_ids()
        if args.source == "eventbrite" and not _eb_auth_available():
            return 0  # place refresh alone is a complete, useful run

    names = list(SOURCES) if (args.all or args.source == "all") else [args.source]
    q = load_queue()
    added_total = 0
    for name in names:
        out, info = run_source(name, args.days, args.max, probe=args.probe)
        q["sources"][name] = {**info, "ran_at": datetime.now().isoformat(timespec="seconds")}
        if out:
            added = sum(add_candidate(q, c) for c in out)
            added_total += added
            print(f"  -> {added} new (queue now {len(q['candidates'])})")
    if not args.probe:
        save_queue(q)
        print(f"wrote {QUEUE} ({added_total} new candidates)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

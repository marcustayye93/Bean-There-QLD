#!/usr/bin/env python3
"""Bean There QLD — data pipeline (v1).

Regenerates all three JSON data files from public sources:
  1. data/holidays.json    — Qld DoE school-holiday ICS feed (+ baked fallbacks)
  2. data/activities.json  — BCC parks + pools (live) + hand-verified samples
  3. data/postcodes.json   — QLD postcode centroids (falls back to an honest
                             empty file if no verifiable public dataset exists)

Usage:
    python3 scripts/build-data.py            # from the repo root
    # or: ./scripts/build-data.py

Everything is keyless. Nothing here fabricates listings: live records come
straight from the source datasets; everything else is flagged live:false.

Australian English throughout.
"""

import csv
import json
import re
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TODAY = "2026-09-10"

ICS_URL = "http://education.qld.gov.au/about/Documents/qld-school-holidays.ics"
PARKS_URL = ("https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/"
             "park-locations/exports/csv?limit=-1&timezone=Australia%2FBrisbane"
             "&use_labels_for_header=false")
POOLS_URL = ("https://data.brisbane.qld.gov.au/api/explore/v2.1/catalog/datasets/"
             "swimming-pools/exports/csv?limit=-1&timezone=Australia%2FBrisbane"
             "&use_labels_for_header=false")

# ---------------------------------------------------------------------------
# Zone rectangles (lat_min, lat_max, lng_min, lng_max), approximating SEQ LGAs.
# Checked in order; first match wins. Anything unmatched -> "Queensland".
# These are coarse on purpose — document, don't precision-tune.
# ---------------------------------------------------------------------------
ZONES = [
    # name,                 lat_min, lat_max, lng_min, lng_max,  notes
    ("Brisbane CBD & Inner", -27.53, -27.41, 152.97, 153.08,
     "CBD, Valley, New Farm, South Bank, West End, Paddington, Milton, Toowong"),
    ("North Brisbane",       -27.41, -27.27, 152.95, 153.13,
     "Chermside, Aspley, Zillmere, Bracken Ridge, Sandgate, Brighton"),
    ("South Brisbane",       -27.66, -27.53, 152.95, 153.13,
     "Holland Park, Mt Gravatt, Sunnybank, Runcorn, Calamvale, Parkinson"),
    ("East Brisbane",        -27.62, -27.38, 153.08, 153.24,
     "Cannon Hill, Tingalpa, Wynnum, Manly, Burbank, Chandler"),
    ("West Brisbane",        -27.62, -27.39, 152.78, 152.97,
     "Indooroopilly, Kenmore, Jindalee, Mt Ommaney, Bellbowrie, Ferny Grove"),
    ("Ipswich",              -27.78, -27.48, 152.50, 152.95,
     "Ipswich CBD, Springfield, Redbank Plains"),
    ("Logan",                -27.80, -27.62, 152.95, 153.25,
     "Logan Central, Beenleigh, Jimboomba (edge approx)"),
    ("Redlands",             -27.62, -27.48, 153.13, 153.35,
     "Cleveland, Capalaba, Victoria Point"),
    ("Moreton Bay",          -27.42, -26.95, 152.75, 153.20,
     "Caboolture, Redcliffe, North Lakes, Strathpine"),
    ("Gold Coast",           -28.30, -27.80, 153.05, 153.65,
     "Surfers Paradise, Burleigh, Coolangatta, hinterland"),
    ("Sunshine Coast",       -27.00, -26.30, 152.80, 153.25,
     "Caloundra, Maroochydore, Noosa, hinterland"),
]


def zone_for(lat, lng):
    for name, la0, la1, lo0, lo1, _notes in ZONES:
        if la0 <= lat <= la1 and lo0 <= lng <= lo1:
            return name
    return "Queensland"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fetch(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "BeanThereQLD-data-pipeline/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def titlecase(s):
    s = s.strip().title()
    s = re.sub(r"\bMc([a-z])", lambda m: "Mc" + m.group(1).upper(), s)
    s = re.sub(r"([A-Za-z])'S\b", lambda m: m.group(1) + "'s", s)
    s = re.sub(r"\bO'([A-Za-z])", lambda m: "O'" + m.group(1).upper(), s)
    s = s.replace("Coot-Tha", "Coot-tha")
    return s


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return re.sub(r"-{2,}", "-", s)


def iso(d):
    return d.isoformat()


# ---------------------------------------------------------------------------
# 1. holidays.json
# ---------------------------------------------------------------------------
# Baked fallback if the ICS feed cannot be fetched (verified 2026-09-10).
FALLBACK_HOLIDAYS = [
    ("Autumn school holidays 2026", "2026-04-07", "2026-04-18"),
    ("Winter school holidays 2026", "2026-06-30", "2026-07-11"),
    ("Spring school holidays 2026", "2026-09-22", "2026-10-03"),
    ("Summer school holidays 2026-27", "2026-12-15", "2027-01-23"),
]

# 2027 windows from the DoE 2027 school planner (the ICS feed currently only
# extends to Jan 2027, so these are baked in and re-checked on each rebuild).
HOLIDAYS_2027 = [
    ("Autumn school holidays 2027", "2027-03-26", "2027-04-11"),
    ("Winter school holidays 2027", "2027-06-26", "2027-07-11"),
    ("Spring school holidays 2027", "2027-09-18", "2027-10-04"),
    ("Summer school holidays 2027-28", "2027-12-11", "2028-01-23"),
]

# DoE-published term dates for 2026 (not present in the ICS; confirmed across
# multiple QLD state school sites publishing the department's dates).
TERMS_2026 = [
    ("Term 1 2026", "2026-01-27", "2026-04-02"),
    ("Term 2 2026", "2026-04-20", "2026-06-26"),
    ("Term 3 2026", "2026-07-13", "2026-09-18"),
    ("Term 4 2026", "2026-10-06", "2026-12-11"),
]


def season_name(start):
    m = start.month
    if m in (12, 1, 2):
        yr = f"{start.year}-{str(start.year + 1)[-2:]}" if m == 12 else f"{start.year - 1}-{str(start.year)[-2:]}"
        return f"Summer school holidays {yr}"
    if m in (3, 4, 5):
        return f"Autumn school holidays {start.year}"
    if m in (6, 7, 8):
        return f"Winter school holidays {start.year}"
    return f"Spring school holidays {start.year}"


def parse_ics(raw):
    """Return (holiday_periods, public_holidays) from ICS text.

    Holiday periods: (name, start_iso, end_iso) with inclusive dates.
    The feed's DTEND;VALUE=DATE is exclusive, so the inclusive end is DTEND-1.
    """
    text = raw.decode("utf-8", errors="replace")
    # iCalendar unfolding: continuation lines start with a space or tab.
    text = re.sub(r"\r?\n[ \t]", "", text)
    holidays, public = [], []
    for chunk in text.split("BEGIN:VEVENT")[1:]:
        chunk = chunk.split("END:VEVENT")[0]

        def get(prop):
            m = re.search(r"^" + prop + r"(?:;[^:]*)?:([^\n]*)", chunk, re.M)
            return m.group(1).strip() if m else ""

        summary = get("SUMMARY")
        ds, de = get("DTSTART"), get("DTEND")
        if not (summary and ds and de):
            continue
        start = date(int(ds[0:4]), int(ds[4:6]), int(ds[6:8]))
        end = date(int(de[0:4]), int(de[4:6]), int(de[6:8])) - timedelta(days=1)  # exclusive -> inclusive
        if "School Holidays" in summary:
            holidays.append((season_name(start), iso(start), iso(end)))
        elif "Public Holiday" in summary or summary in (
                "Christmas Day", "Boxing Day", "New Years Day", "New Year's Day"):
            public.append((re.sub(r"\s+", " ", summary), iso(start), iso(end)))
        # Staff development days etc. are intentionally skipped.
    return holidays, public


def build_holidays():
    periods = []
    note_bits = []
    try:
        raw = fetch(ICS_URL)
        feed_holidays, feed_public = parse_ics(raw)
        if not feed_holidays:
            raise ValueError("ICS parsed but contained no School Holidays events")
        for name, s, e in feed_holidays:
            if s >= "2026-01-01":
                periods.append({"name": name, "type": "holiday", "start": s, "end": e})
        for name, s, e in feed_public:
            if s >= "2026-01-01":
                periods.append({"name": name, "type": "public_holiday", "start": s, "end": e})
        note_bits.append(
            "School-holiday windows parsed live from the Qld Department of Education ICS feed "
            "(VEVENTs; the feed's DTEND is exclusive, so end dates are DTEND minus one day).")
        # Sanity: the feed's Spring 2026 window should roughly match the known one.
        spring = [p for p in periods if p["name"] == "Spring school holidays 2026"]
        if spring and (spring[0]["start"], spring[0]["end"]) != ("2026-09-21", "2026-10-02"):
            note_bits.append(
                "WARNING: the feed's Spring 2026 window moved since 2026-09-10 — "
                "check the DoE planner before publishing.")
    except Exception as exc:  # feed failed -> baked fallback, flagged honestly
        print(f"  ICS fetch failed ({exc}); using baked fallback windows", file=sys.stderr)
        for name, s, e in FALLBACK_HOLIDAYS:
            periods.append({"name": name, "type": "holiday", "start": s, "end": e})
        note_bits.append(
            "WARNING: the DoE ICS feed could not be fetched on this run, so the school-holiday "
            "windows below are baked fallbacks verified 2026-09-10. Re-run the build when the "
            "feed is reachable.")

    for name, s, e in TERMS_2026:
        periods.append({"name": name, "type": "term", "start": s, "end": e})
    note_bits.append(
        "Term dates are from DoE-published term dates (confirmed across QLD state school sites); "
        "terms are not present in the ICS feed.")
    for name, s, e in HOLIDAYS_2027:
        periods.append({"name": name, "type": "holiday", "start": s, "end": e})
    note_bits.append(
        "2027 holiday windows are from the DoE 2027 school planner — the ICS feed currently "
        "extends only to Jan 2027.")
    note_bits.append(
        "Holiday windows mark school weekdays; the flanking weekends are school-free too. "
        "Re-fetch annually; the ICS feed extends ~12 months forward.")

    periods.sort(key=lambda p: p["start"])
    return {
        "source_url": ICS_URL,
        "generated": TODAY,
        "note": " ".join(note_bits),
        "periods": periods,
    }


# ---------------------------------------------------------------------------
# 2. activities.json
# ---------------------------------------------------------------------------
BCC_PARKS = {"label": "Brisbane City Council — Park Locations",
             "url": "https://www.data.qld.gov.au/dataset/park-locations"}
BCC_POOLS = {"label": "Brisbane City Council — Swimming Pool locations",
             "url": "https://www.data.qld.gov.au/dataset/swimming-pools"}


def build_live_activities():
    activities = []
    seen_ids = set()

    def unique_id(base):
        cand = base
        i = 2
        while cand in seen_ids:
            cand = f"{base}-{i}"
            i += 1
        seen_ids.add(cand)
        return cand

    # -- Parks: 10 largest per Brisbane zone (objective, reproducible curation).
    raw = fetch(PARKS_URL).decode("utf-8-sig")
    parks = list(csv.DictReader(raw.splitlines(), delimiter=";"))
    by_zone = {}
    for p in parks:
        try:
            lat, lng = float(p["lat"]), float(p["long"])
        except (ValueError, TypeError, KeyError):
            continue
        z = zone_for(lat, lng)
        if z == "Queensland":
            continue  # outside the SEQ zone rectangles
        by_zone.setdefault(z, []).append((float(p["shape_area"] or 0), p, lat, lng))
    for z in [zname for zname, *_ in ZONES[:5]]:
        picks = sorted(by_zone.get(z, []), key=lambda t: t[0], reverse=True)[:10]
        for _area, p, lat, lng in picks:
            name = titlecase(p["park_name"])
            suburb = titlecase(p["suburb"])
            activities.append({
                "id": unique_id("park-" + slug(name)),
                "name": name,
                "description": f"Park in {suburb} listed by Brisbane City Council.",
                "suburb": suburb, "region": "Brisbane", "zone": z,
                "age_min": 0, "age_max": 12, "category": "playgrounds",
                "indoor": "outdoor", "price_aud": 0, "price_note": "Free entry",
                "duration": "1-3 hours", "booking_url": None, "booking_required": False,
                "lat": round(lat, 6), "lng": round(lng, 6),
                "source": BCC_PARKS, "live": True, "holiday_only": False,
                "interests": ["outdoor"],
            })

    # -- Pools: all 22 council pools. The dataset gives no prices, so price is
    # unknown (entry fees usually apply) — never claimed as free.
    raw = fetch(POOLS_URL).decode("utf-8-sig")
    pools = list(csv.DictReader(raw.splitlines(), delimiter=";"))

    def pool_suburb(address):
        address = address.strip()
        if "," in address:
            return titlecase(address.rsplit(",", 1)[-1])
        return titlecase(address.rsplit(" ", 1)[-1])

    for p in pools:
        name = p["name"].strip()
        try:
            lat, lng = float(p["latitude"]), float(p["longitude"])
        except (ValueError, TypeError):
            continue
        suburb = pool_suburb(p["address"])
        activities.append({
            "id": unique_id("pool-" + slug(name)),
            "name": name,
            "description": f"Public swimming pool in {suburb} listed by Brisbane City Council.",
            "suburb": suburb, "region": "Brisbane", "zone": zone_for(lat, lng),
            "age_min": 0, "age_max": 16, "category": "water",
            "indoor": "outdoor", "price_aud": None,
            "price_note": "Entry fees may apply — check council site",
            "duration": "1-3 hours", "booking_url": None, "booking_required": False,
            "lat": round(lat, 6), "lng": round(lng, 6),
            "source": BCC_POOLS, "live": True, "holiday_only": False,
            "interests": ["water", "outdoor"],
        })
    return activities


def sample(id_, name, description, category, age_min, age_max, booking_url,
           interests, indoor="both", price_aud=None, price_note="Check with provider",
           duration="Varies — check with provider", booking_required=True,
           holiday_only=False):
    return {
        "id": id_, "name": name, "description": description,
        "suburb": "Various", "region": "Queensland", "zone": "Queensland",
        "age_min": age_min, "age_max": age_max, "category": category,
        "indoor": indoor, "price_aud": price_aud, "price_note": price_note,
        "duration": duration, "booking_url": booking_url,
        "booking_required": booking_required,
        "lat": None, "lng": None,
        "source": {"label": "Hand-verified sample (see data/DATA_SOURCES.md)",
                   "url": booking_url},
        "live": False, "holiday_only": holiday_only,
        "interests": interests,
    }


SCOUTS_JOIN = "https://scoutsqld.com.au/join-scouts/cub-scouts-7-11-yrs/"
PLAYFOOTBALL_MINIROOS = "https://playfootball.com.au/miniroos/players"
BASKETBALL_GET_STARTED = "https://www.queensland.basketball/play/get-started"
PCYC_HOLIDAYS = "https://www.pcyc.org.au/get-active/school-holiday-programs/"
YMCA_CENTRES = "https://ymcaqueensland.org.au/services/community-centres?mc_cid=3386862d1c&mc_eid=UNIQID"
BCC_EVENTS = "https://www.brisbane.qld.gov.au/events"


def build_samples():
    return [
        # -- Scouts (ages per Scouts Queensland: Joeys 5-8, Cubs 8-11) --
        sample("sample-scouts-joeys", "Scouts Queensland — Joey Scouts (ages 5–8)",
               "Weekly section for 5–8 year olds: games, craft, day hikes and outdoor adventure "
               "skills. Find your local of 200+ Queensland groups via Scouts Queensland.",
               "scouts", 5, 8, SCOUTS_JOIN, ["scouts", "outdoor"],
               price_note="Membership fees apply — check with your local group",
               duration="Weekly during school terms"),
        sample("sample-scouts-cubs", "Scouts Queensland — Cub Scouts (ages 8–11)",
               "Weekly section for 8–11 year olds: camping, canoeing, navigation and bushwalks. "
               "Find your local group via Scouts Queensland.",
               "scouts", 8, 11, SCOUTS_JOIN, ["scouts", "outdoor"],
               price_note="Membership fees apply — check with your local group",
               duration="Weekly during school terms"),
        sample("sample-scouts-scouts", "Scouts Queensland — Scouts (ages 11–14)",
               "Weekly section for 11–14 year olds: expeditions, camp cooking and leadership "
               "skills. Find your local group via Scouts Queensland.",
               "scouts", 11, 14, SCOUTS_JOIN, ["scouts", "outdoor"],
               price_note="Membership fees apply — check with your local group",
               duration="Weekly during school terms"),
        # -- Soccer (ages per Football Australia / Football Queensland) --
        sample("sample-soccer-miniroos-kickoff", "MiniRoos Kick-Off (ages 4–11)",
               "National introductory soccer program for boys and girls aged 4–11: 45–60 minute "
               "weekly sessions over 4–12 weeks. Find a club via Play Football.",
               "soccer", 4, 11, PLAYFOOTBALL_MINIROOS, ["soccer"], indoor="outdoor",
               price_note="Registration fees vary by club — check with provider",
               duration="45–60 min weekly sessions"),
        sample("sample-soccer-miniroos-club", "MiniRoos Club Football (ages 5–11)",
               "Team-based small-sided soccer (4v4, 7v7, 9v9) played in the winter season for "
               "ages 5–11. Find a club via Play Football.",
               "soccer", 5, 11, PLAYFOOTBALL_MINIROOS, ["soccer"], indoor="outdoor",
               price_note="Registration fees vary by club — check with provider",
               duration="Weekly in the winter season"),
        sample("sample-soccer-miniroos-girls", "MiniRoos for Girls — MiniTillies (ages 4–11)",
               "Girls-only introductory soccer program for ages 4–11, run over 4–12 weeks. "
               "Find a program via Play Football.",
               "soccer", 4, 11, PLAYFOOTBALL_MINIROOS, ["soccer"], indoor="outdoor",
               price_note="Registration fees vary by club — check with provider",
               duration="45–60 min weekly sessions"),
        # -- Basketball --
        sample("sample-basketball-junior", "Basketball Queensland — junior domestic competitions",
               "Junior domestic basketball run by 43 affiliated associations across Queensland. "
               "Age groups and seasons vary by association — use the Basketball Queensland "
               "finder to contact your nearest one.",
               "basketball", 5, 16, BASKETBALL_GET_STARTED, ["basketball"], indoor="indoor",
               price_note="Registration fees vary by association — check with provider",
               duration="Weekly in season"),
        sample("sample-basketball-dev", "Basketball Queensland — kids development programs (ages 4–9)",
               "Introductory basketball for kids aged 4–9: fundamental skills, teamwork and "
               "confidence through structured activities and modified games. Find a program via "
               "Basketball Queensland.",
               "basketball", 4, 9, BASKETBALL_GET_STARTED, ["basketball"], indoor="indoor",
               price_note="Program fees vary by association — check with provider",
               duration="Varies by program"),
        # -- Holiday camps --
        sample("sample-camp-pcyc", "PCYC Queensland school holiday programs",
               "Half-day and full-day school holiday activity camps at PCYC clubs statewide — "
               "gymnastics, team games, laser tag, court sports and more. Program varies by club.",
               "camps", 5, 12, PCYC_HOLIDAYS, ["outdoor"],
               price_note="Check with provider", duration="Half-day and full-day camps",
               holiday_only=True),
        sample("sample-camp-ymca", "YMCA Queensland school holiday programs",
               "School holiday programs run at YMCA community centres across south-east "
               "Queensland (e.g. Springfield Lakes, North Lakes, Mango Hill). Check your nearest "
               "centre for the current program.",
               "camps", 3, 12, YMCA_CENTRES, ["outdoor"],
               price_note="Check with provider", duration="Varies by centre",
               holiday_only=True),
        # -- Lego / building --
        sample("sample-lego-bcc-brick-builders", "BCC Libraries — Brick builders code club (ages 8–12)",
               "Hands-on STEAM building sessions at Brisbane City Council libraries, usually in "
               "the school holidays. Some branches require bookings — check the council events "
               "page for current sessions.",
               "lego", 8, 12, BCC_EVENTS, ["lego"], indoor="indoor",
               price_note="Check with provider", duration="1–2 hour sessions",
               holiday_only=True),
        # -- Craft --
        sample("sample-craft-bcc-make-create", "BCC Libraries — Make and create for kids (ages 4–12)",
               "Free drop-in art and craft sessions at Brisbane City Council libraries — no "
               "booking needed. Check the council events page for current sessions.",
               "craft", 4, 12, BCC_EVENTS, ["craft"], indoor="indoor",
               price_aud=0, price_note="Free entry", duration="Drop-in sessions",
               booking_required=False),
    ]


def build_activities():
    live = build_live_activities()
    samples = build_samples()
    activities = live + samples
    sources = [
        {"label": BCC_PARKS["label"], "url": BCC_PARKS["url"],
         "license": "CC-BY-4.0", "used": "live"},
        {"label": BCC_POOLS["label"], "url": BCC_POOLS["url"],
         "license": "CC-BY-4.0", "used": "live"},
        {"label": "Scouts Queensland", "url": "https://scoutsqld.com.au/",
         "license": "n/a (program info)", "used": "sample"},
        {"label": "Play Football (Football Australia) — MiniRoos",
         "url": PLAYFOOTBALL_MINIROOS, "license": "n/a (program info)", "used": "sample"},
        {"label": "Basketball Queensland", "url": BASKETBALL_GET_STARTED,
         "license": "n/a (program info)", "used": "sample"},
        {"label": "PCYC Queensland — School Holiday Programs", "url": PCYC_HOLIDAYS,
         "license": "n/a (program info)", "used": "sample"},
        {"label": "YMCA Queensland — Community Centres", "url": YMCA_CENTRES,
         "license": "n/a (program info)", "used": "sample"},
        {"label": "Brisbane City Council — library events", "url": BCC_EVENTS,
         "license": "n/a (program info)", "used": "sample"},
        {"label": "ATDW ATLAS API (queensland.com / TEQ)",
         "url": "https://developer.atdw.com.au",
         "license": "keyed distributor API", "used": "skipped"},
    ]
    return {
        "meta": {
            "generated": TODAY,
            "live_count": len(live),
            "sample_count": len(samples),
            "sources": sources,
        },
        "activities": activities,
    }


# ---------------------------------------------------------------------------
# 3. postcodes.json
# ---------------------------------------------------------------------------
def build_postcodes():
    # Searched 2026-09-10: data.gov.au and data.qld.gov.au carry no public,
    # verifiable Australia-wide postcode -> suburb -> centroid dataset
    # (Australia Post's postcode datafile is paid; G-NAF is ~5GB unpacked;
    # Geoscape admin boundaries carry localities/LGAs but not postcodes).
    # Per the data policy we ship the honest fallback rather than a partial
    # or unverifiable list.
    return {
        "note": ("Postcode lookup unavailable — no verifiable public AU postcode dataset "
                 "found (checked data.gov.au and data.qld.gov.au 2026-09-10). "
                 "The app should degrade with an honest re-enter notice."),
        "postcodes": {},
    }


# ---------------------------------------------------------------------------
def main():
    DATA.mkdir(parents=True, exist_ok=True)

    print("1/3 holidays.json ...")
    holidays = build_holidays()
    (DATA / "holidays.json").write_text(json.dumps(holidays, indent=2, ensure_ascii=False) + "\n")
    print(f"    {len(holidays['periods'])} periods")

    print("2/3 activities.json ...")
    activities = build_activities()
    (DATA / "activities.json").write_text(json.dumps(activities, indent=2, ensure_ascii=False) + "\n")
    m = activities["meta"]
    print(f"    {m['live_count']} live, {m['sample_count']} samples")

    print("3/3 postcodes.json ...")
    postcodes = build_postcodes()
    (DATA / "postcodes.json").write_text(json.dumps(postcodes, indent=2, ensure_ascii=False) + "\n")
    print(f"    {len(postcodes['postcodes'])} postcodes (fallback note written)")

    print("Done.")


if __name__ == "__main__":
    main()

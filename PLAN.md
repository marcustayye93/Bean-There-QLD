# Bean There QLD — Phase 1 Adaptation Plan (2026-09-10)

Status: **AWAITING MARCUS'S APPROVAL.** No build until approved.

## V2 SCOPE UPDATE (2026-09-10): family school-holiday planner

The concept has been reframed around a concrete end user. Everything in
§1–§11 below (the V1 architecture baseline) still applies, with these
additions/changes:

**Who it's for:** Mek — a mother of two in Queensland who works full
time. Her husband spends hours over multiple nights each school holidays
manually hunting for activities for their older son Levi (who does not
want to stay home while both parents work). The app replaces that manual
search. Design for low patience, mobile-first: **"good enough in 30
seconds" beats "perfect in 5 minutes".**

**Core question the app answers:** "What can we do with the kids around
here, in the next school holidays or this weekend, that works for both
ages?"

### Data model (extends the SG activity schema)

Every activity carries: name, short description, suburb/region, **age_min
+ age_max**, category, indoor/outdoor, price (AUD, incl. free), duration,
booking link, booking_required (bool), lat/lng, source. Age suitability
is a first-class field, not a tag.

### Dual-age suitability filter (headline feature)

- Settings store two configurable child ages (any pair, 0–16). Seed
  defaults: **4 and 7** (Levi is the older).
- Three filter states, clearly labelled: (a) Suits both children,
  (b) Suits younger only, (c) Suits older only. **Default: suits both.**
- Matching rule: activity suits a child when
  `age_min <= age <= age_max`. This is the single hardest thing the
  parent currently works out manually.

### Travel time filter

- Home suburb or Queensland postcode in settings.
- Buckets: under 15 min, under 30 min, under 1 hour, under 2 hours, any.
- Estimated drive time shown on every card; sort-by-travel-time as a
  sort option.
- Implementation: distance-based drive-time heuristic (same honest
  discipline as SG's drive chips — estimates labelled as estimates,
  recomputed live from the user's own postcode).

### Categories

User-named: **Sports (soccer and basketball called out by name)**,
Craft, Holiday camps / vacation care, Scouts and similar youth programs,
Lego and building activities.
Supporting: playgrounds and parks, museums and science centres, animal
encounters and zoos, water play / pools / beaches, free activities.

### School holiday calendar awareness

- Queensland state school term/holiday dates for the current and next
  year, from the official Department of Education source. (Research
  underway to verify the URL and 2026–2027 dates.)
- Persistent banner, e.g. "September holidays: 2 weeks, starting
  <date>, N days away" — computed live from the dates.
- One-tap filter: "Show me things for the next school holidays".
- Holiday-only programs (vacation care, holiday camps) flagged as such —
  they don't run during term.
- README documents how to update the dates each year.

### Saving and planning (local-first, no login)

- Favourite an activity; assign a saved activity to a specific date.
- Simple calendar/list view of the holiday block showing which days are
  empty.
- Share the plan as a link (plan encoded in the URL hash) or as plain
  text, so Mek can send it to her husband.
- V1: all settings + saved activities in device localStorage. **No user
  accounts, no payments, no social features** (explicitly out of scope).

### Child interest profiles

- Per-child interest tags. Seed **Levi's with soccer, basketball, Lego**.
- A "Recommended for Levi" row matching interest + age + travel time.

### Data policy (non-negotiable)

- Real, verifiable public sources only. Never fabricate activity listings.
- If a category has no live source: build the schema, seed a small set of
  clearly labelled SAMPLE records, document exactly which records are
  samples and which are live. **Never present sample data as real.**
### Data source verdicts (2026-09-10 ~14:15 SGT, all URLs opened/verified)

**LIVE:**
- **Qld DoE school holidays ICS feed** — `education.qld.gov.au/about/Documents/qld-school-holidays.ics`
  (official page: `education.qld.gov.au/about-us/calendar/school-holidays`).
  Machine-readable VEVENTs; confirmed windows: Easter 2026 3–17 Apr, Winter
  2026 29 Jun–10 Jul, **Spring 2026 21 Sep–2 Oct**, Summer 2026–27 14 Dec–25 Jan;
  2027 windows from the official planner PDFs. (Note: the live feed's
  school-weekday framing differs by a day from the DoE planner page's
  calendar framing, e.g. the page lists Spring 2026 as 22 Sep–3 Oct. The
  feed is treated as authoritative: it agrees with school term calendars
  and sits cleanly between Term 3's end and Term 4's start on 6 Oct,
  with Labour Day 5 Oct in between.) **Plan: parse the ICS
  for the holiday banner + "next holidays" filter** (it auto-updates when
  DoE extends it; re-fetch annually; hard-code from the planner PDFs as
  fallback). Spring 2026 starts 11 days from 2026-09-10.
- **Council open data (places)**: BCC via data.brisbane.qld.gov.au, CC-BY,
  keyless — "Park — Locations" (2,180+ w/ coordinates), "Swimming Pool
  locations", "Park — Tracks and Trails", "Park — Barbeque locations".
  Covers parks, pools, playground-as-place data.
- **ATDW ATLAS API** (keyed): ATTRACTION + EVENT categories with
  latlong+dist geo search — strong for zoos, museums, theme/water parks,
  animal encounters. Tourism skew: won't have council programs or local
  playgrounds.

**FRAGILE (scrape-class, review queue only):**
- Council event/holiday-program pages (BCC `brisbane.qld.gov.au/events/<slug>/<id>`
  carry dates, venue, lat/lng, booking requirement, AND ideal age like
  "ages 4–12" — perfect schema fields; enumeration is search-engine
  class). Programs named: BCC Chillout, Logan Krank, Moreton Bay Active
  Holiday Programs, Ipswich Kids Go Wild + Active Breaks, Redland holiday
  events calendar.
- whatsongoldcoast.au `/All-events/` pages + Council Active & Healthy
  calendar (440 results).
- CareforKids.com.au vacation-care directory (predictable
  `/vacation-care/<suburb>/<postcode>` URLs; name/address/avg $/day/NQS
  rating — ToS scrape caution, commercial site).
- brisbanekids.com.au (WordPress, server-rendered, 11 years of editorial
  — events calendar, playground guides, free-activity roundups; strongest
  editorial source, ToS caution).
- GameDay legacy tables for soccer club structure (season-keyed).

**NO LIVE SOURCE → labelled samples:**
- Scouts groups (scoutsqld.com.au has no finder; 200+ QLD groups
  confirmed only via PDF; Joeys starts at 6 so Scouts fails "suits both"
  for the 4-year-old — schema keeps it for the older child).
- Soccer clubs (Football QLD: no public club finder; Squadi/per-club
  pages only) and basketball clubs (Basketball QLD: 43 associations,
  static finder page, no suburb machine data).
- Holiday camps with program-level detail (link out to YMCA/PCYC finders).

### Empty states

- If nothing suits both ages within 30 minutes, say so plainly and
  offer the nearest alternative (widen age or travel bucket) — never a
  blank screen.

### Deliverable

A working, deployable web app in `marcustayye93/Bean-There-QLD` plus a
short README: which data sources are live vs sample, how to add new
activities, how to update school holiday dates each year.

### Decision list (updated)

1. Zone quotas/caps (§2) — carried over unless you object.
2. Postcode lookup: prebuilt CSV vs live lookup.
3. ATDW distributor key: register or skip?
4. Eventbrite token: still available?
5. RESOLVED 2026-09-10 ~14:16 SGT: Mek is a persona, not a real user.
   The app must not be built around any one real person. All persona
   details (child names, ages 4 and 7, Levi's soccer/basketball/Lego
   interests, home suburb) ship as changeable defaults in settings —
   nothing is hard-coded to a real identity, and UI copy must not assume
   who is using it (e.g. the recommendation row reads "Recommended for
   {child name}" with the name editable).
6. Build APPROVED 2026-09-10 ~14:17 SGT. Coordinator dispatched to build
   the full v1 in ~/workspace/bean-there-qld (data pipeline + app +
   README), verified locally. Standing rule holds: NO push and NO deploy
   until Marcus reviews the finished build and explicitly approves.

---

## V1 architecture baseline (carried forward)

## 1. What we lift from the Singapore app (unchanged)

Architecture studied from `~/workspace/beanie-day` (full reference from the
baseline-study pass; key points below):

- **Data model**: single `data/week.json` with `{ meta, tabs, activities }`;
  activity schema = `id, title, venue, description, why, when, deal, parking,
  heatNote, days, tags, tabs, highlight, nearHomeBonus, top3Tabs`,
  `travel { zone, region, lat, lng, geoSource, geoQuery, distanceKm
  (curator-reference only), nearest<Station> }`,
  `google { rating, reviews }` (⭐ chip), `source { label, url }`.
- **Pipeline**: `geocode → fetch → verify → zones`, run from
  `scripts/friday-ingest.py`; discoveries land only in the
  `data/candidates.json` human review queue — **never auto-published**.
- **Verification**: `scripts/google-enrich.py` with a 30-day cache in
  `data/research/google-cache.json`; flags (closed / weak name match /
  low rating) are flagged, never deleted.
- **Build**: `js/app.part{0,1,2}.js` is ONE IIFE concatenated in order by
  `scripts/build-assets.py`; after edits, rebuild and bump `?v=` in
  `index.html`. Same for the CSS bundle.
- **Push**: git transport is blocked from this machine, so pushes go
  blobs → tree → commit → ref-update via the GitHub git-database REST API
  (`gh-push.py`); the PAT lacks Workflows scope, so **never touch
  `.github/workflows/*` via API**; never push/deploy without Marcus's
  explicit approval.
- **Product rules carried over**: editorial-curation-first (ratings are a
  signal, not the sort key), mobile-first PWA, honest UI copy (geo-failure
  notices with one-tap re-enter), live per-user distances recomputed from
  the visitor's own postcode (baked `distanceKm` never shown).

## 2. Zone design (proposed)

SE Queensland is sprawling, so Brisbane CBD plays the same role SG's
Central did — it would flood everything without a cap. Quotas mirror the
SG pattern (`Central:4 quota / 10 cap`):

| Zone | Quota | Cap | Notes |
|---|---|---|---|
| Brisbane CBD & Inner | 4 | 10 | Flood-guard, mirrors Central |
| North Brisbane | 2 | — | |
| South Brisbane | 2 | — | |
| East Brisbane | 2 | — | |
| West Brisbane | 2 | — | |
| Gold Coast | 3 | 6 | Big tourist zone, but capped |
| Sunshine Coast | 2 | 4 | |
| Moreton Bay | 2 | — | |
| Ipswich | 1 | — | |
| Logan | 1 | — | |
| Redlands | 1 | — | |

Zone assignment: lat/lng rectangles approximating LGAs in a QLD
`zones.py` (single source of truth, mirrored in the client's
`zoneFromLatLng`). Exact boundary rects will be drawn at build time and
shown to Marcus for sign-off before any data ships.

## 3. Geocoding — Queensland Geocoder (PLSplus-QG web service)

- Endpoint: `https://geocode.information.qld.gov.au/validate` (single +
  batch CSV). **Keyless, CC-BY-4.0**, returns address + locality +
  postcode + lat/lng + confidence + geocode type (building/parcel/access).
- Fragility: the service's own help says it "may be changed without
  notice"; some PLSplus API endpoints are agency-only. Mitigation: a
  response-validation layer in the geocode stage, plus fallback to
  Google Places Text Search (already connected) for odd cases.
- Runner-up rejected: Google Geocoding API — our `custom.google-places`
  credential is restricted to `places.googleapis.com`; Geocoding lives on
  `maps.googleapis.com` and would need new key/enablement.

## 4. Postcodes

- Validation: `^\d{4}$`, stored as string (leading zeros matter);
  QLD = `4000–4999`; anything outside warns as "outside Queensland coverage".
- Lookup: a prebuilt ~4,000-row QLD postcode→suburb→centroid CSV, refreshed
  yearly. (G-NAF is ~5GB unpacked — too heavy for the pipeline; Australia
  Post's postcode datafile is paid.) **Open question**: prebuilt file vs
  live lookup.

## 5. Event discovery (review queue only)

- **Primary — BCC "What's On"**: `data.qld.gov.au/dataset/brisbane-city-council-events`.
  Official, daily-updated, structured (dates, costs, booking, venue,
  location) via the Trumba Calendar API. Cleanest SISTIC replacement.
  (Exact Trumba feed URLs to be pulled from the dataset page at build time.)
- **Eventbrite AU**: same API as SG, location search by lat/lng — carried
  over unchanged; still needs the private `EVENTBRITE_TOKEN`.
- **Ticketek** (`premier.ticketek.com.au`): server-rendered search pages are
  fetchable without auth — usable as a **fragile review-queue candidate
  only** (legacy ASP.NET; ToS caveat). Same risk class as the old SISTIC
  endpoint.

### 5a. Follow-up investigation (2026-09-10 ~14:10 SGT, per Marcus's call)

- **Oztix** — verdict: **parked**. Individual event pages
  (`tickets.oztix.com.au/outlet/event/<uuid>`) render keyless without JS,
  but the main site is an Angular SPA with no verified machine-readable
  listing URL, no API, no RSS, no sitemap — events can't be *discovered*
  programmatically. ToS on scraping is unconfirmed. Not worth pipeline
  investment now; revisit if a listing URL is confirmed.
- **Gold Coast** — verdict: **included**. Two verified, official, keyless
  sources:
  (a) `whatsongoldcoast.au` (City of Gold Coast's official events site) —
  `/All-events/<slug>` pages server-render with dates, venue, address,
  price, categories (verified on a Burleigh Market page). Covers the
  Gold Coast zone blind spot. Same scrape-fragility class as SISTIC.
  (b) Council's Active & Healthy calendar (440 server-rendered results,
  query-param filters) — hundreds of free/low-cost activities for the
  outdoor/family angle.
- **ATDW ATLAS API (queensland.com / TEQ)** — verdict: **highest-value
  find, pending Marcus's call**. queensland.com events are fed by the
  Australian Tourism Data Warehouse; ATDW's documented distributor API
  (`https://developer.atdw.com.au`) serves JSON/XML with `latlong`+`dist`
  radius search (ideal per-zone queries), EVENT category filter, `delta`
  incremental updates, 5,000 records/call. Requires a **distributor API
  key** (registration via ATDW; trial terms/fees unconfirmed; may ask
  for an ABN; content must carry their tracking pixel). Statewide
  coverage — Gold Coast/Sunshine Coast zones benefit too. Fragile
  fallback: scraping queensland.com's locale-variant event pages.
  **Decision needed**: register the ATDW key, or skip for now?
- **Open**: Oztix (no machine access found), Gold Coast events (no open API
  confirmed), queensland.com / Visit Brisbane / TEQ (unconfirmed).
  Proposal: start with BCC + Eventbrite; Marcus decides whether Oztix /
  Gold Coast / TEQ warrant a feasibility check later.

## 6. Parks

Two builders, one `parks.json` schema (mirroring the NParks layer's
`id/name/travel/attractions/url/source` shape), **monthly refresh**:

- **BCC "Park — Locations"**: `data.qld.gov.au/dataset/park-locations` —
  2,180+ Brisbane parks with coordinates (CSV/GeoJSON, CC-BY).
- **QPWS state parks**: "Protected areas of Queensland" datasets on
  data.qld.gov.au (CC-BY-4.0) — polygon formats, so centroid/point
  extraction happens at build time.

## 7. Transport — TransLink GTFS

- SEQ feed: `https://gtfsrt.api.translink.com.au/GTFS/SEQ_GTFS.zip`
  (**verify the live URL at build time**). Keyless, CC-BY-4.0.
- Covers SEQ bus, **QR rail, Gold Coast light rail, and ferry**;
  `stops.txt` gives every stop/station with lat/lng.
- Nearest-station stamper: same haversine approach as the MRT stamper —
  rail parent stations + busway stations by name + ferry terminals.
- Fragility: portal metadata says "data last updated 14 Nov 2023" — looks
  like stale portal metadata rather than a stale feed; confirm freshness
  on first download.

## 8. Locale

- `Australia/Brisbane`: AEST = UTC+10, **no daylight saving** (like SG,
  fixed offset — simpler than DST states).
- Currency: **AUD** (`$` reads as AUD); card copy in Australian English.

## 9. Dropped

- The **Causeway traffic page** — no QLD equivalent; cut.
- SG constants: OneMap, SISTIC, MRT dataset, 6-digit postal regex,
  `SECTOR_ZONE` table.

## 10. Still needed from Marcus (decision list)

1. Approve the zone design, quotas, and caps (§2).
2. Postcode lookup: prebuilt centroid file vs live lookup?
3. Investigate Oztix / Gold Coast / TEQ event feeds, or skip for now?
4. `EVENTBRITE_TOKEN` — same private token as the SG pipeline (confirm
   still available).
5. Build-time verifications (not decisions): live GTFS URL, Trumba feed
   URLs, Queensland Geocoder response shape.

## 11. Repo note

`marcustayye93/Bean-There-QLD` is empty on `main` — first push via the
git-database REST API works from an empty base. GitHub Pages will need
enabling in repo Settings (like Marcus did for the Gnog app) before the
preview goes live.

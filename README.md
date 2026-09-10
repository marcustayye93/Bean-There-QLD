# The Queensland Adventure — app (v1)

A dependency-free, mobile-first web app: a Queensland kids/family weekend +
school-holiday activity finder. No build step — GitHub Pages serves the
static files as-is. No login; settings, favourites and plans live in the
browser's localStorage.

## Files

- `index.html` — structure: sticky header + holiday banner + tabs (Find / Saved / Plan),
  filter bar, settings and plan-date dialogs.
- `css/styles.css` — warm family aesthetic, teal/green palette, mobile-first.
- `js/app.js` — all logic. Pure helpers (dates, haversine, filtering, plan
  share encoding) are exported for node when `module` exists, so they can be
  unit-tested without a DOM: `node -e "const t = require('./js/app.js')"`.
- `manifest.webmanifest`, `icon.svg` — minimal PWA metadata.

## Data files consumed (built by the data pipeline)

- `data/activities.json` — `{ meta, activities: [...] }`. Each activity:
  `id, name, description, suburb, region, zone, age_min, age_max, category,
  indoor ("indoor"|"outdoor"|"both"), price_aud (0 = free, null = unknown),
  price_note, duration, booking_url (or null), booking_required, lat, lng,
  source {label, url}, live (false = SAMPLE, shown with a "Sample listing"
  badge), holiday_only, interests []`.
- `data/holidays.json` — `{ source_url, generated, periods: [...] }` with
  `{ name, type ("holiday"|"term"|"public_holiday"), start, end }`, dates
  inclusive `YYYY-MM-DD`. Powers the persistent holiday banner and the Plan
  tab's day list. Missing/degraded file: banner hides, Plan tab explains
  itself and still lists saved items.
- `data/postcodes.json` — `{ note, postcodes: { "4000": { suburb, lat, lng } } }`.
  If empty/missing and a postcode is set, the app shows an honest
  "couldn't pin your postcode" notice with a re-enter affordance and the
  travel filter degrades to "Any distance".

## Key behaviours

- Dual-age filter: "Suits both kids" (default), "Suits {younger} only",
  "Suits {older} only"; match rule `age_min <= age <= age_max`. Names/ages
  are editable settings; labels recompute live.
- Travel time: haversine from the postcode centroid at ~40 km/h, always
  labelled "est.". Buckets: under 15/30 min, under 1/2 hours, any.
- "Recommended for {child1 name}" row: child1's interests ∩ activity
  interests, suits child1's age, within the travel bucket.
- Favourites (heart) → Saved tab. Plan tab: assign a favourited activity to
  a date within a school-holiday block; empty days read "Nothing planned yet".
- Share: "Copy share link" (`#plan=<base64url JSON of [{id,date}]>`, loads on
  open with a confirm banner) and "Copy as text" (plain-text itinerary).
- Empty states are honest and offer one-tap alternatives (wider travel
  bucket, other child, reset) — never a blank screen.

## Local settings keys

`btq-settings` (children's names/ages/interests + postcode),
`btq-favourites` (activity ids), `btq-plan` ([{id, date}]).

## Data sources: live vs sample

Full ledger with URLs, licences and verification dates:
[`data/DATA_SOURCES.md`](data/DATA_SOURCES.md). Summary:

**Live (verified, traceable to the source):**
- Queensland Department of Education school-holidays ICS feed → `data/holidays.json`
  (school-holiday windows + public holidays; terms baked from DoE term dates;
  2027 windows from the DoE 2027 planner since the feed extends ~12 months).
- Brisbane City Council "Park — Locations" open data (CC-BY) → 50 live parks,
  `category: "playgrounds"`, free entry.
- Brisbane City Council "Swimming Pool locations" open data (CC-BY) → 22 live
  pools, `category: "water"` (prices not published in the dataset, so
  `price_aud: null` with "Entry fees may apply").

**Samples (`"live": false`, shown with a "Sample listing" badge — never
presented as real):** 3 Scouts, 3 MiniRoos soccer, 2 Basketball QLD,
2 holiday camps (PCYC, YMCA), 1 Lego, 1 craft. Each links to the official
finder/join page so a parent can find the real program. Descriptions claim
nothing beyond what the linked program page states; suburb is "Various",
coordinates are null.

**Deliberately deferred:** ATDW ATLAS distributor API (needs a distributor
key — best future upgrade for zoos/museums/theme parks); Eventbrite AU API
(needs `EVENTBRITE_TOKEN` in env, or the stored Eventbrite credential on this machine); Oztix (no machine listing URL); postcode
centroids (no free verifiable AU dataset — the app degrades honestly with
a "couldn't pin your postcode" notice).

## Event discovery (review queue)

`python3 scripts/fetch-events.py --all` sweeps two event sources into
`data/candidates.json` — the human review queue (`status: "proposed"`).
Nothing auto-publishes into `data/activities.json`; promote by hand.

- **BCC What's On (Trumba extract)** — keyless, runs immediately. 300
  candidates in a 21-day window, with age ranges, costs, booking flags,
  and coordinates mapped.
- **Eventbrite** — undocumented destination/search endpoint (the same one
  the eventbrite.com frontend uses), authenticated with Marcus's stored
  Eventbrite token via the eventbrite skill. Sweeps Brisbane, Gold Coast
  and Sunshine Coast with a family-biasing query and filters to the
  21-day window; 160 candidates on the first live run. Re-scrape
  destination place IDs with `--source eventbrite --refresh-places`.

See `data/DATA_SOURCES.md` ("File: `data/candidates.json`") for the
access, licence and fragility notes of each source.

## Adding an activity

1. Edit `data/activities.json` (or extend `scripts/build-data.py` if it comes
   from a live source) and add an object with all 21 fields — copy an existing
   entry. Required: `id` (unique slug), `name`, `description` (traceable to the
   source — never invented), `suburb`, `region`, `zone` (one of the 11 in
   `scripts/build-data.py`), `age_min`/`age_max` (0–16), `category`, `indoor`,
   `price_aud` (0 = free, null = unknown + honest `price_note`), `booking_url`
   (or null), `booking_required`, `lat`/`lng`, `source {label, url}`,
   `live` (true only if verified against the source), `holiday_only`,
   `interests []`.
2. Rule: if it isn't verified against a live source, set `"live": false` —
   it will render with the "Sample listing" badge.
3. Refresh the browser; no build step.

## Updating school holiday dates

Run `python3 scripts/build-data.py` — it re-fetches the DoE ICS feed and
rewrites `data/holidays.json` (also re-fetches the council datasets). Do this
once a year: the ICS feed extends ~12 months forward. The banner and planner
compute everything live from the file — no code changes needed. The script
warns if the Spring 2026 window moves again (the feed's school-weekday
framing differs by a day from the DoE planner PDF's calendar framing).

## Test

Pure-logic suite + stub-DOM interaction suite were run against mock data
(not shipped): 53 + 44 checks passing. Mocks live in `/tmp/btq-mock/`
(test data only — clearly labelled, never presented as real listings).

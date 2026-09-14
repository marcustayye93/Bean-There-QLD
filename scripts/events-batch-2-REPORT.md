# Events Batch 2 — Review Report (2026-09-14)

**REVIEW ONLY. Nothing was written to `data/activities.json`, nothing was pushed, nothing was published.**
Untouched files: `data/activities.json` (146 records), all app code, all other scripts.
This packet proposes `scripts/events-batch-2.json` for Marcus's review. It goes live only after his explicit approval of the exact list.

## Funnel

| Stage | Count |
|---|---|
| 2026-09-14 discovery refresh, new candidates | 335 |
| Full proposal queue at screening start | 838 |
| Date screen: start date on/after 2026-09-14 | 487 |
| Auto-drop: obvious adult / weak-fit | −182 |
| Manual review (chronological, `/tmp/batch2-review.txt`) | 305 |
| **KEPT for batch 2** | **27** |
| Dropped at manual review / verification | 278 |

Queue composition at screening: 563 Brisbane City Council (Trumba), 218 Eventbrite, 54 WeekendNotes, 3 Urban List.
Ticketmaster and Urban List discovery produced nothing new in the refresh.

## ⚠️ Time-sensitive: starts within 7 days (14–21 Sep)

Nine of the 27 start before 22 Sep — these lose value fastest if approval waits:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Tue 15 Sep | Lord Mayor's City Hall Concerts: East of West (Brisbane Festival) | Brisbane City | Free |
| Tue 15 Sep | Cosmic Collisions (Planetarium, recurring) | Mt Coot-tha | Child $11 |
| Tue–Thu 15–17 Sep | Bush Kindy: Kirra and Coco | Chermside West | Free |
| Thu 17 Sep | What's In The Woods? — Backbone Theatre For Babies (also Sat 19 + Thu 24 Sep) | Seven Hills | See listing |
| Fri 18 Sep | ILLUSIONS Magic Show | Surfers Paradise | A$69–A$129 |
| Sat–Sun 19–20 Sep | VietJet Redcliffe KiteFest | Clontarf | Free |
| Sun 20 Sep | School Holidays Kids Pizza Masterclass | Carrara | A$35 |
| Mon 21 Sep | School Holiday Slime Workshop | Flagstone | A$5 |
| Mon 21 Sep | Journey-stick Adventure | Tanawha | A$10 |

## Drop reasons (278 manual drops + 182 auto-drops)

| Reason | Count | Basis |
|---|---|---|
| Adult fitness classes (HIIT, yoga, aqua, tennis, martial arts, dance fitness) | large share | manual review |
| Recurring kids classes / weak-fit generic sessions (storytimes, Lego clubs, rhyme time, weekly workshops) | large share | manual review |
| Health, civic and support sessions (immunisation clinics, carers groups, JP signings, council meetings) | dozens | manual review |
| Already live in the app (DUP-LIVE vs the 25 live events) | 25 | name match vs `data/activities.json` |
| Adult-only entertainment (18+ shows, wine/beer events) | small | manual review |
| Outside Queensland (Sydney/Melbourne/NSW listings) | small | manual review |
| **Verification failures (would otherwise have been kept)** | **5** | page-level checks below |

## Verification method

- **BCC Trumba (4 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-09-14 (2,000 rows, `/tmp/bcc-fresh-2026-09-14.csv`). Event IDs, dates, venues, costs, age ranges and booking requirements all confirmed present in the fresh feed.
- **Eventbrite (22 keepers):** every page fetched with a browser user agent. Required: JSON-LD `eventStatus: EventScheduled`, startDate matching the expected date in Australia/Brisbane, no sold-out/ended/cancelled markers. 26 unique venues checked through Google Places; 24 OPERATIONAL, 1 suburb-level approximation ×2, 1 route-level match ×1 (see table). Raw dumps and the parse script are kept at `/tmp/eb-batch2/` for audit.
- **WeekendNotes (1 keeper):** article text fetched and read in full; dates 19–20 Sep 2026, Pelican Park Clontarf, free entry, explicit family programme. Venue confirmed OPERATIONAL on Google Places.
- **Prices:** taken from the page/feed text. Three Eventbrite free events carry `priceCurrency: USD` in their JSON-LD — they are free, so this is cosmetic only. Unknown prices stay `null` with "See official listing for ticket details."
- **Dates, venues, prices, coordinates, business details:** nothing invented. Multi-session events are folded into one record (TheatreDome 10am + 1pm; TurtleCare 8:30am + 10:30am; Meet Wildlife 10am + 11am) with sessions noted in the description. Recurring BCC occurrences follow batch-1 convention (date range or `date_end: null`).

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| East of West (Brisbane Festival) | 15 Sep | City Hall, feed-confirmed | Free, feed-confirmed | ✅ |
| Cosmic Collisions | from 15 Sep (recurring) | Planetarium, feed-confirmed | Child (3–14) $11, feed-confirmed | ✅ |
| What's In The Woods? | 17 / 19 / 24 Sep | Seven Hills Hub, feed-confirmed | See website → null | ✅ |
| Bush Kindy: Kirra and Coco | 15–17 Sep | Downfall Creek Bushland Centre, feed-confirmed | Free, feed-confirmed | ✅ |
| Redcliffe KiteFest | 19–20 Sep | Pelican Park, Clontarf — OPERATIONAL | Free entry, article-confirmed | ✅ |
| ILLUSIONS Magic Show | 18 Sep | ILLUSIONS Magic Theatre, Surfers Paradise — OPERATIONAL | A$69–A$129 | ✅ |
| TheatreDome | 23 Sep (2 sessions) | Brisbane City Hall — OPERATIONAL | Free | ✅ |
| Aunty Sharron and The Daughts | 22 Sep | Karawatha Forest Discovery Centre — OPERATIONAL | Free | ✅ |
| TurtleCare Hatchling Club | 22 Sep (2 sessions) | Wyanda Park, Warana — OPERATIONAL | A$10 | ✅ |
| Ellis and the Night Orchestra (Helensvale) | 24 Sep | Helensvale Library — OPERATIONAL | Free | ✅ |
| Ellis and the Night Orchestra (Nerang) | 24 Sep | Nerang Library — OPERATIONAL | Free | ✅ |
| Slime Workshop | 21 Sep | Flagstone Community Centre — OPERATIONAL | A$5 | ✅ |
| Journey-stick Adventure | 21 Sep | Maroochy Regional Bushland Botanic Garden — OPERATIONAL | A$10 | ✅ |
| Batty Bush Walk | 22 Sep | Downfall Creek Bushland Centre — OPERATIONAL | Free | ✅ |
| Meet Wildlife Neighbours | 25 Sep (2 sessions) | Boondall Wetlands Environment Centre — OPERATIONAL | Free | ✅ |
| Mini Marine Biologist | 25 Sep | Mudgeeraba, exact venue in confirmation email — suburb centroid | Free | ⚠️ approximate location |
| Wild about Whales | 24 Sep | Broadbeach, exact venue in confirmation email — suburb centroid | Free | ⚠️ approximate location |
| Pizza Masterclass | 20 Sep | Enzo's Cucina Carrara — OPERATIONAL | A$35 | ✅ |
| Gympie Cinema Family Movie Day | 4 Oct | Gympie Cinemas — OPERATIONAL | A$6.61 | ✅ |
| Starry Night screening: Babe | 2 Oct | Sundale Ltd, Burnside — OPERATIONAL (geocode resolved to adjacent Parklands address) | Free | ✅ |
| Make a Robotic Arm | 23 Sep | Pittsworth Library — OPERATIONAL | Free | ✅ |
| Voices in Colour with Chris Collin | 23 Sep | The Old Ambulance Station, Nambour — OPERATIONAL | A$5–A$10 | ✅ |
| Portrait Detectives | 22 Sep | State Library of Queensland — OPERATIONAL | Free | ✅ |
| Kangamoo & The Not New Crew | 29 Sep | Tewantin Noosa RSL — OPERATIONAL | A$5 | ✅ |
| Make AI Movies (5-day program) | 28 Sep – 2 Oct | The Precinct, Fortitude Valley — OPERATIONAL | A$160 | ✅ |
| MiniBoss Business Tour (ages 9–16) | 30 Sep – 1 Oct | Fortitude Valley ("Marshall Street") — route-level geocode match, not a business | A$580.62 | ⚠️ vague venue, steep price |
| Learn to DJ Workshop | 29 Sep | Mooloolaba Music — OPERATIONAL | Free | ✅ |

## Verification failures (dropped)

| Candidate | Reason |
|---|---|
| Junior Explorers: Bug Detectives (23 Sep) | Sold out |
| Koala Painting Kids Art Workshop (23 Sep) | Sold out |
| Sister City Children's Art Workshop (19 Sep) | Sold out |
| KRANK Kerbside Creatures (23 Sep) | Sold out |
| Full Day Kids Woodworking (28 Sep) | Venue is Behs Lane, Lynwood **NSW** — outside Queensland scope |

## Open questions and caveats

1. **MiniBoss Business Tour (A$580.62):** the steepest item in the batch, and its venue geocoded only to street level ("Marshall Street, Fortitude Valley"). It is a real, scheduled, kid-relevant (ages 9–16) event — but Marcus may want to cut it on price alone.
2. **NaturallyGC events (Mini Marine Biologist, Wild about Whales):** free and verified, but the organiser only discloses the exact meeting point in the confirmation email, so coordinates are suburb centroids. The description says this plainly.
3. **Sundale Starry Night:** page venue is Burnside; Google Places resolved to the adjacent Sundale Parklands address. Coordinates point at the precinct, not a wrong place.
4. **What's In The Woods? price:** BCC feed shows only "See website" — recorded as `null` per the unknown-price rule.
5. **Recurring records** (Cosmic Collisions `date_end: null`; Bush Kindy and What's In The Woods date ranges) follow batch-1 convention. The known `eventEnd()` null-handling quirk noted in batch 1 still applies and is intentionally not touched in this review-only packet.
6. **Zone boundary:** Flagstone (Slime Workshop) sits ~20m south of the Logan rectangle, so the zone function labels it "Queensland". Coordinates are exact; the label is a known coarseness of the zone grid.

## Files

- `scripts/events-batch-2.json` — 27 records, batch-1 schema, unique IDs, no overlap with the 146 live records.
- Evidence: `/tmp/bcc-fresh-2026-09-14.csv` (fresh BCC feed), `/tmp/batch2-eb-verify.json` (30 page verifications), `/tmp/eb-batch2/` (raw dumps + parse script), `/tmp/batch2-review.txt` (305-line manual review list).

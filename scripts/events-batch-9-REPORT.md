# PUBLISH PACKET — Events Batch 9

**Queensland Adventure — weekly discovery curation, Monday 2026-11-02 (Australia/Brisbane)**
**File:** `scripts/events-batch-9.json` — 10 records (2 Brisbane City Council Trumba, 8 Eventbrite)
**Status:** Verified batch for live publishing under Marcus's standing auto-publish rule (2026-09-14). Merge and push follow this packet.

---

## TIME-SENSITIVE — starts within 7 days, before 2026-11-09 (2 of 10)

Publish promptly or these lose value:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Tue 2026-11-03 | Lord Mayor's City Hall Concerts - Cinema & Standards: A Multi-Instrumental Tapestry | Brisbane City | Free |
| Wed 2026-11-04 | Gathering: Blak : Story : Song | Brisbane City | Free |

Later keepers (2026-11-10 to 2026-11-22): Ranger Stacey's Joey Club (Capalaba), Family day | Cardboard sculptures with Andy Siong (Logan Central), Lights, Camera, Action! (Mudgeeraba), Movie Night: Hoppers (Kalbar), AT THE ZOO - Preschool Show (Carbrook), Better Bike Maintenance (Pimpama), Training Wheels to Two Wheels (Pimpama) - Session 1, Santa Steam Express - Loop two departing at 11.42am (Brisbane City).

---

## Funnel

| Stage | Count |
|---|---:|
| Listings pipeline new candidates (`fetch-listings.py --all`) | 16 |
| Events pipeline new candidates (`fetch-events.py --all`) | 743 |
| **Combined new candidates this run** | **759** |
| Full proposal queue after both sequential runs | 5,877 |
| Date screen: start date on/after 2026-11-02 | 759 |
| Past-dated dropped at date screen | 0 |
| Unique titles after folding daily occurrences | 602 |
| Kid-signal shortlist after bulk-drop and fit screening | 14 (3 Trumba, 11 Eventbrite) |
| **Final keepers** | **10 (2 Trumba, 8 Eventbrite)** |

Pipelines ran sequentially, as required; no overwrite race. The listings run was clean: Ticketmaster 0 new from 85 unique events (6 API calls), The Urban List 2 candidates (0 new), WeekendNotes 40 candidates (16 new venue leads, none promoted this run — no verified date/venue in the candidate record, following the batch 1-8 pattern). The events run was clean: 298 new Trumba candidates from 2,000 BCC feed rows and 445 new Eventbrite candidates across Brisbane, Gold Coast and Sunshine Coast (891 candidates read, 36 pages).

## Drop reasons

Bulk manual drops from the 759 future-dated new candidates, following the batch 1-8 pattern:

| Reason | Basis |
|---|---|
| Adult fitness and Active & Healthy sessions (yoga, Pilates, Tai Chi, Zumba, aqua classes, HIIT, line dancing, martial arts terms) | large share, keyword screen of the chronological list |
| Seniors (50 Plus Centre program) and adult craft workshops (macramé, resin, pottery, candle and lamp making) | large share, keyword screen |
| Recurring library and kids programs (First 5 Forever storytimes, rhyme time, generic Bush Kindy, Music Beat kids groups, Create it library sessions, kids sports and term classes) | large share, keyword screen; the special themed sessions were shortlisted instead |
| Adult-only, business, health, civic and support sessions (networking, carer and peer support, immunisation clinics, singles and speed dating, Halloween bar parties, comedy clubs, professional courses, parent seminars such as the Baby & Toddler Sleep Masterclasses) | large share, keyword screen |
| Already live in the app | 23 candidates with an exact live name match (including repeat sessions of Stories You Wear: Magpie Goose, Little Artist's Eye Spy, Warrajamba, Clock Tower Tour, and new Eventbrite listings for the already-live Trinket Trove's Mini Market!, Bead Day at Trinket Trove!, Wheely Fun, Children's Bike Skills (Pimpama), BioBliz Belmont Hills, Sea Slug Survey and Meet the Rainforest Guided Walk) |
| Verification failures at page level | 2, listed below |
| Shortlist fit drops after verification | 2, listed below |

### Shortlist drops after verification (fit, duplicate or scope)

Abseiling (Kangaroo Point Cliffs Park, 2026-11-04, $6, ages 10+): verified in the fresh feed but dropped as a recurring Active & Healthy series (three dates in the feed window), following the batch 1-8 recurring-program rule. Little Potters - Christmas Wreath Ceramic Workshop (Thornlands, 2026-11-22, A$120): page live and on sale, but the page states no child suitability, so it was dropped rather than inventing a kids fit, following the batch 1-8 rule used for Chasing Shadows and the Spring Pademelon Survey.

## Verification method

- **BCC Trumba (2 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-11-02 (2,000 rows). Every keeper was matched by subject, date, venue, cost, age text and geolocation in the fresh feed. Coordinates come from the feed geolocation column. The Lord Mayor's concert series recurs weekly but each concert is a distinct program, following the batch 8 precedent; Gathering: Blak : Story : Song appears once in the feed window.
- **Eventbrite (8 keepers):** all 11 shortlisted pages were fetched with a Chrome browser user agent. Eventbrite's JSON-LD Event block is no longer present on every page, so where it was absent the page's embedded __NEXT_DATA__ record was used instead, with the same bar: event status live, sales status on_sale, a start date in Australia/Brisbane matching the expected date, and a venue record with coordinates. Prices come from the JSON-LD AggregateOffer lowPrice/highPrice or the page offers record. The words "sold out" in page text were not trusted; only the structured availability/sales field decided.
- **Google Places:** every Eventbrite keeper venue was searched and confirmed OPERATIONAL (IndigiScapes Centre Capalaba, Logan Art Gallery, Kalbar School of Arts & Memorial Hall, Clover Hill State School, Calvary Christian College Carbrook, Pimpama Sports Hub, Roma Street Station). Note: the Maleny Christmas Markets listing was dropped because its page venue record is in Gympie, not Maleny (see below).
- **Prices:** 6 of 10 are free. Paid keepers are taken honestly from the source: Family day cardboard sculptures A$5, Movie Night: Hoppers from A$10 (offer range A$10-A$38.37), AT THE ZOO - Preschool Show from A$17.19 (offer range A$17.19-A$38.37), Santa Steam Express from A$7 (offer range A$7-A$15).
- **Dates, venues, prices, coordinates, business details:** nothing invented. Australian English, AUD, Australia/Brisbane throughout.

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| Lord Mayor's City Hall Concerts - Cinema & Standards: A Multi-Instrumental Tapestry | 2026-11-03 | Brisbane City Hall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Gathering: Blak : Story : Song | 2026-11-04 | Queen Street Mall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Ranger Stacey's Joey Club | 2026-11-10 | IndigiScapes Centre, Capalaba — OPERATIONAL | Free, on_sale, last Joey Club of the year | ✅ |
| Family day \| Cardboard sculptures with Andy Siong | 2026-11-14 | Logan Art Gallery — OPERATIONAL | A$5, on_sale, 2-hour workshop | ✅ |
| Lights, Camera, Action! | 2026-11-21 | Clover Hill State School, Mudgeeraba — OPERATIONAL | Free, InStock, Drama Club family showcase | ✅ |
| Movie Night: Hoppers | 2026-11-21 | Kalbar School of Arts & Memorial Hall — OPERATIONAL | From A$10, InStock, family movie night | ✅ |
| AT THE ZOO - Preschool Show | 2026-11-22 | Calvary Christian College, Carbrook — OPERATIONAL | From A$17.19, InStock, preschool dance showcase | ✅ |
| Better Bike Maintenance (Pimpama) | 2026-11-22 | Pimpama Sports Hub — OPERATIONAL | Free, on_sale, family friendly workshop | ✅ |
| Training Wheels to Two Wheels (Pimpama) - Session 1 | 2026-11-22 | Pimpama Sports Hub — OPERATIONAL | Free, on_sale, ages 4+ | ✅ |
| Santa Steam Express - Loop two departing at 11.42am | 2026-11-22 | Roma Street Station, Platform 3 — OPERATIONAL | From A$7, on_sale, 40-minute return loop | ✅ |

## Verification failures (dropped)

| Candidate | Date | Failure |
|---|---|---|
| Sensory friendly sessions (The Corner, State Library) | 2026-11-08 | Structured `offers.availability: SoldOut` (fifth week running) |
| Maleny Handmade and Artisan Christmas Markets | 2026-11-13 | Page venue record is 39 Monkland Street, Gympie, not Maleny — title and venue do not match, so the event cannot be geocoded honestly |

## Caveats

1. **2 of 10 records start within 7 days**, on Tue 2026-11-03 and Wed 2026-11-04. Merge promptly.
2. **Santa Steam Express** runs three return loops on Sun 2026-11-22; this record is loop two only (page start 11:30, departure 11:42am). The app does not store a start time.
3. **Movie Night: Hoppers** is in Kalbar (Scenic Rim), outside the usual Brisbane/Gold Coast/Sunshine Coast footprint; it is recorded with region and zone "Queensland" per the app's own taxonomy, since the listing came through the discovery search.
4. **AT THE ZOO - Preschool Show** is performed by preschool dancers for a family audience; its age range is recorded 0-16 as a family show.
5. **Eventbrite verification method change:** JSON-LD Event blocks are missing from some current Eventbrite pages. For those pages the embedded __NEXT_DATA__ record (status live, salesStatus on_sale, venue coordinates) was used at the same bar, and the method is recorded here so the next run does not mistake the missing JSON-LD for a verification failure.
6. Eventbrite times were read with +10:00 (AEST). Durations are coarse buckets per batch 1-8 convention.

## Files

- `scripts/events-batch-9.json` — 10 records, batch 1-8 schema (26 fields), unique IDs, no overlap with the 336 records in `data/activities.json`.
- Evidence (internal, under the goal workspace): fresh BCC CSV, 11 Eventbrite page dumps with a JSON-LD/__NEXT_DATA__ verification summary, Google Places results, the chronological review lists and the batch builder, all in `~/workspace/goals/the-queensland-adventure-app/hidden_files/batch9-2026-11-02/`.

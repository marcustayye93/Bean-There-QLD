# PUBLISH PACKET — Events Batch 11

**Queensland Adventure — weekly discovery curation, Monday 2026-11-16 (Australia/Brisbane)**
**File:** `scripts/events-batch-11.json` — 22 records (3 Brisbane City Council Trumba, 19 Eventbrite)
**Status:** Verified batch for live publishing under Marcus's standing auto-publish rule (2026-09-14). Merge and push follow this packet.

---

## TIME-SENSITIVE — starts within 7 days, before 2026-11-23 (6 of 22)

Publish promptly or these lose value:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Tue 2026-11-17 | Bush Kindy: Bugs in my Backyard (Downfall Creek) | Chermside West | Free |
| Tue 2026-11-17 | Lord Mayor's City Hall Concert - What a Wonderful World | Brisbane City | Free |
| Wed 2026-11-18 | Gathering: Georgia Corowa | Brisbane City | Free |
| Thu 2026-11-19 | Gowonda Dreaming | Tamborine Mountain | From A$5 |
| Fri 2026-11-20 | Illusions Magic Show - Surfers Paradise | Surfers Paradise | From A$69 |
| Sun 2026-11-22 | Santa Steam Express - Loop three departing at 1:12pm | Brisbane City | From A$7 |

Later keepers (2026-11-23 to 2026-12-06): Family Zumba (Caboolture), Great Southern Bioblitz Spotlight Night (Springfield Lakes), Tamborine's Biggest Christmas Twilight Market 2026 (Tamborine), Free Santa Photos (Moorooka), Sleighbells & Showstoppers (Woolloongabba), Kokoda Youth Foundation Golf Family Fun Day (Raceview), Christmas Movies: Shrek (Mudgeeraba), Christmas Ornaments (South Brisbane), A Very Merry Singalong! (Burleigh Waters), Sundale Community Christmas Carols (Nambour), DIY Craftmas Workshops (BNE Southside) (Moorooka), Harmony Christmas by Candlelight (Palmview), Children's Bike Skills (Miami) (Miami), Christmas Family Nights at Southport Sharks (Southport), Batty Boat Christmas Cruise 2026 (South Brisbane), Wonka Showskate (Albany Creek).

---

## Funnel

| Stage | Count |
|---|---:|
| Listings pipeline new candidates (`fetch-listings.py --all`) | 0 |
| Events pipeline new candidates (`fetch-events.py --all`) | 700 |
| **Combined new candidates this run** | **700** |
| Full proposal queue after both sequential runs | 7,355 |
| Date screen: start date on/after 2026-11-16 | 700 |
| Past-dated dropped at date screen | 0 |
| Undated WeekendNotes leads (no verified date/venue, not promoted) | 0 |
| Unique titles after folding daily occurrences | 542 |
| Kid-signal shortlist after bulk-drop and fit screening | 32 (5 Trumba, 27 Eventbrite) |
| **Final keepers** | **22 (3 Trumba, 19 Eventbrite)** |

Pipelines ran sequentially, as required; no overwrite race. The listings run was clean: Ticketmaster 2 candidates (0 new from 77 unique events), The Urban List 0 candidates (HTTP 403 Forbidden, source-only error), WeekendNotes 0 candidates. The events run was clean: 296 new Trumba candidates from 2,000 BCC feed rows and 404 new Eventbrite candidates across Brisbane, Gold Coast and Sunshine Coast (922 candidates read, 36 pages).

## Drop reasons

Bulk manual drops from the 700 future-dated new candidates, following the batch 1-10 pattern:

| Reason | Basis |
|---|---|
| Adult fitness and Active & Healthy sessions (yoga, Pilates, Tai Chi, Zumba, aqua classes, HIIT, line dancing, martial arts terms) | large share, keyword screen of the chronological list |
| Seniors (50 Plus Centre program) and adult craft workshops (macramé, resin, pottery, candle and lamp making) | large share, keyword screen |
| Recurring library and kids programs (First 5 Forever storytimes, rhyme time, toddler time, generic Bush Kindy, Music Beat kids groups, Create it library sessions, Family STEAM, kids sports and term classes) | large share, keyword screen; the special themed sessions were shortlisted instead |
| Adult-only, business, health, civic and support sessions (networking, carer and peer support, immunisation clinics, singles and speed dating, comedy clubs, professional courses, parent seminars) | large share, keyword screen |
| Already live in the app | 20 candidates with an exact live name match (Stories You Wear: Magpie Goose, Little Artist's Eye Spy, Warrajamba, Clock Tower Tour, Journey to the Stars, NDIS Capoeira class - Kids, Wheely Fun, Kids Beginner Crochet Class, Park after Dark: Spotlighting, Training Wheels to Two Wheels (Miami) - Session 1, Sea Slug Survey in the Rocky Shores) |
| Past-dated at date screen | 0 |
| Verification failures at page level | 1, listed below |
| Shortlist fit drops after verification | 9, listed below |

### Shortlist drops after verification (fit, duplicate or scope)

Gumtreekids Messy Play - Baby only session (Love Street Park, Bulimba, 2026-11-16, ages 6 months to walkers): verified in the fresh feed but dropped as a recurring series (second session 2026-11-23, Mixed theme, George Clayton Park), following the batch 9 Abseiling and batch 10 Bazil Grumble precedents. Family STEAM (Bracken Ridge Library, 2026-11-17): verified in the fresh feed but dropped as a recurring library program (five dates across libraries in the feed window). Junior Bike Skills (Coorparoo, 2026-12-05, free, ages 5-10): structured JSON-LD offers availability SoldOut, listed under verification failures below. Kids Creative (Laidley, 2026-11-19, A$10): a kids creative hour, but Laidley (Lockyer Valley) is outside the app's Brisbane / Gold Coast / Sunshine Coast footprint. Fun Factory: Origami Card Making (Toowoomba City Library, 2026-12-05, free, ages 5-12): same, Toowoomba is outside the footprint. Festive bunting (2026-12-01, A$55): the page carries no venue record or coordinates, so the venue cannot be verified without inventing it. Cello Christmas Concert 2026 (Ashmore, 2026-11-22): a student recital for performers' families, with no ticket price or availability data on the page. Creative Club with Kate Lardner (Tallebudgera Valley, 2026-11-30, A$38.37, ages 6-11): fortnightly recurring series, five sessions in Term 4, following the batch 9 recurring precedent. International Day of People with Disability 2026 (Milton, 2026-12-03, A$50): a professional and community audience (business owners, organisation representatives), not a family outing. Recycle Christmas Decorations (Nambour, 2026-12-01): a carers' support-group craft session, adult audience. Healthcare for a Day (2026-11-19): a career taster for students, following the batch 10 Doctor For A Day precedent. SociABILITY: An Inclusive Social Group for Under 18s (2026-11-19): a teen drop-in social group with no activity detail, following the batch 10 Youth Night precedent.

## Verification method

- **BCC Trumba (3 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-11-16 (2,000 rows). Every keeper was matched by subject, date, venue, cost, age text and geolocation in the fresh feed. Coordinates come from the feed geolocation column. The Lord Mayor's concert series recurs weekly but each concert is a distinct program, following the batch 8 precedent. Bush Kindy: Bugs in my Backyard runs at three venues on three days (Downfall Creek 17 Nov, Karawatha 18 Nov, Boondall Wetlands 19 Nov); the Downfall Creek session is recorded, following the batch 1-10 precedent of recording one venue-dated session of a touring special.
- **Eventbrite (19 keepers):** all 27 shortlisted pages were fetched with a Chrome browser user agent. Eventbrite's JSON-LD Event block is present on only some current pages, so where it was absent the page's embedded __NEXT_DATA__ record was used instead, with the same bar: event status live, sales status on_sale, a start date in Australia/Brisbane matching the expected date, and a venue record with coordinates. Prices come from the JSON-LD AggregateOffer lowPrice/highPrice or the __NEXT_DATA__ seo.offersSchema lowPrice/highPrice (AUD, fee-inclusive low price per batch 1-10 convention). The words "sold out" in page text were not trusted; only the structured availability/sales field decided. The one exception proves the rule: Junior Bike Skills shows salesStatus on_sale in __NEXT_DATA__ but its structured JSON-LD offers availability is SoldOut, so it was dropped.
- **Google Places:** every Eventbrite keeper venue was searched and confirmed OPERATIONAL (Roma Street station Platform 3, Illusions Magic Theatre Surfers Paradise, Tamborine Mountain State School, 24 Wanderer Crescent Springfield Lakes, Bearded Dragon Hotel Tamborine, Alma Kids Moorooka, Metro Community Hub Hall Woolloongabba, Ipswich Golf Driving Range, Boomerang Hills Mudgeeraba, The Edge State Library Queensland South Brisbane, Burleigh Waters Library, Sundale Ltd Nambour, Clubhouse Moorooka, Flintwood Crescent Park Palmview, Pizzey Park Miami, Southport Sharks, Cultural Centre Pontoon South Brisbane, Skateaway Albany Creek, Caboolture Memorial Hall).
- **Prices:** 10 of 22 are free (price_aud 0). Paid keepers are taken honestly from the source: Gowonda Dreaming from A$5, Great Southern Bioblitz Spotlight Night from A$6.61, Santa Steam Express from A$7 (children 4-15; adults A$15), Family Zumba A$8.50, Kokoda Youth Foundation Golf Family Fun Day from A$15, Christmas Movies: Shrek A$17.19, Wonka Showskate from A$17 (children; adults A$20), Sleighbells & Showstoppers A$20.37, Batty Boat Christmas Cruise from A$27.78, DIY Craftmas Workshops (BNE Southside) A$36, Christmas Ornaments A$55, Illusions Magic Show from A$69 (kids; adults A$99). Christmas Family Nights at Southport Sharks is free for children 3 and under; buffet A$28.90 per child (4-12), A$54.90 per adult.
- **Dates, venues, prices, coordinates, business details:** nothing invented. Australian English, AUD, Australia/Brisbane throughout.

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| Bush Kindy: Bugs in my Backyard (Downfall Creek) | 2026-11-17 | Downfall Creek Bushland Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Lord Mayor's City Hall Concert - What a Wonderful World | 2026-11-17 | Brisbane City Hall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Gathering: Georgia Corowa | 2026-11-18 | Queen Street Mall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Gowonda Dreaming | 2026-11-19 | Tamborine Mountain State School — OPERATIONAL | From A$5, on_sale, school play | ✅ |
| Illusions Magic Show - Surfers Paradise | 2026-11-20 | Illusions Magic Theatre — OPERATIONAL | From A$69, on_sale, family outing | ✅ |
| Santa Steam Express - Loop three departing at 1:12pm | 2026-11-22 | Roma Street station, Platform 3 — OPERATIONAL | From A$7, on_sale, loop 3 only | ✅ |
| Family Zumba | 2026-11-23 | Caboolture Memorial Hall — OPERATIONAL | A$8.50, on_sale, family fitness | ✅ |
| Great Southern Bioblitz Spotlight Night | 2026-11-27 | 24 Wanderer Crescent, Springfield Lakes — address-confirmed | From A$6.61, on_sale, families | ✅ |
| Tamborine's Biggest Christmas Twilight Market 2026 | 2026-11-27 | Bearded Dragon Hotel, Tamborine — OPERATIONAL | Free, on_sale, kids' shows + pony rides | ✅ |
| Free Santa Photos | 2026-11-28 | Alma Kids, Moorooka — OPERATIONAL | Free, on_sale | ✅ |
| Sleighbells & Showstoppers | 2026-11-28 | Metro Community Hub Hall, Woolloongabba — OPERATIONAL | A$20.37, on_sale | ✅ |
| Kokoda Youth Foundation Golf Family Fun Day | 2026-11-29 | Ipswich Golf Driving Range — OPERATIONAL | From A$15, on_sale, family fun day | ✅ |
| Christmas Movies: Shrek | 2026-12-02 | Boomerang Hills, Mudgeeraba — OPERATIONAL | A$17.19, on_sale, lawn screening | ✅ |
| Christmas Ornaments | 2026-12-02 | Innovation Lab, The Edge, South Brisbane — OPERATIONAL | A$55, on_sale, under-16s with guardian | ✅ |
| A Very Merry Singalong! | 2026-12-03 | Burleigh Waters Library — OPERATIONAL | Free, on_sale | ✅ |
| Sundale Community Christmas Carols | 2026-12-04 | Sundale Ltd, Nambour — OPERATIONAL | Free, on_sale, Santa Zone gift per child | ✅ |
| DIY Craftmas Workshops (BNE Southside) | 2026-12-05 | Clubhouse Moorooka — OPERATIONAL | A$36, on_sale, festive bon-bons | ✅ |
| Harmony Christmas by Candlelight | 2026-12-05 | Flintwood Crescent Park, Palmview — OPERATIONAL | Free, on_sale, carols + Santa + ice cream | ✅ |
| Children's Bike Skills (Miami) | 2026-12-06 | Pizzey Park, Miami — OPERATIONAL | Free, on_sale, ages 6+ | ✅ |
| Christmas Family Nights at Southport Sharks | 2026-12-06 | Southport Sharks — OPERATIONAL | Free under-3s; buffet from A$28.90, first of 3 Sundays | ✅ |
| Batty Boat Christmas Cruise 2026 | 2026-12-06 | Cultural Centre Pontoon, South Brisbane — OPERATIONAL | From A$27.78, on_sale, baby bats + kids' crafts | ✅ |
| Wonka Showskate – A Magical Evening of Skating! | 2026-12-06 | Skateaway, Albany Creek — OPERATIONAL | From A$17, on_sale, first of 2 shows | ✅ |

## Verification failures (dropped)

| Candidate | Date | Failure |
|---|---|---|
| Junior Bike Skills (Coorparoo) | 2026-12-05 | Structured JSON-LD offers `availability: SoldOut`, although __NEXT_DATA__ salesStatus still reads on_sale |

## Caveats

1. **6 of 22 records start within 7 days**, on Tue 2026-11-17 (x2), Wed 2026-11-18, Thu 2026-11-19, Fri 2026-11-20 and Sun 2026-11-22. Merge promptly; the two Tuesday keepers are tomorrow.
2. **Santa Steam Express** runs three loops on Sun 2026-11-22; this record is loop three only (boarding 12:55pm, depart 1:12pm, back about 2:15pm). The app does not store a start time.
3. **Wonka Showskate** runs two shows (Sun 6 and Mon 7 December); this record is Sunday 6 December, 5:30pm only.
4. **Christmas Family Nights at Southport Sharks** runs three Sundays (6, 13 and 20 December); this record is 6 December only.
5. **Bush Kindy: Bugs in my Backyard** runs at three venues on consecutive days; this record is the Downfall Creek session on Tue 2026-11-17 at 10:00am, booked via the Eventbrite listing for that session.
6. **Junior Bike Skills (Coorparoo)** is sold out and was dropped; the Miami Children's Bike Skills session is a different event and is included.
7. **Christmas Family Nights at Southport Sharks** pricing is taken from the page text: children 3 and under free, buffet A$28.90 per child (4-12), A$54.90 per adult. The structured offer range (A$0-A$57.56) is the fee-inclusive equivalent.
8. **Scenic Rim** is a new region value in the app (Tamborine Mountain, Tamborine); the app's zone logic places both in the Gold Coast zone.
9. Eventbrite times were read with +10:00 (AEST). Durations are coarse buckets per batch 1-10 convention.

## Files

- `scripts/events-batch-11.json` — 22 records, batch 1-10 schema (26 fields), unique IDs, no overlap with the 364 records in `data/activities.json`.
- Evidence (internal, under the goal workspace): fresh BCC CSV, 27 Eventbrite page dumps with a JSON-LD/__NEXT_DATA__ verification summary, Google Places results, the chronological review lists and the batch builder, all in `~/workspace/goals/the-queensland-adventure-app/hidden_files/batch11-2026-11-16/`.

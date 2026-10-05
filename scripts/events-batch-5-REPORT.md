# PUBLISH PACKET — Events Batch 5

**Queensland Adventure — weekly discovery curation, Monday 2026-10-05 (Australia/Brisbane)**
**File:** `scripts/events-batch-5.json` — 25 records (9 Brisbane City Council Trumba, 15 Eventbrite, 1 Ticketmaster)
**Status:** Verified batch for live publishing under Marcus's standing auto-publish rule (2026-09-14). `data/activities.json` untouched at report writing; merge and push follow this packet.

---

## TIME-SENSITIVE — starts within 7 days, before 2026-10-12 (10 of 25)

Publish promptly or these lose value:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Tue 2026-10-06 | Bush Kindy: Australian Wildlife Week (Karawatha) | Karawatha | Free |
| Tue 2026-10-06 | Bush Kindy: Australian Wildlife Week (Downfall Creek) | Chermside West | Free |
| Tue 2026-10-06 | Lord Mayor's City Hall Concerts - Love, Life & Song: An Operatic Love Story - Jud Arthur | Brisbane City | Free |
| Wed 2026-10-07 | Gathering: Toni Janke | Brisbane City | Free |
| Wed 2026-10-07 | Food Truck Feasts | Brisbane City | Free entry |
| Wed 2026-10-07 – Sun 2026-10-25 | Audrey Gibbs Art Prize | Petrie Terrace | Free |
| Thu 2026-10-08 | Bush Kindy: Australian Wildlife Week (Boondall) | Boondall | Free |
| Thu 2026-10-08 | Bead Day at Trinket Trove! | Indooroopilly | Free |
| Fri 2026-10-09 – Wed 2026-10-14 | 2026 Recovered Futures ArT Exhibition | Brisbane City | Free |
| Fri 2026-10-09 | Bands in Parks: Twilight Jazz by the River | South Brisbane | Free |

Later keepers (2026-10-17 to 2026-12-23): Waterbug Sampling Currumbin, Halloween painting afternoon Redcliffe, Chinese Cultural Experience Day UQ, Breakfast with Ranger Stacey (ages 12+), preschool pipette painting at Logan Art Gallery, Baringa Family Music Bingo, BioBliz Belmont Hills, Children's Week Family Fun Day, Diwali Festival Pimpama, Logan BookFest, Monster Truck Mayhem Beaudesert, Spring Family Carnival Camp Hill, UQ Sport Aquatic Family Fun Day, Flicks & Fireworks Surfers Paradise, and The Christmas Spectacular (Fortitude Valley, 23 Dec, two sessions folded into one record).

---

## Funnel

| Stage | Count |
|---|---:|
| Listings pipeline new candidates (`fetch-listings.py --all`) | 2 |
| Events pipeline new candidates (`fetch-events.py --all`) | 663 |
| **Combined new candidates this run** | **665** |
| Full proposal queue after both sequential runs | 2,936 |
| Date screen: start date on/after 2026-10-05 | 664 |
| Past-dated dropped at date screen | 1 (Botanic By Night: NightGlow occurrence, 2026-09-30) |
| Unique titles after folding daily occurrences | 503 |
| Broad verification shortlist | 53 (17 Trumba, 34 Eventbrite, 2 Ticketmaster) |
| **Final keepers** | **25 (9 Trumba, 15 Eventbrite, 1 Ticketmaster)** |

Pipelines ran sequentially, as required. The listings run reported one source error: The Urban List returned `HTTP Error 403: Forbidden` (0 candidates from that source this week; Ticketmaster produced the 2 new candidates, WeekendNotes 0). The events run was clean: 295 new Trumba candidates from 2,000 BCC feed rows and 368 new Eventbrite candidates across Brisbane, Gold Coast and Sunshine Coast.

## Drop reasons

Bulk manual drops from the 664 future-dated new candidates, following the batch 1-4 pattern:

| Reason | Basis |
|---|---|
| Adult fitness and Active & Healthy sessions (yoga, Pilates, Tai Chi Qigong, Zumba Gold, aqua classes, HIIT, line dancing, martial arts terms) | large share, manual review of the chronological list |
| Recurring library and kids programs (storytimes, rhyme time, generic Bush Kindy, kids sports, music groups, playgroups, term classes and tasters) | large share, manual review |
| Adult-only, business, health, civic and support sessions (networking breakfasts, carer and peer support, immunisation clinics, speed dating, comedy clubs, wine and party events, professional courses) | large share, manual review |
| Already live in the app | 34 candidates with an exact live name match, plus the Lord Mayor's Photographic Awards 2026 exhibition occurrences (same program as the live `evt-photographic-awards` record) |
| Verification failures at page level | 2 Eventbrite sold-out drops, below |
| Shortlist fit drops after verification | 26, listed below |

### Shortlist drops after verification (fit, duplicate or scope)

Brisbane Writers Festival (feed age range young adults/adults/seniors); Visible Ink youth stage Rosa Quant and Live-at-MoB style music (weak kid hook); Aussie Kidz Charity Twilight (adult fundraiser, feed age field "all ages 18+"); Brisbane Blaze hockey (spectator match, price unpublished, weak fit kept out to keep the batch tight); rock climbing, companion planting (16+) and ghost stories (12+, night cemetery tour) Active & Healthy and adult sessions; generic weekly Bush Kindy at Karawatha (the special Australian Wildlife Week sessions were kept instead); Trinket Trove's weekly Mini Market; Strings Attached (adult orchid-ecology performance); Creative Club and Nature Club Living Tapestry tasters (recurring term-club enrolment sessions, ages 6-11, drop-off); Youth Sewing Moorooka (weekly class); Basketball Skills Camp Northside Wizards (open to all players, no kid age stated); Sea Slug Survey Burleigh (general citizen science, and the live Annual Sea Slug Count on 2026-10-09 already covers this program); NaturallyGC Bird Count and eDNA Survey (general adult citizen science, not a Kids session); three Green Leaves Early Learning family fun open days (childcare centre enrolment marketing); Halloween Party at SPEC (bar, 6pm to midnight); Palloween Wildlife Fundraiser (adult Halloween party); Bernard Composer's Halloween Christmas Special ("murder ballads"); Escape room at Hijinx Hotel (adult venue); ILLUSIONS Magic Show 2026-10-09 (duplicate of the live theatre show record); Chinese-cultural and other adult craft workshops in the wider queue (Turkish lamps, macramé, pottery, candle making) were dropped in bulk manual review.

## Verification method

- **BCC Trumba (9 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-10-05 (2,000 rows). Every keeper was matched by subject, date, venue, cost, age text and geolocation in the fresh feed. Coordinates come from the feed geolocation column. Exhibition runs were derived from feed occurrences: Audrey Gibbs Art Prize runs on gallery days 2026-10-07 to 2026-10-25; Recovered Futures is listed 2026-10-09 to 2026-10-14 in its description (feed end is midnight 2026-10-15).
- **Eventbrite (15 keepers):** all 34 shortlisted pages were fetched with a Chrome browser user agent. Every keeper shows JSON-LD `eventStatus: https://schema.org/EventScheduled`, a `startDate` in Australia/Brisbane matching the expected date, and structured `offers.availability: InStock`. Prices come from the JSON-LD AggregateOffer or the page ticket text. The words "sold out" in page text were not trusted; only the structured availability field decided.
- **Ticketmaster (1 keeper):** the two official Discovery API candidates for The Christmas Spectacular at The Fortitude Music Hall (2pm and 6:30pm, Wednesday 2026-12-23) were folded into one record with both sessions in the description. The API candidate published venue coordinates but no price range, so `price_aud` is null.
- **Google Places:** every Eventbrite keeper venue, plus The Fortitude Music Hall, was searched and confirmed `businessStatus: OPERATIONAL`. Exceptions and approximations, all noted on the records: Chinese Cultural Experience Day is on the University of Queensland St Lucia campus (the listing venue is "Grassy knoll", so the campus location is used); Flicks & Fireworks is on Surfers Paradise beach at the Surfers Paradise Sign on the Esplanade; Spring Family Carnival is at the Camp Hill chapel of The Church of Jesus Christ of Latter-day Saints, confirmed at 22 Sylvia Street.
- **Prices:** 19 of 25 are free. Paid keepers are taken honestly from the page: Halloween painting A$11.90, Chinese Cultural Experience Day A$10, Breakfast with Ranger Stacey A$60, Baringa Family Music Bingo A$15, and Monster Truck Mayhem at page-text face prices (kids 2-14 $35, adults $55, family $170). The Christmas Spectacular price is unpublished in the source and stays null with "See official listing for ticket details".
- **Dates, venues, prices, coordinates, business details:** nothing invented. Australian English, AUD, Australia/Brisbane throughout.

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| Bush Kindy: Australian Wildlife Week (Karawatha) | 2026-10-06 | Karawatha Forest Discovery Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Bush Kindy: Australian Wildlife Week (Downfall Creek) | 2026-10-06 | Downfall Creek Bushland Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Bush Kindy: Australian Wildlife Week (Boondall) | 2026-10-08 | Boondall Wetlands Environment Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Lord Mayor's City Hall Concerts: Jud Arthur | 2026-10-06 | Brisbane City Hall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Gathering: Toni Janke | 2026-10-07 | Queen Street Mall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Food Truck Feasts | 2026-10-07 | Roma Street Parkland, feed-confirmed | Free entry, feed-confirmed | ✅ |
| Audrey Gibbs Art Prize | 2026-10-07 – 2026-10-25 | Petrie Terrace Gallery, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| 2026 Recovered Futures ArT Exhibition | 2026-10-09 – 2026-10-14 | King George Square, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Bands in Parks: Twilight Jazz by the River | 2026-10-09 | Queensland Maritime Museum Park, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Bead Day at Trinket Trove! | 2026-10-08 | Trinket Trove, Indooroopilly — OPERATIONAL | Free, InStock, all ages | ✅ |
| Waterbug Sampling - Currumbin | 2026-10-17 | Long Tan Park, Currumbin Valley — OPERATIONAL | Free, InStock, all ages | ✅ |
| Halloween painting afternoon | 2026-10-18 | Suttons Beach, Redcliffe — OPERATIONAL | A$11.90, InStock | ✅ |
| Chinese Cultural Experience Day | 2026-10-21 | University of Queensland St Lucia — OPERATIONAL (campus) | A$10, InStock, all ages | ✅ campus venue |
| Breakfast with Ranger Stacey and friends | 2026-10-23 | Redlands IndigiScapes Centre, Capalaba — OPERATIONAL | A$60, InStock, ages 12+ | ✅ |
| Let's get arty for preschoolers: Pipette painting | 2026-10-23 | Logan Art Gallery — OPERATIONAL | Free, InStock, preschoolers | ✅ |
| Baringa Family Music Bingo | 2026-10-24 | Baringa State Secondary College — OPERATIONAL | A$15, InStock, all ages | ✅ |
| BioBliz Belmont Hills | 2026-10-24 | Belmont Hills Reserve, Carindale — OPERATIONAL | Free, InStock, family-friendly | ✅ |
| Children's Week Family Fun Day 2026 | 2026-10-24 | Teralba Park, Everton Park — OPERATIONAL | Free, InStock | ✅ |
| Diwali Festival of Lights 2026 Pimpama | 2026-10-24 | Gainsborough State School, Pimpama — OPERATIONAL | Free, InStock | ✅ |
| Logan BookFest 2026 | 2026-10-24 | Beenleigh Events Centre — OPERATIONAL | Free, InStock | ✅ |
| Monster Truck Mayhem Beaudesert | 2026-10-24 | Beaudesert Showgrounds — OPERATIONAL | Kids $35 / adults $55 / family $170, InStock | ✅ |
| Spring Family Carnival | 2026-10-24 | Latter-day Saints chapel, Camp Hill — OPERATIONAL | Free, InStock, 5pm per page text | ✅ |
| UQ Sport Aquatic Centre Family Fun Day | 2026-10-24 | UQ Sport Aquatic Centre, St Lucia — OPERATIONAL | Free, InStock | ✅ |
| Flicks & Fireworks, Surfers Paradise | 2026-10-25 | Surfers Paradise Esplanade — OPERATIONAL | Free, InStock | ✅ |
| The Christmas Spectacular | 2026-12-23 | The Fortitude Music Hall — OPERATIONAL | null — not published by source | ✅ |

## Verification failures (dropped)

| Candidate | Date | Failure |
|---|---|---|
| Sensory friendly sessions (The Corner, State Library) | 2026-10-11 | Structured `offers.availability: SoldOut` |
| Ranger Stacey's Joey Club (IndigiScapes) | 2026-10-13 | Structured `offers.availability: SoldOut` |

## Caveats

1. **10 of 25 records start before 2026-10-12**, including three on Tuesday 2026-10-06. Merge promptly or prune expired records at merge time.
2. **Breakfast with Ranger Stacey is listed ages 12+** in the page highlights and costs A$60 per person. It is kept for older kids and teens, with `age_min: 12` recorded honestly.
3. **Spring Family Carnival time discrepancy:** the JSON-LD start is 05:00 while the page text says "Saturday 24th, 5pm". The record stores the date (2026-10-24) with an Evening duration per the page text; the app does not store a start time.
4. **Monster Truck Mayhem prices** are the page-text face prices. Eventbrite's fee-inclusive AggregateOffer range (A$38.26–A$176.26) differs; the record notes the face prices parents will recognise.
5. **Chinese Cultural Experience Day** only names a campus landmark ("Grassy knoll") as its venue. Coordinates are the University of Queensland St Lucia campus, and the description says the campus plainly.
6. **The Christmas Spectacular** folds two Ticketmaster sessions (2pm and 6:30pm, 2026-12-23) into one record, following the batch 2-4 multi-session convention. Its price was not published by the source.
7. **The Urban List discovery source failed this run** with HTTP 403. No Urban List candidates were added to the queue this week; the other listings sources ran normally.
8. Eventbrite times were read from JSON-LD with +10:00 (AEST). Durations are coarse buckets per batch 1-4 convention.

## Files

- `scripts/events-batch-5.json` — 25 records, batch 1-4 schema (26 fields), unique IDs, no overlap with the 248 live records in `data/activities.json`.
- Evidence (internal, under the goal workspace): fresh BCC CSV, 34 Eventbrite page dumps with a JSON-LD verification summary, Google Places results, the chronological review list and the batch builder, all in `~/workspace/goals/the-queensland-adventure-app/hidden_files/batch5-2026-10-05/`.

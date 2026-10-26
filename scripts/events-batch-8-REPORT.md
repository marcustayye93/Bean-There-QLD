# PUBLISH PACKET — Events Batch 8

**Queensland Adventure — weekly discovery curation, Monday 2026-10-26 (Australia/Brisbane)**
**File:** `scripts/events-batch-8.json` — 15 records (5 Brisbane City Council Trumba, 10 Eventbrite)
**Status:** Verified batch for live publishing under Marcus's standing auto-publish rule (2026-09-14). Merge and push follow this packet.

---

## TIME-SENSITIVE — starts within 7 days, before 2026-11-02 (10 of 15)

Publish promptly or these lose value:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Tue 2026-10-27 | Bush Kindy: Grandparents Day | Karawatha | Free |
| Tue 2026-10-27 | Children's Week Storytime | Nundah | Free |
| Tue 2026-10-27 | Lord Mayor's City Hall Concert - Queensland Police Pipes and Drums & Band of Blue | Brisbane City | Free |
| Wed 2026-10-28 | Creative Club: Music IN Life with Mattie Barker | Burleigh Heads | Free |
| Wed 2026-10-28 | Gathering: Native Foods and Healthy Cooking | Brisbane City | Free |
| Wed 2026-10-28 | Story explorers: Spooky Halloween | Holland Park | Free |
| Thu 2026-10-29 | Bush Kindy - Grandparents' Day | Boondall | Free |
| Thu 2026-10-29 | Trick-or-Treat for Pink -Halloween Fundraiser event | Upper Coomera | Entry by donation |
| Sat 2026-10-31 | Halloween Glow-in-the-Dark Putt Putt | Mudgeeraba | From A$10 |
| Sat 2026-10-31 | Trinket Trove's Mini Market! | Indooroopilly | Free |

Later keepers (2026-11-07 to 2026-11-15): Australian Pollinator Week Event Day (Mount Coot-tha), Little builders craft workshop (South Brisbane), Board Game BBQ Brisbane Summer Game Day 2026 (Brisbane City), Children's Bike Skills (Nerang), Training Wheels to Two Wheels (Nerang) - Session 1.

---

## Funnel

| Stage | Count |
|---|---:|
| Listings pipeline new candidates (`fetch-listings.py --all`) | 20 |
| Events pipeline new candidates (`fetch-events.py --all`) | 707 |
| **Combined new candidates this run** | **727** |
| Full proposal queue after both sequential runs | 5,118 |
| Date screen: start date on/after 2026-10-26 | 727 |
| Past-dated dropped at date screen | 0 |
| Unique titles after folding daily occurrences | 574 |
| Broad verification shortlist | 42 (8 Trumba, 34 Eventbrite) |
| **Final keepers** | **15 (5 Trumba, 10 Eventbrite)** |

Pipelines ran sequentially, as required; no overwrite race. The listings run was clean: Ticketmaster 0 new from 67 unique events (6 API calls), The Urban List 1 candidate (0 new), WeekendNotes 40 candidates (20 new venue leads, none promoted this run — no verified date/venue in the candidate record, following the batch 1-7 pattern). The events run was clean: 298 new Trumba candidates from 2,000 BCC feed rows and 409 new Eventbrite candidates across Brisbane, Gold Coast and Sunshine Coast (899 candidates read, 36 pages).

## Drop reasons

Bulk manual drops from the 727 future-dated new candidates, following the batch 1-7 pattern:

| Reason | Basis |
|---|---|
| Adult fitness and Active & Healthy sessions (yoga, Pilates, Tai Chi, Zumba, aqua classes, HIIT, line dancing, martial arts terms) | large share, manual review of the chronological list |
| Recurring library and kids programs (First 5 Forever storytimes, rhyme time, generic Bush Kindy, kids sports, music groups, playgroups, term classes and tasters) | large share, manual review; the special themed sessions were kept instead (Grandparents Day Bush Kindy at two venues, Children's Week Storytime, Spooky Halloween story explorers, Music IN Life) |
| Adult-only, business, health, civic and support sessions (BNI/Bx networking, carer and peer support, immunisation clinics, singles and speed dating, Melbourne Cup lunches, Halloween bar parties, comedy clubs, professional courses) | large share, manual review |
| Seniors (50 Plus Centre program) and adult craft workshops (macramé, resin, pottery, candle and lamp making) | large share, manual review |
| Already live in the app | 14 candidates with an exact live name match (including new Eventbrite listings for the already-live Halloween Cookie Decorating at Birtinya and Monster Hunt at Kawana sessions on 2026-10-31, and repeat sessions of Fairy Rhyme Time, Sea Slug Survey and Waterbug Sampling) |
| Verification failures at page level | 6, listed below |
| Shortlist fit drops after verification | 21, listed below |

### Shortlist drops after verification (fit, duplicate or scope)

Diverse abilities: Halloween (New Farm Library; the feed states it is ideal for adults with diverse abilities and their support workers — an adult event); Orava Quartet (QPAC evening concert, adult chamber music, paid via the QPAC website); Bazil Grumble playtime (a recurring session series, not a one-off); Bush Kindy: Wild Play (generic recurring Bush Kindy, four occurrences in the window); Halloween Drawing Workshop, morning and evening sessions (A$60 charcoal still-life classes at a general art studio, no child suitability stated); Robina Town Centre: Music, Movement & Sensory Play Sessions (a recurring weekly Making Rainbows class); SociABILITY: An Inclusive Social Group for Under 18s (a peer social/support group, not a family outing); ILLUSIONS MAGIC SHOW - Surfers Paradise (evening commercial magic show at A$69-A$129); Halloween Garden Party, West End (an adult party with electronic music selectors, A$20); ZYPED HAUNTED HOUSE (live scare actors at a nightclub, 8pm start); Family zumba (a fitness class; Zumba is a standing bulk-drop category); Creative Play, Woolloongabba (a recurring fortnightly class); Making Rainbows Classes at The Plaza (a recurring under-5 class series, same provider as the Robina sessions); Chasing Shadows in the gardens (a general botanical art workshop, no child suitability stated); Brisbane Kids Track and Field Athletics (a multiple-date athletics program at QSAC); Nature Club with Rebecca Fewings (a Term 4 taster series); Kids Creative, Laidley (a multiple-date class series); Heritage Park Bush Kindy Playgroup (a recurring playgroup program); Spring Pademelon Survey (a weekday 7:30am citizen-science survey with no child or family suitability stated).

## Verification method

- **BCC Trumba (5 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-10-26 (2,000 rows). Every keeper was matched by subject, date, venue, cost, age text and geolocation in the fresh feed. Coordinates come from the feed geolocation column. The Dark Side of the Moon planetarium show in the same feed window was dropped at review again: the feed itself says it features mature themes and is not recommended for children.
- **Eventbrite (10 keepers):** all 34 shortlisted pages were fetched with a Chrome browser user agent. Every keeper shows JSON-LD `eventStatus: https://schema.org/EventScheduled`, a `startDate` in Australia/Brisbane matching the expected date, and structured `offers.availability: InStock`. Venue name, address and coordinates come from the page's embedded venue record. Prices come from the JSON-LD AggregateOffer lowPrice/highPrice. The words "sold out" in page text were not trusted; only the structured availability field decided.
- **Google Places:** every Eventbrite keeper venue was searched and confirmed Active/OPERATIONAL (Boondall Wetlands Environment Centre, Fradgley Hall Community Centre, Coomera Clubhouse for Early Childhood Learning Centre, Boomerang Hills, Trinket Trove, Brisbane Botanic Gardens Mount Coot-tha, State Library of Queensland, Glennon Park, Royal On The Park).
- **Prices:** 13 of 15 are free. Paid keepers are taken honestly from the source: Halloween Glow-in-the-Dark Putt Putt from A$10 (offer range A$10-A$40), Board Game BBQ Summer Game Day from A$25 (offer range A$25-A$64.84). Trick-or-Treat for Pink is free to register on Eventbrite and its own page text says entry is by donation for the National Breast Cancer Foundation, so its price stays 0 with an "Entry by donation" note.
- **Dates, venues, prices, coordinates, business details:** nothing invented. Australian English, AUD, Australia/Brisbane throughout.

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| Bush Kindy: Grandparents Day (Karawatha) | 2026-10-27 | Karawatha Forest Discovery Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Children's Week Storytime (Nundah) | 2026-10-27 | Nundah Library, feed-confirmed | Free, feed-confirmed, ages 0-5 | ✅ |
| Lord Mayor's City Hall Concert: Queensland Police Pipes and Drums & Band of Blue | 2026-10-27 | Brisbane City Hall, feed-confirmed | Free, feed-confirmed, all ages, Auslan interpreted | ✅ |
| Story explorers: Spooky Halloween | 2026-10-28 | Holland Park Library, feed-confirmed | Free, feed-confirmed, ages 5-12 | ✅ |
| Gathering: Native Foods and Healthy Cooking | 2026-10-28 | Queen Street Mall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Creative Club: Music IN Life with Mattie Barker | 2026-10-28 | Fradgley Hall Community Centre — OPERATIONAL | Free, InStock, under 5s | ✅ |
| Bush Kindy - Grandparents' Day (Boondall) | 2026-10-29 | Boondall Wetlands Environment Centre — OPERATIONAL | Free, InStock, ages 3-5 | ✅ |
| Trick-or-Treat for Pink (Upper Coomera) | 2026-10-29 | Coomera Clubhouse — OPERATIONAL | Entry by donation, InStock, ages 0-8 | ✅ |
| Halloween Glow-in-the-Dark Putt Putt | 2026-10-31 | Boomerang Hills — OPERATIONAL | From A$10, InStock | ✅ |
| Trinket Trove's Mini Market! | 2026-10-31 | Trinket Trove — OPERATIONAL | Free, InStock, all ages | ✅ |
| Australian Pollinator Week Event Day | 2026-11-07 | Brisbane Botanic Gardens, Mount Coot-tha — OPERATIONAL | Free, InStock | ✅ |
| Little builders craft workshop | 2026-11-12 | State Library of Queensland — OPERATIONAL | Free, InStock | ✅ |
| Board Game BBQ Brisbane Summer Game Day 2026 | 2026-11-14 | Royal On The Park — OPERATIONAL | From A$25, InStock, page states family friendly | ✅ |
| Children's Bike Skills (Nerang) | 2026-11-15 | Glennon Park — OPERATIONAL | Free, InStock, ages 6+ | ✅ |
| Training Wheels to Two Wheels (Nerang) - Session 1 | 2026-11-15 | Glennon Park — OPERATIONAL | Free, InStock, ages 4+ | ✅ |

## Verification failures (dropped)

| Candidate | Date | Failure |
|---|---|---|
| Sensory friendly sessions (The Corner, State Library) | 2026-11-01 | Structured `offers.availability: SoldOut` (fourth week running) |
| Creative Club: Young Artist Club (Burleigh Heads) | 2026-10-28 | Structured `offers.availability: SoldOut` |
| Sunny Jacks Sensory Play at Yamanto Central [Halloween] | 2026-10-30 | Structured `offers.availability: SoldOut` |
| Kingaroy Mall Trick or Treat 2026 | 2026-10-31 | Structured `offers.availability: SoldOut` |
| NaturallyGC - The Life of Frogs (Spotlighting) | 2026-11-13 | Organiser withholds the exact venue (suburb only; full location sent after registration), so the event cannot be geocoded honestly |
| Inner You Development Presents: Children's Week 2026 | 2026-11-01 | Venue (Inner You Development, Upper Mount Gravatt) has no Google Places record, so OPERATIONAL status could not be confirmed |

## Caveats

1. **10 of 15 records start within 7 days**, three of them on Tuesday 2026-10-27. Merge promptly.
2. **Grandparents Day Bush Kindy runs at two venues this week** (Karawatha on Tue 27 Oct via the council feed, Boondall on Thu 29 Oct via Eventbrite). They are separate sessions at separate environment centres and are listed as two records.
3. **Halloween Glow-in-the-Dark Putt Putt** shows a 16:00-17:00 window in its structured data. The record stores the date (2026-10-31) with an "Under 1 hour" duration; the app does not store a start time.
4. **Australian Pollinator Week Event Day** runs 10:00-14:00 in its structured data. Its duration is recorded as "Half day", a label the app displays as-is.
5. **Children's Week Storytime** carries age 0-5 from the feed's age column; the feed description calls it ideal for children aged 3-5.
6. Eventbrite times were read from JSON-LD with +10:00 (AEST). Durations are coarse buckets per batch 1-7 convention.

## Files

- `scripts/events-batch-8.json` — 15 records, batch 1-7 schema (26 fields), unique IDs, no overlap with the 321 records in `data/activities.json`.
- Evidence (internal, under the goal workspace): fresh BCC CSV, 34 Eventbrite page dumps with a JSON-LD verification summary, Google Places results, the chronological review lists and the batch builder, all in `~/workspace/goals/the-queensland-adventure-app/hidden_files/batch8-2026-10-26/`.

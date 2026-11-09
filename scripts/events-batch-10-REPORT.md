# PUBLISH PACKET — Events Batch 10

**Queensland Adventure — weekly discovery curation, Monday 2026-11-09 (Australia/Brisbane)**
**File:** `scripts/events-batch-10.json` — 18 records (4 Brisbane City Council Trumba, 14 Eventbrite)
**Status:** Verified batch for live publishing under Marcus's standing auto-publish rule (2026-09-14). Merge and push follow this packet.

---

## TIME-SENSITIVE — starts within 7 days, before 2026-11-16 (6 of 18)

Publish promptly or these lose value:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Mon 2026-11-09 | Make and create: Diwali | Ashgrove | Free |
| Tue 2026-11-10 | Bush Kindy: Australian Pollinator Week (Downfall Creek) | Chermside West | Free |
| Tue 2026-11-10 | Lord Mayor's City Hall Concert - The Beatlegs | Brisbane City | Free |
| Tue 2026-11-10 | Waste Smart Tales: Recycled Rhythms | Inala | Free |
| Wed 2026-11-11 | NDIS Capoeira class - Kids | Bethania | Free |
| Sat 2026-11-14 | Queer Zine Making Workshop | Woolloongabba | Free |

Later keepers (2026-11-21 to 2026-11-29): Junior Ranger – Park Prepared (Enoggera Reservoir), Brisbane Kids Track and Field Athletics (Nathan), DIY Craftmas Workshops (Banksia Beach), Robina Village Christmas 2026 (Robina), Children's Week Family Fun Day 2026 (Everton Park), Mini Beast Explorers (Cornubia), Kids Art - puppet making (Camp Hill), Kids Illustrator Workshop with Sophie Beer (Helensvale), Robowars Nationals 2026: Session 1 (Northgate), Everleigh Rockin' Christmas & Fireworks (Greenbank), Twelfth Annual Australasian Bat Night - Maleny (Maleny), 2026 YAD Children's Happy Camp (Priestdale).

---

## Funnel

| Stage | Count |
|---|---:|
| Listings pipeline new candidates (`fetch-listings.py --all`) | 19 |
| Events pipeline new candidates (`fetch-events.py --all`) | 759 |
| **Combined new candidates this run** | **778** |
| Full proposal queue after both sequential runs | 6,655 |
| Date screen: start date on/after 2026-11-09 | 758 |
| Past-dated dropped at date screen | 1 |
| Undated WeekendNotes leads (no verified date/venue, not promoted) | 19 |
| Unique titles after folding daily occurrences | 601 |
| Kid-signal shortlist after bulk-drop and fit screening | 28 (8 Trumba, 20 Eventbrite) |
| **Final keepers** | **18 (4 Trumba, 14 Eventbrite)** |

Pipelines ran sequentially, as required; no overwrite race. The listings run was clean: Ticketmaster 0 new from 82 unique events (6 API calls), The Urban List 2 candidates (0 new), WeekendNotes 40 candidates (19 new venue leads, none promoted this run — no verified date/venue in the candidate record, following the batch 1-9 pattern). The events run was clean: 298 new Trumba candidates from 2,000 BCC feed rows and 461 new Eventbrite candidates across Brisbane, Gold Coast and Sunshine Coast (942 candidates read, 36 pages).

## Drop reasons

Bulk manual drops from the 758 future-dated new candidates, following the batch 1-9 pattern:

| Reason | Basis |
|---|---|
| Adult fitness and Active & Healthy sessions (yoga, Pilates, Tai Chi, Zumba, aqua classes, HIIT, line dancing, martial arts terms) | large share, keyword screen of the chronological list |
| Seniors (50 Plus Centre program) and adult craft workshops (macramé, resin, pottery, candle and lamp making) | large share, keyword screen |
| Recurring library and kids programs (First 5 Forever storytimes, rhyme time, generic Bush Kindy, Music Beat kids groups, Create it library sessions, kids sports and term classes) | large share, keyword screen; the special themed sessions were shortlisted instead |
| Adult-only, business, health, civic and support sessions (networking, carer and peer support, immunisation clinics, singles and speed dating, Halloween bar parties, comedy clubs, professional courses, parent seminars) | large share, keyword screen |
| Already live in the app | 8 candidates with an exact live name match (Stories You Wear: Magpie Goose, Little Artist's Eye Spy, Warrajamba, Clock Tower Tour, Kids Fun Lab at Beenleigh Marketplace, Kids Beginner Crochet Class, Bead Day at Trinket Trove, Sea Slug Survey in the Rocky Shores) |
| Past-dated at date screen | 1 (Shingle Inn annual RizeUp Christmas gift appeal, 2026-11-03) |
| Verification failures at page level | 1, listed below |
| Shortlist fit drops after verification | 9, listed below |

### Shortlist drops after verification (fit, duplicate or scope)

Fun soccer for 2-3 years (Ferny Grove, 2026-11-11, free, ages 2-3), Fun soccer for 4-5 years (Ferny Grove, 2026-11-11, free, ages 4-5) and Kick start kids (Decker Park, Brighton, 2026-11-11, free, ages 3-8): all verified in the fresh feed but dropped as recurring Active & Healthy series (three dates each in the feed window), following the batch 9 Abseiling precedent. Bazil Grumble playtime (Anzac Park, Toowong, 2026-11-10, free, ages 2-5): verified in the fresh feed but dropped as a recurring series (two dates in the feed window). Sensory friendly sessions (The Corner, State Library, 2026-11-22): page is live and on sale again after five weeks SoldOut, but dropped as a recurring program. Chaos at the Disney Convention (Caloundra, 2026-11-25, A$11.90): page live and on sale, but the page states no child suitability, so it was dropped rather than inventing a kids fit, following the batch 9 rule used for Little Potters. Youth Night ages 12-17 (2026-11-25): a teen drop-off night with no activity detail on the page, not a family outing. Doctor For A Day, Brisbane (2026-11-28, to A$80): a career taster for high school students aspiring to enter medicine, not a family outing. Bush Kindy - Australian Pollinator Week (Eventbrite listing): duplicate of the Trumba record for the same Downfall Creek session on 2026-11-10 at 10:00am; the Trumba record was kept.

## Verification method

- **BCC Trumba (4 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-11-09 (2,000 rows). Every keeper was matched by subject, date, venue, cost, age text and geolocation in the fresh feed. Coordinates come from the feed geolocation column. The Lord Mayor's concert series recurs weekly but each concert is a distinct program, following the batch 8 precedent. Bush Kindy: Australian Pollinator Week runs at three venues on three days (Downfall Creek 10 Nov, Karawatha 11 Nov, Boondall Wetlands 12 Nov); the Downfall Creek session is recorded, following the batch 1-9 precedent of recording one venue-dated session of a touring special.
- **Eventbrite (14 keepers):** all 20 shortlisted pages were fetched with a Chrome browser user agent. Eventbrite's JSON-LD Event block is present on only some current pages, so where it was absent the page's embedded __NEXT_DATA__ record was used instead, with the same bar: event status live, sales status on_sale, a start date in Australia/Brisbane matching the expected date, and a venue record with coordinates. Prices come from the JSON-LD AggregateOffer lowPrice/highPrice or the __NEXT_DATA__ lowPrice/highPrice (AUD). The words "sold out" in page text were not trusted; only the structured availability/sales field decided.
- **Google Places:** every Eventbrite keeper venue was searched and confirmed OPERATIONAL (Bethania Community Centre, echo & bounce Woolloongabba, Walkabout Creek Discovery Centre, Teralba Park Everton Park, Cornubia Forest Park, Kaye West Studios Camp Hill, Helensvale Library, ARM Hub AI Adopt Centre Northgate, Everleigh Park Greenbank, Robina Shopping Village, Maleny Showground, Fo Guang Shan Chung Tian Temple Priestdale, Bribie Island Community Arts Centre, QSAC Nathan).
- **Prices:** 13 of 18 are free. Paid keepers are taken honestly from the source: Brisbane Kids Track and Field Athletics from A$30 (offer range A$30-A$40), DIY Craftmas Workshops A$30, Kids Art - puppet making A$33.08, Robowars Nationals 2026: Session 1 A$49.50, 2026 YAD Children's Happy Camp A$54.26.
- **Dates, venues, prices, coordinates, business details:** nothing invented. Australian English, AUD, Australia/Brisbane throughout.

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| Make and create: Diwali | 2026-11-09 | Ashgrove Library, feed-confirmed | Free, feed-confirmed, ages 5-12 | ✅ |
| Bush Kindy: Australian Pollinator Week (Downfall Creek) | 2026-11-10 | Downfall Creek Bushland Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Lord Mayor's City Hall Concert - The Beatlegs | 2026-11-10 | Brisbane City Hall, feed-confirmed | Free, feed-confirmed, all ages, AUSLAN interpreted | ✅ |
| Waste Smart Tales: Recycled Rhythms | 2026-11-10 | Inala Library, feed-confirmed | Free, feed-confirmed, ages 4-12 | ✅ |
| NDIS Capoeira class - Kids | 2026-11-11 | Bethania Community Centre — OPERATIONAL | Free, on_sale, inclusive kids class | ✅ |
| Queer Zine Making Workshop | 2026-11-14 | echo & bounce, Woolloongabba — OPERATIONAL | Free, on_sale, all ages | ✅ |
| Junior Ranger – Park Prepared | 2026-11-21 | Walkabout Creek Discovery Centre — OPERATIONAL | Free, on_sale, ages 8-12 | ✅ |
| Brisbane Kids Track and Field Athletics | 2026-11-23 | QSAC, Nathan — OPERATIONAL | From A$30, on_sale, kids athletics | ✅ |
| DIY Craftmas Workshops (Bribie Island) | 2026-11-27 | Bribie Island Community Arts Centre — OPERATIONAL | A$30, on_sale, festive craft | ✅ |
| Robina Village Christmas 2026 | 2026-11-27 | Robina Shopping Village — OPERATIONAL | Free, on_sale, Christmas celebration | ✅ |
| Children's Week Family Fun Day 2026 | 2026-11-28 | Teralba Park, Everton Park — OPERATIONAL | Free, on_sale, family fun day | ✅ |
| Mini Beast Explorers | 2026-11-28 | Cornubia Forest Park — OPERATIONAL | Free, on_sale, Great Southern BioBlitz | ✅ |
| Kids Art - puppet making | 2026-11-28 | Kaye West Studios, Camp Hill — OPERATIONAL | A$33.08, on_sale, ages 7-13 | ✅ |
| Kids Illustrator Workshop with Sophie Beer | 2026-11-28 | Helensvale Library — OPERATIONAL | Free, on_sale, illustration workshop | ✅ |
| Robowars Nationals 2026: Session 1 - Saturday - 9:30am | 2026-11-28 | ARM Hub AI Adopt Centre, Northgate — OPERATIONAL | A$49.50, InStock, session 1 only | ✅ |
| Everleigh Rockin' Christmas & Fireworks | 2026-11-28 | Everleigh Park, Greenbank — OPERATIONAL | Free, on_sale, Christmas + fireworks | ✅ |
| Twelfth Annual Australasian Bat Night - Maleny | 2026-11-28 | Maleny Showground — OPERATIONAL | Free, InStock, annual bat night | ✅ |
| 2026 YAD Children's Happy Camp | 2026-11-29 | Fo Guang Shan Chung Tian Temple, Priestdale — OPERATIONAL | A$54.26, on_sale, full-day kids camp | ✅ |

## Verification failures (dropped)

| Candidate | Date | Failure |
|---|---|---|
| Junior Ranger – Survival Starters (David Fleay Wildlife Park) | 2026-11-22 | Structured `salesStatus: sold_out` with message "Sold Out" |

## Caveats

1. **6 of 18 records start within 7 days**, on Mon 2026-11-09, Tue 2026-11-10 (x3), Wed 2026-11-11 and Sat 2026-11-14. Merge promptly; the Diwali craft session is today, 3:30pm AEST.
2. **Robowars Nationals 2026** runs seven sessions across Sat 2026-11-28 and Sun 2026-11-29; this record is session 1 only (Sat 9:30am). The app does not store a start time.
3. **Bush Kindy: Australian Pollinator Week** runs at three venues on consecutive days; this record is the Downfall Creek session on Tue 2026-11-10 at 10:00am, booked via the Eventbrite listing for that session.
4. **Brisbane Kids Track and Field Athletics** is priced A$30-A$40 in the page offer range; the record carries the low price (A$30) with a "From A$30" note, per batch 1-9 convention.
5. **Sensory friendly sessions** (The Corner) is back on sale after five weeks SoldOut; it was dropped this run as a recurring program, not on availability.
6. Eventbrite times were read with +10:00 (AEST). Durations are coarse buckets per batch 1-9 convention.

## Files

- `scripts/events-batch-10.json` — 18 records, batch 1-9 schema (26 fields), unique IDs, no overlap with the 346 records in `data/activities.json`.
- Evidence (internal, under the goal workspace): fresh BCC CSV, 20 Eventbrite page dumps with a JSON-LD/__NEXT_DATA__ verification summary, Google Places results, the chronological review lists and the batch builder, all in `~/workspace/goals/the-queensland-adventure-app/hidden_files/batch10-2026-11-09/`.

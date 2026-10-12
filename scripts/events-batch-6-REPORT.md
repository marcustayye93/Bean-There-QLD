# PUBLISH PACKET — Events Batch 6

**Queensland Adventure — weekly discovery curation, Monday 2026-10-12 (Australia/Brisbane)**
**File:** `scripts/events-batch-6.json` — 26 records (6 Brisbane City Council Trumba, 20 Eventbrite)
**Status:** Verified batch for live publishing under Marcus's standing auto-publish rule (2026-09-14). Merge and push follow this packet.

---

## TIME-SENSITIVE — starts within 7 days, before 2026-10-19 (7 of 26)

Publish promptly or these lose value:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Tue 2026-10-13 | Bush Kindy - Tea Party with Tree | Karawatha | Free |
| Tue 2026-10-13 | Bush Kindy: Library Stories and Rhymes - Nature Book Week (Downfall Creek) | Chermside West | Free |
| Tue 2026-10-13 | Lord Mayor's City Hall Concerts - Jodie-Joy Salutes Dusty Springfield and Divas | Brisbane City | Free |
| Tue 2026-10-13 | Journey to the Stars | Mount Coot-tha | Child $11 / adult $17.50 |
| Wed 2026-10-14 | Bush Kindy: Library Stories and Rhymes - Nature Book Week (Karawatha) | Karawatha | Free |
| Wed 2026-10-14 | Gathering: Zayne Hall | Brisbane City | Free |
| Thu 2026-10-15 | Halloween Magik Market | Miami | Free |

Later keepers (2026-10-24 to 2026-11-02): Junior Ranger Flying Friends and Cadet Ranger Bat Insights (both David Fleay Wildlife Park), AFRO & CARIBBEAN FEST Helensvale, Batty Boat Halloween Cruise, Weave a Web at Southport Library, Movies Under the Stars: Hotel Transylvania (Runaway Bay), BIYMF Winners Concert, Brick or Treat LEGO workshop, Festival of Lights Deepavali Mount Gravatt, Halloween in Tamborine, Redcliffe Festival of Frights, Moriarty Park Halloween Disco, Flames and Flavour BBQ Fest, Old Fashioned Craft at Mayes Cottage, Halloween Family Night Southport Sharks, Children's Bike Skills and Training Wheels to Two Wheels (Miami), Illustrating Wild Worlds for Children, and the Artisans' Guild Craft Exhibition Morayfield.

---

## Funnel

| Stage | Count |
|---|---:|
| Listings pipeline new candidates (`fetch-listings.py --all`) | 0 |
| Events pipeline new candidates (`fetch-events.py --all`) | 727 |
| **Combined new candidates this run** | **727** |
| Full proposal queue after both sequential runs | 3,663 |
| Date screen: start date on/after 2026-10-12 | 727 |
| Past-dated dropped at date screen | 0 |
| Unique titles after folding daily occurrences | 575 |
| Broad verification shortlist | 40 (6 Trumba, 34 Eventbrite) |
| **Final keepers** | **26 (6 Trumba, 20 Eventbrite)** |

Pipelines ran sequentially, as required. The listings run reported one source error: The Urban List returned `HTTP Error 403: Forbidden` (0 candidates from that source this week; Ticketmaster 2 candidates, 0 new; WeekendNotes 0). The events run was clean: 296 new Trumba candidates from 2,000 BCC feed rows and 431 new Eventbrite candidates across Brisbane, Gold Coast and Sunshine Coast (904 candidates read, 36 pages).

## Drop reasons

Bulk manual drops from the 727 future-dated new candidates, following the batch 1-5 pattern:

| Reason | Basis |
|---|---|
| Adult fitness and Active & Healthy sessions (yoga, Pilates, Tai Chi, Zumba, aqua classes, HIIT, line dancing, martial arts terms) | large share, manual review of the chronological list |
| Recurring library and kids programs (First 5 Forever storytimes, rhyme time, generic Bush Kindy, kids sports, music groups, playgroups, term classes and tasters) | large share, manual review; the two special Nature Book Week Bush Kindy sessions and the Tea Party with Tree session were kept instead |
| Adult-only, business, health, civic and support sessions (networking, carer and peer support, immunisation clinics, singles and speed dating, Halloween bar crawls and parties, comedy clubs, professional courses) | large share, manual review |
| Already live in the app | 21 candidates with an exact live name match (daily occurrences of Stories You Wear, Brisbane German Week, Brisbane Sculpture Festival, Warrajamba, Little Artist's Eye Spy, Clock Tower Tour, Audrey Gibbs Art Prize and others) |
| Verification failures at page or venue level | 5, listed below |
| Shortlist fit drops after verification | 9, listed below |

### Shortlist drops after verification (fit, duplicate or scope)

ILLUSIONS Magic Show Surfers Paradise (duplicate program of the live `evt-illusions-magic-show` record); BIYMF First Steps concert (same festival as the kept Winners Concert); Trinket Trove's Mini Market (weekly market, dropped in batch 5 on the same basis); Brisbane Kids Track and Field Athletics (A$79.99 commercial term class at QSAC); Clover Hill State School Dance Showcase (school-family showcase, weak general fit); Aussie World Halloween FestEVIL (registration-of-interest listing only, not a ticketed event); Freedom's Halloween Spooktacular (venue is a street address only, no verifiable venue record); Get your Spook on this Halloween at Tweed Mall (Tweed Heads, New South Wales, out of area); VHW Bingo and Sausage Sizzle Gympie (adult community bingo, weak family fit).

## Verification method

- **BCC Trumba (6 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-10-12 (2,000 rows). Every keeper was matched by subject, date, venue, cost, age text and geolocation in the fresh feed. Coordinates come from the feed geolocation column. The Dark Side of the Moon planetarium show in the same feed window was dropped at review: the feed itself says it features mature themes and is not recommended for children.
- **Eventbrite (20 keepers):** all 34 shortlisted pages were fetched with a Chrome browser user agent. Every keeper shows JSON-LD `eventStatus: https://schema.org/EventScheduled`, a `startDate` in Australia/Brisbane matching the expected date, and structured `offers.availability: InStock`. Venue name, address and coordinates come from the page's embedded venue record. Prices come from the JSON-LD AggregateOffer lowPrice/highPrice. The words "sold out" in page text were not trusted; only the structured availability field decided.
- **Google Places:** every Eventbrite keeper venue was searched and confirmed `businessStatus: OPERATIONAL` (Miami Marketta, Runaway Bay Cricket Club, Nerang Library, Mount Gravatt Showgrounds, Bearded Dragon Hotel, Redcliffe Markets, Moriarty Park Community Sports Centre, Barbeques & More Browns Plains, Southport Sharks, Pizzey Park, Karawatha Forest Discovery Centre, David Fleay Wildlife Park, The Potters House Church Helensvale, Brisbane City Hall, Cultural Centre Public Pontoon, Morayfield Shopping Centre, Southport Library, Mayes Cottage).
- **Prices:** 21 of 26 are free. Paid keepers are taken honestly from the source: Journey to the Stars child $11 / adult $17.50, AFRO & CARIBBEAN FEST from A$10, Batty Boat Halloween Cruise from A$27.78, Moriarty Park Halloween Disco A$6.61. The BIYMF Winners Concert shows free and ticketed options in its offer range, so its price stays 0 with a "see official listing" note.
- **Dates, venues, prices, coordinates, business details:** nothing invented. Australian English, AUD, Australia/Brisbane throughout.

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| Bush Kindy - Tea Party with Tree | 2026-10-13 | Karawatha Forest Discovery Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Bush Kindy: Nature Book Week (Downfall Creek) | 2026-10-13 | Downfall Creek Bushland Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Bush Kindy: Nature Book Week (Karawatha) | 2026-10-14 | Karawatha Forest Discovery Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Lord Mayor's City Hall Concerts: Jodie-Joy | 2026-10-13 | Brisbane City Hall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Journey to the Stars | 2026-10-13 | Sir Thomas Brisbane Planetarium, feed-confirmed | Child $11, ages 8+ | ✅ |
| Gathering: Zayne Hall | 2026-10-14 | Queen Street Mall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Halloween Magik Market | 2026-10-15 | Miami Marketta — OPERATIONAL | Free, InStock | ✅ |
| Junior Ranger - Flying Friends | 2026-10-24 | David Fleay Wildlife Park — OPERATIONAL | Free, InStock, ages 8-12 | ✅ |
| Cadet Ranger - Bat Insights | 2026-10-24 | David Fleay Wildlife Park — OPERATIONAL | Free, InStock, ages 13-17 | ✅ |
| AFRO & CARIBBEAN FEST | 2026-10-24 | The Potters House Church, Helensvale — OPERATIONAL | From A$10, InStock | ✅ |
| Batty Boat Halloween Cruise 2026 | 2026-10-25 | Cultural Centre Pontoon, South Bank — OPERATIONAL | From A$27.78, InStock | ✅ |
| Weave a Web at Southport | 2026-10-27 | Southport Library — OPERATIONAL | Free, InStock | ✅ |
| Movies Under the Stars: Hotel Transylvania | 2026-10-30 | Runaway Bay Cricket Club — OPERATIONAL | Free, InStock | ✅ |
| BIYMF Winners Concert | 2026-10-30 | Brisbane City Hall — OPERATIONAL | Free/ticketed, InStock | ✅ |
| Brick or Treat! Family LEGO Workshop | 2026-10-31 | Nerang Library — OPERATIONAL | Free, InStock | ✅ |
| Festival of Lights - Deepavali 2026 | 2026-10-31 | Mount Gravatt Showgrounds — OPERATIONAL | Free, InStock | ✅ |
| Halloween in Tamborine | 2026-10-31 | Bearded Dragon Hotel — OPERATIONAL | Free entry, InStock | ✅ |
| Redcliffe Festival of Frights | 2026-10-31 | Redcliffe Markets — OPERATIONAL | Free, InStock | ✅ |
| Moriarty Park Halloween Disco 2026 | 2026-10-31 | Moriarty Park Community Sports Centre — OPERATIONAL | A$6.61, InStock | ✅ |
| Flames and Flavour BBQ Fest 2026 | 2026-10-31 | Barbeques & More, Browns Plains — OPERATIONAL | Free, InStock | ✅ |
| Old Fashioned Craft at Mayes Cottage | 2026-10-31 | Mayes Cottage, Kingston — OPERATIONAL | Free, InStock | ✅ |
| Halloween Family Night | 2026-11-01 | Southport Sharks — OPERATIONAL | Free entry, InStock | ✅ |
| Children's Bike Skills (Miami) | 2026-11-01 | Pizzey Park, Miami — OPERATIONAL | Free, InStock, ages 6+ | ✅ |
| Training Wheels to Two Wheels (Miami) | 2026-11-01 | Pizzey Park, Miami — OPERATIONAL | Free, InStock, ages 4+ | ✅ |
| Illustrating Wild Worlds for Children | 2026-11-01 | Karawatha Forest Discovery Centre — OPERATIONAL | Free, InStock | ✅ |
| Artisans' Guild Craft Exhibition | 2026-11-02 | Morayfield Shopping Centre — OPERATIONAL | Free, InStock | ✅ |

## Verification failures (dropped)

| Candidate | Date | Failure |
|---|---|---|
| Sensory friendly sessions (The Corner, State Library) | 2026-10-18 | Structured `offers.availability: SoldOut` |
| Monster Mash Halloween Party (Helensvale) | 2026-10-31 | Structured `offers.availability: SoldOut` |
| Bewitching Bunting at Burleigh Waters | 2026-10-27 | Burleigh Waters Library is `CLOSED_TEMPORARILY` on Google Places |
| NAMBOUR HUB: Halloween Fun at the Hub | 2026-10-30 | Venue (Nambour Carer Gateway Hub) has no Google Places record to verify OPERATIONAL |
| Logan Arts Festival - Hillcrest | 2026-10-31 | Venue is a street address only (unit 3/13 Corporate Place), no named Places record |

## Caveats

1. **7 of 26 records start within 7 days**, including six on Tuesday 2026-10-13 and Wednesday 2026-10-14. Merge promptly.
2. **Cadet Ranger - Bat Insights is listed ages 13-17** on Eventbrite. The record caps `age_max` at 16 per the app schema and states the listed range in the description.
3. **Halloween Magik Market** shows a 05:00-09:00 start in its structured data at Miami Marketta. The record stores the date (2026-10-15) with a Morning duration; the app does not store a start time.
4. **Halloween Family Night and Halloween in Tamborine** show paid options in their offer ranges alongside free entry tickets. Both records use free entry, matching the structured low price.
5. **The Urban List discovery source failed this run** with HTTP 403, as in batch 5. No Urban List candidates were added to the queue this week; the other listings sources ran normally.
6. Eventbrite times were read from JSON-LD with +10:00 (AEST). Durations are coarse buckets per batch 1-5 convention.

## Files

- `scripts/events-batch-6.json` — 26 records, batch 1-5 schema (26 fields), unique IDs, no overlap with the 273 live records in `data/activities.json`.
- Evidence (internal, under the goal workspace): fresh BCC CSV, 34 Eventbrite page dumps with a JSON-LD verification summary, Google Places results, the chronological review list and the batch builder, all in `~/workspace/goals/the-queensland-adventure-app/hidden_files/batch6-2026-10-12/`.

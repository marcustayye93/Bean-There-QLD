# PUBLISH PACKET — Events Batch 4

**Queensland Adventure — event curation, Monday 2026-09-28 (Australia/Brisbane)**
**File:** `scripts/events-batch-4.json` — 42 records (36 Eventbrite, 6 Brisbane City Council Trumba)
**Status:** Ready for Marcus's review. Nothing pushed. `data/activities.json` untouched.

---

## TIME-SENSITIVE — starts before 2026-10-05 (32 of 42)

Most of this batch is school-holiday programming. If the merge is delayed past the dates below, those records should be held or dropped.

| Date | Event | Suburb | Price |
|---|---|---|---|
| 2026-09-28 (today) | Botanic By Night: NightGlow | Mount Coot-tha | See listing |
| 2026-09-28 (today) | Create a poppy suncatcher (runs to 4 Oct) | Brisbane City | Free |
| 2026-09-28 (today) | School Holiday Workshop: 3 Day Dance, Acro & Inspire | Tingalpa | From $91.31 |
| 2026-09-29 | A&H Circus Play with HAPY Studio | Currumbin Valley | Free |
| 2026-09-29 | A&H Music, Movement and Magic: Nia for Kids | Carrara | Free |
| 2026-09-29 | A&H Water warriors | Mermaid Beach | Free |
| 2026-09-29 | Children's Bike Skills (Palm Beach) | Palm Beach | Free |
| 2026-09-29 | Kids Fun Lab at Beenleigh Marketplace | Beenleigh | Free |
| 2026-09-29 | Monster Jump Sandstone Point (inflatable obstacle course) | Sandstone Point | Free |
| 2026-09-29 | NaturallyGC Kids - Seagrass Meadows | Palm Beach | Free |
| 2026-09-29 | Training Wheels to Two Wheels (Palm Beach) | Palm Beach | Free |
| 2026-09-29 | Winnie the Pooh Pom Pom Friends | Nerang | Free |
| 2026-09-30 | A&H Basketball and soccer | Coomera | Free |
| 2026-09-30 | Creative Club: Mini Music Club with ELSKA (under 5s) | Burleigh Heads | Free |
| 2026-09-30 | Creative Club: Young Song Writers Club (7-12) | Burleigh Heads | Free |
| 2026-09-30 | Gathering: Muralappi Arts — Jessica Skeen (artist talk) | Brisbane City | Free |
| 2026-09-30 | Kids Beginner Crochet Class | Capalaba | $55.00 |
| 2026-09-30 | Meet the Rainforest Guided Walk | Maleny | $5.00 |
| 2026-09-30 | NaturallyGC Kids - Discover Dolphins | Broadbeach | Free |
| 2026-09-30 | NaturallyGC Kids - Insect Explorers | Southport | Free |
| 2026-09-30 | Pencil Holder Friends | Nerang | Free |
| 2026-10-01 | Brisbane German Week (18-day citywide program) | Brisbane City | Free |
| 2026-10-01 | Creature kids (5-14, bookings essential) | Sherwood | Free |
| 2026-10-01 | Geckoes Wildlife experience | Capalaba | $27.78 |
| 2026-10-01 | Junior explorers: Nature journaling (9+) | Boondall | Free |
| 2026-10-01 | Learn to DJ Workshop | Aspley | Free |
| 2026-10-01 | Pencil Holder Friends | Robina | Free |
| 2026-10-02 | Junior First Aid Training (6-12) | Lamb Island | Free |
| 2026-10-02 | NaturallyGC Kids - Nature Arts and Craft | Benowa | Free |
| 2026-10-02 | Unravel: All ages Aerial & Acrobatic Show | Currumbin | From $5.00 |
| 2026-10-03 | Spring Flower Garden Ballet Party (ages 3-8) | Tingalpa | $22.49 |
| 2026-10-03 | Vapiano Carindale Pizza Kids! | Carindale | $27.78 |

Later keepers (2026-10-05 to 2026-10-18): The Grand Diwali at Eat Street (5 Oct), NaturallyGC Wildlife Watch (7 Oct), Drag Story Hour (8 Oct), Sea Slug Annual Count + NaturallyGC Nocturnal Natives (9 Oct), Movies Under the Stars: Madagascar (10 Oct), Comics Workshop Carindale (11 Oct), Twilight on the Turf Buddina (16 Oct), Movies Under the Stars: The Wild Robot + Writing Wild Worlds (17-18 Oct).

---

## Funnel

| Stage | Count |
|---|---:|
| Full proposal queue | 2,271 |
| Date on/after 2026-09-28 | 1,149 |
| Date-screen drops (1,039 past, 83 undated) | 1,122 |
| Auto-drop: obvious adult / weak-fit (keywords) | 148 |
| Exact live-name duplicates | 55 |
| Chronological manual review | 946 |
| Broad verification shortlist | 79 (6 Trumba, 73 Eventbrite) |
| **Final keepers** | **42 (36 Eventbrite, 6 Trumba)** |

Manual review was done oldest-first across the full 946; the shortlist was deliberately broad and then cut hard on verification and fit.

## Drop-reason counts (from the 79 shortlisted)

| Reason | Count |
|---|---:|
| Sold out (Eventbrite structured `offers.availability: SoldOut`) | 14 |
| Booked out (Trumba feed status) | 1 |
| Duplicate sessions of same program (kept one/fewest) | 14 |
| Weak fit: generic commercial class / vague program / adult-skewed | 6 |
| Out of area (Toowoomba / Darling Downs) | 3 |
| Venue not verifiable on Google Places | 1 |
| Weak family fit on timing/content | 2 |

Notable sold-out losses: most NaturallyGC Kids sessions (Sea Creatures, Indigenous Arts and Culture), both A&H Hidden Gems nature explorations, Teddy Bear Donut sensory sessions, Messy Play Flagstone, Dungeons & Dragons workshops, Holiday Program Habitat Makers and Little Scientists. All showed `availability: SoldOut` in the page's JSON-LD AggregateOffer — a hard drop per the rules.

Notable judgment calls:
- **Wild Faaji x Jerk X Jollof** (shortlisted by index mix-up) dropped: adult Afrobeats party, not family content. **The Grand Diwali at Eat Street** (the intended one) verified and kept.
- **WANTED - A CIRQUE HEIST** dropped: venue is only a street address (950 Beaudesert Nerang Rd, Mount Nathan) with no Google Places business record, so it could not be verified OPERATIONAL.
- **Moon & Nation** dropped: 6am Monday event, weak family fit.
- **Cultural Connect Day** dropped: venue is only "5 Hicks St, Southport", no verifiable details.
- **Monster Jump Sandstone Point**: live data already holds a 2026-09-19 occurrence (`evt-monster-jump-sandstone-point`); the 2026-09-29 occurrence is kept under a new date-suffixed id `evt-monster-jump-sandstone-point-20260929`.
- Pencil Holder Friends kept at Nerang + Robina only (Helensvale and Runaway Bay sessions dropped as duplicates). Training Wheels / Bike Skills kept at Palm Beach only (Pacific Pines, Nerang, Runaway Bay dropped). Sea Slug Survey kept as the Annual Count only. Vapiano kept at Carindale only (Coomera and Garden City sold out, Orion dropped as duplicate). Water warriors kept at Mermaid Beach only.

## Verification method

- **BCC Trumba:** fresh semicolon-delimited OpenDataSoft CSV pulled 2026-09-28 (2,000 rows). Every keeper matched by title + date; ID, venue, cost, age text, geolocation and status confirmed from the feed row. Geocoordinates come from the feed's geolocation column (batch-3 convention).
- **Eventbrite:** all 73 shortlisted pages fetched with a Chrome browser user agent. Every keeper shows JSON-LD `eventStatus: https://schema.org/EventScheduled`, a `startDate` in Australia/Brisbane matching the expected date, and `offers.availability: InStock`. Prices taken from the JSON-LD `AggregateOffer` lowPrice/highPrice (AUD; several free library events carry `priceCurrency: USD` in their JSON-LD but are $0.00, cosmetic only). The word "sold out" in page text was not trusted (it appears in Eventbrite i18n dictionaries); only the structured availability field decided.
- **Google Places:** every Eventbrite keeper's venue was searched and confirmed `businessStatus: OPERATIONAL` via the google-places skill. Exceptions, all noted in the record description: six NaturallyGC events only disclose the suburb ("location details within order confirmation email") so the suburb centroid is used; Junior First Aid's LIRA Building has no Places record so the Lamb Island centroid is used; Brisbane German Week is an 18-day citywide program with no single venue so the Brisbane CBD centroid is used.
- Prices unknown are `null` only where genuinely unknown (NightGlow: "See website"); everything else is the verified ticketed price or 0 with "Free entry".

## Per-event verification table

| Event | Date | Venue check | Status | Price source |
|---|---|---|---|---|
| Botanic By Night: NightGlow | 2026-09-28 | Feed coords (-27.4759, 152.9777) | Feed match, all ages | null — "See website" |
| Create a poppy suncatcher | 2026-09-28–10-04 | Feed coords (-27.4665, 153.0266) | Feed match, free, all ages | Free entry |
| School Holiday Workshop: 3 Day Dance, Acro & Inspire | 2026-09-28 | Frontier Studios Tingalpa — OPERATIONAL | EventScheduled, InStock | $91.31 lowPrice |
| A&H Circus Play with HAPY Studio | 2026-09-29 | Robert Neumann Park — OPERATIONAL | EventScheduled, InStock | Free entry |
| A&H Music, Movement and Magic: Nia for Kids | 2026-09-29 | Carrara Community Centre — OPERATIONAL | EventScheduled, InStock | Free entry |
| A&H Water warriors | 2026-09-29 | St Johns Park — OPERATIONAL | EventScheduled, InStock | Free entry |
| Children's Bike Skills (Palm Beach) | 2026-09-29 | Mallawa Sports Complex — OPERATIONAL | EventScheduled, InStock | Free entry |
| Kids Fun Lab at Beenleigh Marketplace | 2026-09-29 | Beenleigh Marketplace — OPERATIONAL | EventScheduled, InStock | Free entry |
| Monster Jump Sandstone Point | 2026-09-29 | Sandstone Point Hotel — OPERATIONAL | EventScheduled, InStock | Free entry |
| NaturallyGC Kids - Seagrass Meadows | 2026-09-29 | Palm Beach suburb centroid (noted) | EventScheduled, InStock | Free entry |
| Training Wheels to Two Wheels (Palm Beach) | 2026-09-29 | Mallawa Sports Complex — OPERATIONAL | EventScheduled, InStock | Free entry |
| Winnie the Pooh Pom Pom Friends | 2026-09-29 | Nerang Library — OPERATIONAL | EventScheduled, InStock | Free entry |
| A&H Basketball and soccer | 2026-09-30 | Viney Park — OPERATIONAL | EventScheduled, InStock | Free entry |
| Creative Club: Mini Music Club with ELSKA | 2026-09-30 | Fradgley Hall — OPERATIONAL | EventScheduled, InStock | Free entry |
| Creative Club: Young Song Writers Club | 2026-09-30 | Fradgley Hall — OPERATIONAL | EventScheduled, InStock | Free entry |
| Gathering: Muralappi Arts — Jessica Skeen | 2026-09-30 | Feed coords (-27.4697, 153.0253) | Feed match, free, all ages | Free entry |
| Kids Beginner Crochet Class | 2026-09-30 | Redland Coast Art Society — OPERATIONAL | EventScheduled, InStock | $55.00 |
| Meet the Rainforest Guided Walk | 2026-09-30 | Mary Cairncross Scenic Reserve — OPERATIONAL | EventScheduled, InStock | $5.00 |
| NaturallyGC Kids - Discover Dolphins | 2026-09-30 | Broadbeach suburb centroid (noted) | EventScheduled, InStock | Free entry |
| NaturallyGC Kids - Insect Explorers | 2026-09-30 | Southport suburb centroid (noted) | EventScheduled, InStock | Free entry |
| Pencil Holder Friends | 2026-09-30 | Nerang Library — OPERATIONAL | EventScheduled, InStock | Free entry |
| Brisbane German Week | 2026-10-01–10-17 | CBD centroid, citywide program (noted) | Feed match, free, all ages | Free entry |
| Creature kids | 2026-10-01 | Feed coords (-27.5327, 152.9741) | Feed match, free, 5-14 | Free entry |
| Geckoes Wildlife experience | 2026-10-01 | Redlands IndigiScapes Centre — OPERATIONAL | EventScheduled, InStock | $27.78 |
| Junior explorers: Nature journaling | 2026-10-01 | Feed coords (-27.3367, 153.0741) | Feed match, free, 9+ | Free entry |
| Learn to DJ Workshop | 2026-10-01 | Arties Music Aspley — OPERATIONAL | EventScheduled, InStock | Free entry |
| Pencil Holder Friends | 2026-10-01 | Robina Library — OPERATIONAL | EventScheduled, InStock | Free entry |
| Junior First Aid Training | 2026-10-02 | Lamb Island centroid (noted) | EventScheduled, InStock | Free entry |
| NaturallyGC Kids - Nature Arts and Craft | 2026-10-02 | Benowa suburb centroid (noted) | EventScheduled, InStock | Free entry |
| Unravel: Aerial & Acrobatic Show | 2026-10-02 | HAPY Studio Currumbin — OPERATIONAL | EventScheduled, InStock | from $5.00 |
| Spring Flower Garden Ballet Party | 2026-10-03 | Frontier Studios Tingalpa — OPERATIONAL | EventScheduled, InStock | $22.49 |
| Vapiano Carindale Pizza Kids! | 2026-10-03 | Vapiano Carindale — OPERATIONAL | EventScheduled, InStock | $27.78 |
| The Grand Diwali at Eat Street | 2026-10-05 | Eat Street Northshore — OPERATIONAL | EventScheduled, InStock | from $5.00 |
| NaturallyGC Wildlife Watch | 2026-10-07 | Varsity Lakes suburb centroid (noted) | EventScheduled, InStock | Free entry |
| Ally Network + Library - Drag Story Hour | 2026-10-08 | Bond University — OPERATIONAL | EventScheduled, InStock | Free entry |
| Sea Slug Survey: Annual Sea Slug Count | 2026-10-09 | John Laws Park — OPERATIONAL | EventScheduled, InStock | Free entry |
| NaturallyGC Nocturnal Natives | 2026-10-09 | Varsity Lakes suburb centroid (noted) | EventScheduled, InStock | Free entry |
| Movies Under the Stars: Madagascar | 2026-10-10 | Chevron Island Park — OPERATIONAL | EventScheduled, InStock | Free entry |
| Comics Workshop - Carindale Library | 2026-10-11 | Carindale Library — OPERATIONAL | EventScheduled, InStock | Free entry |
| Twilight on the Turf | 2026-10-16 | Buddina State School — OPERATIONAL | EventScheduled, InStock | Free entry |
| Movies Under the Stars: The Wild Robot | 2026-10-17 | Greenheart Robina Parklands — OPERATIONAL | EventScheduled, InStock | Free entry |
| Writing Wild Worlds with Meredith Downes | 2026-10-18 | Karawatha Forest Discovery Centre — OPERATIONAL | EventScheduled, InStock | Free entry |

## Verification failures (dropped)

| Candidate | Date | Failure |
|---|---|---|
| Laser tag (Trumba) | 2026-09-29 | Feed status "Booked out" |
| Holiday Program: Habitat Makers | 2026-09-28 | offers.availability SoldOut |
| A&H Hidden gems nature exploration Hope Island | 2026-09-29 | offers.availability SoldOut |
| NaturallyGC Kids - Sea Creatures | 2026-09-29 | offers.availability SoldOut |
| A&H Hidden gems nature exploration Pimpama | 2026-10-01 | offers.availability SoldOut |
| Holiday Program: Little Scientists - Platypus | 2026-10-01 | offers.availability SoldOut |
| Teddy Bear Donut King Donuts SENSORY SESSIONS | 2026-09-30 | offers.availability SoldOut |
| Our Beaches and Waterways - dune planting | 2026-09-30 | offers.availability SoldOut |
| Messy Play - Sensory Play Flagstone | 2026-09-30 | offers.availability SoldOut |
| Dungeons & Dragons: Character Creation | 2026-09-30 | offers.availability SoldOut |
| NaturallyGC Indigenous Arts and Culture | 2026-10-02 | offers.availability SoldOut |
| Vapiano Garden City Pizza Kids! | 2026-10-03 | offers.availability SoldOut |
| Vapiano Coomera Pizza Kids! | 2026-10-03 | offers.availability SoldOut |
| Junior Bike Skills | 2026-10-03 | offers.availability SoldOut |
| Sensory friendly sessions | 2026-10-04 | offers.availability SoldOut |
| WANTED - A CIRQUE HEIST | 2026-10-02 | Venue not verifiable (street address only, no Places record) |

## Caveats

1. **32 of 42 records start before 2026-10-05.** Merge promptly or prune expired ones at merge time.
2. NaturallyGC events (6) deliberately withhold exact meeting points until booking confirmation; coordinates are suburb centroids and the description says so.
3. Brisbane German Week is an 18-day citywide program; dates set 2026-10-01 to 2026-10-17 from the feed occurrence, venue listed as "Various venues across Brisbane" with a CBD centroid. The program's real start may be a day or two earlier; description advises checking the program.
4. NightGlow's price is on the event website ("See website" in the feed); `price_aud` is null.
5. Eventbrite times were converted from the JSON-LD `startDate` (+10:00, AEST). Durations are coarse buckets per batch-3 convention.
6. Two Trumba keepers from the earlier broad shortlist were cut on fit: Brisbane Greeters guided walk (teen/adult-skewed ages) and the generic "Laser tag" (booked out).
7. `python3 -m json.tool` passes; all 42 ids unique and none overlap `data/activities.json`; schema matches batch-3 exactly (26 fields, category "events", indoor as string, interests from the batch-3 vocabulary).

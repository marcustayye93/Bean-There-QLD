# Events Batch 3 — Review Report (2026-09-21)

**PUBLISH PACKET. Nothing was written to `data/activities.json`, nothing was pushed.**
Untouched files: `data/activities.json` (173 records, 52 live events), all app code, all other scripts.
This packet proposes `scripts/events-batch-3.json` (33 records, batch-2 schema) for live publishing under Marcus's standing auto-publish rule (2026-09-14).

## Funnel

| Stage | Count |
|---|---|
| 2026-09-21 discovery refresh, new candidates | 375 |
| Full proposal queue at screening start | 1,213 |
| Date screen: start date on/after 2026-09-21 | 510 |
| Auto-drop: obvious adult / weak-fit | −93 |
| Already live in the app (name match vs `data/activities.json`) | −41 |
| Manual review (chronological, `/tmp/batch3-review.txt`) | 376 |
| **KEPT for batch 3** | **33** |
| Dropped at manual review / verification | 343 |

Queue composition at screening: 857 Brisbane City Council (Trumba), 286 Eventbrite, 67 WeekendNotes, 3 Urban List.

## ⚠️ Time-sensitive: starts within 7 days (21–28 Sep)

Sixteen of the 33 start before 29 Sep — publish promptly or they lose value:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Mon 21 Sep | Children's Bike Skills (Pimpama) | Pimpama | Free |
| Mon 21 Sep – Fri 2 Oct | MoB Kids: Pop Badges (daily) | Brisbane City | $2–$5 |
| Mon 21 Sep – Fri 2 Oct | MoB Kids: Fun with Ferns (daily) | Brisbane City | Free |
| Mon 21 Sep – Fri 2 Oct | Lord Mayor's Photographic Awards 2026 (exhibition) | Brisbane City | Free |
| Tue 22 Sep | Lord Mayor's City Hall Concerts: UQ (Brisbane Festival) | Brisbane City | Free |
| Tue 22 Sep | Go Seek Snow Globe Creation Workshop | Tewantin | $5 |
| Tue 22 Sep | NaturallyGC Kids: Creek Habitat Hunt | Paradise Point | Free |
| Wed 23 Sep | ESCAPE by DIAVOLO, QPAC (season to 28 Sep) | South Brisbane | A$65.90–A$99.90 |
| Wed 23 Sep | Gathering: Nana Magic's Deadly Adventures | Brisbane City | Free |
| Wed 23 Sep | Shingle Inn City Hall: Paint a pot party | Brisbane City | A$28–A$40 |
| Wed 23 Sep | MoB Teens: Sunday Fun-day Workshop (also Wed 30 Sep) | Brisbane City | $30 |
| Wed 23 Sep | Twilight walk: Karawatha Forest (10+) | Karawatha | Free |
| Wed 23 Sep | Movie Night at the Hills: Lilo and Stitch | Mudgeeraba | A$17.19–A$63.79 |
| Thu 24 Sep | Senses alive: see, hear and touch nature (3+) | Karawatha | Free |
| Thu 24 Sep | Under the Full Moon: Mid-Autumn Festival | Annerley | Free entry |
| Thu 24 Sep | NaturallyGC Kids: Sharks and Rays | Labrador | Free |

## Drop reasons (343 manual drops + 93 auto-drops)

| Reason | Count | Basis |
|---|---|---|
| Recurring kids classes / generic Active & Healthy sessions (music beat, creative movement, kids sports, karate, martial arts, scooter/skate clinics, fishing, archery) | large share | manual review |
| Recurring library programs (storytimes, Lego clubs, rhyme time, Winnie the Pooh craft, drop-in crafts) | large share | manual review |
| Adult fitness / seniors classes (tai chi, aqua, MoveFit, Silver Swans) | dozens | manual review |
| Health, civic, support and business sessions (immunisation, carers, networking, info evenings) | dozens | manual review |
| Already live in the app (DUP-LIVE vs the 52 live events) | 41 | name match vs `data/activities.json` |
| Adult-only entertainment (18+ shows, wine/beer, burlesque, club nights) | small | manual review |
| Outside Queensland (Casino NSW, Lismore NSW, Ballina NSW) | 3 | manual review |
| **Verification failures (would otherwise have been kept)** | **11** | page-level checks below |

## Verification method

- **BCC Trumba (10 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-09-21 (2,000 rows, `/tmp/bcc-fresh-2026-09-21.csv`). Event IDs, dates, venues, costs, age ranges all confirmed present in the fresh feed. Geocoordinates taken from the feed's geolocation column.
- **Eventbrite (23 keepers):** every page fetched with a browser user agent. Required: JSON-LD `eventStatus` containing `EventScheduled` (or page-title date confirmation where the organiser publishes no JSON-LD), startDate matching the expected date in Australia/Brisbane, offers `availability` of `InStock` — the word "sold out" alone is not trusted (it appears in Eventbrite's i18n dictionaries on every page). 23 unique venues checked through Google Places: 19 OPERATIONAL, 2 suburb centroids (NaturallyGC), 1 street-level, 1 reserve entrance (see table). Raw dumps and the parse scripts are kept at `/tmp/eb-batch3/` and `/tmp/eb-verify3.py` for audit.
- **Prices:** taken from the page's ticket data (lowPrice/highPrice) or description text. Unknown prices stay `null` with "See official listing for ticket details."
- **Dates, venues, prices, coordinates, business details:** nothing invented. Multi-day occurrences folded into one record (MoB Kids programs 21 Sep–2 Oct; Photographic Awards 21 Sep–2 Oct; Play The Bluey Way 26–27 Sep; ESCAPE 23–28 Sep) with sessions noted in the description. Recurring BCC occurrences follow batch-1/2 convention.

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| City Hall Concerts: UQ (Brisbane Festival) | 22 Sep | City Hall, feed-confirmed | Free, feed-confirmed | ✅ |
| Photographic Awards 2026 | 21 Sep–2 Oct | Museum of Brisbane, feed-confirmed | Free, feed-confirmed | ✅ |
| MoB Kids: Pop Badges | 21 Sep–2 Oct | Museum of Brisbane, feed-confirmed | $2–$5, feed-confirmed | ✅ |
| MoB Kids: Fun with Ferns | 21 Sep–2 Oct | Museum of Brisbane, feed-confirmed | Free, feed-confirmed | ✅ |
| ESCAPE by DIAVOLO (QPAC) | 23–28 Sep | QPAC, feed-confirmed | A$65.90–A$99.90, feed-confirmed | ✅ |
| Nana Magic's Deadly Adventures | 23 Sep | Queen Street Mall, feed-confirmed | Free, feed-confirmed | ✅ |
| Paint a pot party | 23 Sep | City Hall, feed-confirmed | A$28–A$40, feed-confirmed | ✅ |
| MoB Teens: Sunday Fun-day | 23 + 30 Sep | Museum of Brisbane, feed-confirmed | $30, feed-confirmed | ✅ |
| Twilight walk: Karawatha | 23 Sep | Karawatha Forest Discovery Centre, feed-confirmed | Free, feed-confirmed | ✅ |
| Senses alive | 24 Sep | Karawatha Forest Discovery Centre, feed-confirmed | Free, feed-confirmed | ✅ |
| Under the Full Moon | 24 Sep | VEND Cafe Annerley — OPERATIONAL | Free entry; to A$17.19 | ✅ |
| Sister City Art Workshop | 26 Sep | Logan Art Gallery — OPERATIONAL | Free | ✅ |
| Go Seek Snow Globe | 22 Sep | Tewantin Noosa RSL — OPERATIONAL | A$5 | ✅ |
| Creek Habitat Hunt | 22 Sep | Paradise Point Parklands — OPERATIONAL | Free | ✅ |
| Sharks and Rays | 24 Sep | Labrador, exact point in confirmation email — suburb centroid | Free | ⚠️ approximate location |
| Wildlife Encounters (GC) | 1 Oct | Upper Coomera, exact point in confirmation email — suburb centroid | Free | ⚠️ approximate location |
| iNaturalist (9+) | 29 Sep | Downfall Creek Bushland Centre — OPERATIONAL | Free | ✅ |
| Play The Bluey Way | 26–27 Sep | Wittonga Park, The Gap — OPERATIONAL | Free | ✅ |
| Meet Bluey and Bingo (BCF) | 3 Oct | BCF Everton Park — OPERATIONAL | Free | ✅ |
| Everleigh Big Machine Day | 10 Oct | Everleigh estate, Ivory Pkwy Greenbank — street-level | Free | ⚠️ approximate location |
| BioBlitz Minnippi | 10 Oct | Porter's Paddock Park, Tingalpa — OPERATIONAL | Free | ✅ |
| Shorebird Adventures | 11 Oct | Boondall Wetlands Environment Centre — OPERATIONAL | Free | ✅ |
| Great Koala Count | 11 Oct | Whites Hill Reserve — OPERATIONAL | A$5–A$8 | ✅ |
| Park after Dark: Spotlighting | 10 Oct | Birnam Range Reserve entrance, Jimboomba — OPERATIONAL | Free | ✅ |
| Films in the Forest | 10 Oct | Starlight Hall, Bridges — OPERATIONAL | A$19.84–A$43.66 | ✅ |
| Movie Night: Lilo and Stitch | 23 Sep | Boomerang Hills, Mudgeeraba — OPERATIONAL | A$17.19–A$63.79 | ✅ |
| Movie Night: Minecraft | 29 Sep | Boomerang Hills, Mudgeeraba — OPERATIONAL | A$17.19–A$63.79 | ✅ |
| Kindira Bee & Pollinator | 2 Oct | Flagstone Parklands Community Hub — OPERATIONAL | Free | ✅ |
| Dessert Nachos Kids' Workshop | 1 Oct | Riverlink Shopping Centre, Nth Ipswich — OPERATIONAL | $7/child | ✅ |
| Youth Writing Workshop | 2 Oct | Upper Coomera Library — OPERATIONAL | Free | ✅ |
| Painted Still Life (5–10) | 4 Oct | Creative Room Art Space, West End — OPERATIONAL | A$35 | ✅ |
| Pumpkins! (8–13) | 12 Oct | Wynnum Manly Arts Council — OPERATIONAL | A$54.26 | ✅ |
| Bike Skills (Pimpama, 6+) | 21 Sep | Pimpama Sports Hub — OPERATIONAL | Free | ✅ |

## Verification failures (dropped)

| Candidate | Reason |
|---|---|
| Junior Explorers: Bug Detectives (23 Sep) | Sold out (offers availability `SoldOut`) |
| Koala Painting Kids Art Workshop (23 Sep) | Sold out |
| KRANK Kerbside Creatures (23 Sep) | Sold out |
| Rainbow Teddy Bear Stuffems (21 Sep) | Sold out |
| School Holiday Slime Workshop 2026 (21 Sep) | Sold out |
| NaturallyGC: Scaly Reptiles (25 Sep) | Sold out |
| BMX Skills (26 Sep) | Sold out |
| Junior Explorers: Be a Platypal (24 Sep) | Sold out |
| Kids Holiday Workshop: Crazy Critters (29 Sep) | Sold out |
| [Gold Coast] Kids AI Workshop (26 Sep) | Venue is a residential address (3 Stanton Court, Parkwood) — not suitable for a family listing |
| The Dark Side of the Moon (planetarium, 23 Sep) | Feed age field: "Not recommended for children" |

## Photo-keyword gaps (for the app, not this packet)

The app's `EVENT_KEYWORDS` in `js/app.js` maps these keepers to the generic festival pack where a better pack exists:

| Keeper | Current pack | Better match | Suggested keyword addition |
|---|---|---|---|
| Creek Habitat Hunt | festival | nature | add `creek`, `habitat` to nature |
| Sharks and Rays | festival | water | add `shark` to water |
| BioBlitz Minnippi | festival | nature | add `bioblitz`, `biodivers` to nature |
| Shorebird Adventures | festival | nature | add `bird` to nature |
| Great Koala Count | festival | nature | add `koala` to nature |
| Kindira Bee & Pollinator | festival | nature | add `bee`, `pollinat` to nature |
| Everleigh Big Machine Day | festival | truck | add `machine` to truck (check for false positives first) |

Everything else maps sensibly (cinema nights → cinema, Full Moon → space, art workshops → art, bike skills → wheels, forest/nature walks → nature, concerts/shows/Bluey → festival).

## Open questions and caveats

1. **NaturallyGC suburb centroids** (Sharks and Rays, Wildlife Encounters): free and verified, but the organiser only discloses the exact meeting point in the confirmation email. Descriptions say this plainly, as in batch 2.
2. **Big Machine Day street-level pin:** the Everleigh estate event lists "Ivory Parkway, Greenbank"; the pin is street-level. Description says to check the listing for the exact spot.
3. **Shorebird Adventures** publishes no JSON-LD; verified via page title ("Sunday 11 October, 10 am - 11 am"), venue text (Boondall Wetlands Environment Centre), and offers availability `InStock`.
4. **Under the Full Moon pricing:** Eventbrite lowPrice is A$0.00 / highPrice A$17.19 — free entry with paid ticket options. Recorded as price_aud 0 with an honest note.
5. **Play The Bluey Way** runs 26–27 September per its description; the Eventbrite start is 26 Sep and the record folds both days.
6. **Pumpkins! at A$54.26** is the priciest kids workshop in the batch; price is stated plainly.
7. **MoB Kids programs and the Photographic Awards** run daily through the feed window (to 2 Oct); end dates are the last confirmed feed occurrence, not a published closing date.

## Files

- `scripts/events-batch-3.json` — 33 records, batch-2 schema, unique IDs, no overlap with the 173 live records.
- Evidence: `/tmp/bcc-fresh-2026-09-21.csv` (fresh BCC feed), `/tmp/eb-batch3-verify.json` (33 page verifications), `/tmp/eb-batch3/` (raw page dumps), `/tmp/eb-verify3.py` (parse script), `/tmp/batch3-places.json` (23 venue verifications), `/tmp/batch3-review.txt` (376-line manual review list).

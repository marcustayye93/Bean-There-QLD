# PUBLISH PACKET — Events Batch 7

**Queensland Adventure — weekly discovery curation, Monday 2026-10-19 (Australia/Brisbane)**
**File:** `scripts/events-batch-7.json` — 22 records (6 Brisbane City Council Trumba, 16 Eventbrite)
**Status:** Verified batch for live publishing under Marcus's standing auto-publish rule (2026-09-14). Merge and push follow this packet.

---

## TIME-SENSITIVE — starts within 7 days, before 2026-10-26 (7 of 22)

Publish promptly or these lose value:

| Date | Event | Suburb | Price |
|---|---|---|---|
| Tue 2026-10-20 | Bush Kindy: National Bird Week | Karawatha | Free |
| Tue 2026-10-20 | Bush Kindy: Stanley the Brush Turkey | Chermside West | Free |
| Tue 2026-10-20 | Gumtreekids messy play - Halloween | New Farm | See website |
| Tue 2026-10-20 | Lord Mayor's City Hall Concerts - Going For Gold with Andrej Kouznetsov and Blake Humphrey | Brisbane City | Free |
| Wed 2026-10-21 | Gathering: Story : Song | Brisbane City | Free |
| Wed 2026-10-21 | Scribble Station with Sunday Jemmott | Brisbane City | Free |
| Wed 2026-10-21 | The Kreative Fairies presents Fairy Rhyme Time | Elanora | Free |

Later keepers (2026-10-31 to 2026-11-08): Halloween Cookie Decorating at Stockland Birtinya, Monster Hunt at Kawana, Trick or Treat at Historic Rivermill, World Festival of Magic (Forest Lake), Diwali Celebration - The Golden Glow Gathering (Kedron-Wavell), Sea Slug Survey in the Rocky Shores (Burleigh Heads), Movies Under the Stars: Cats in the Museum 2 (Burleigh Heads), Christmas Twilight Markets @ The Well, Fun Factory: Paper Zoo (Toowoomba), Grand Diwali at Sea World, Movies Under the Stars: Jumanji (Jacobs Well), PLAN + PLANT YOUR BUTTERFLY GARDEN - Children's Workshops (Tanawha), Pest Fishing Classic (Robina), Training Wheels to Two Wheels and Tweens Freedom to Ride (both Varsity Lakes).

---

## Funnel

| Stage | Count |
|---|---:|
| Listings pipeline new candidates (`fetch-listings.py --all`) | 27 |
| Events pipeline new candidates (`fetch-events.py --all`) | 701 |
| **Combined new candidates this run** | **728** |
| Full proposal queue after both sequential runs | 4,391 |
| Date screen: start date on/after 2026-10-19 | 727 |
| Past-dated dropped at date screen | 1 |
| Unique titles after folding daily occurrences | 570 |
| Broad verification shortlist | 30 (7 Trumba, 23 Eventbrite) |
| **Final keepers** | **22 (6 Trumba, 16 Eventbrite)** |

Pipelines ran sequentially, as required; no overwrite race. The listings run was clean this week: Ticketmaster 0 candidates from 6 API calls, The Urban List 1 candidate (0 new, no 403 this run), WeekendNotes 40 candidates (27 new). The events run was clean: 297 new Trumba candidates from 2,000 BCC feed rows and 404 new Eventbrite candidates across Brisbane, Gold Coast and Sunshine Coast (904 candidates read, 36 pages).

## Drop reasons

Bulk manual drops from the 727 future-dated new candidates, following the batch 1-6 pattern:

| Reason | Basis |
|---|---|
| Adult fitness and Active & Healthy sessions (yoga, Pilates, Tai Chi, Zumba, aqua classes, HIIT, line dancing, martial arts terms) | large share, manual review of the chronological list |
| Recurring library and kids programs (First 5 Forever storytimes, rhyme time, generic Bush Kindy, kids sports, music groups, playgroups, term classes and tasters) | large share, manual review; the two special themed Bush Kindy sessions (National Bird Week, Stanley the Brush Turkey) and the Halloween messy play session were kept instead |
| Adult-only, business, health, civic and support sessions (networking, carer and peer support, immunisation clinics, singles and speed dating, Halloween bar crawls and parties, comedy clubs, professional courses, Melbourne Cup lunches) | large share, manual review |
| Seniors (50 Plus Centre program) and adult craft workshops (macramé, resin, pottery, candle and lamp making) | large share, manual review |
| Already live in the app | 22 candidates with an exact live name match, plus 2 shortlist-stage exact matches (Kids Beginner Crochet Class = live `evt-kids-crochet-class-capalaba`; Wheely Fun = live `evt-wheely-fun`) |
| Verification failures at page level | 2, listed below |
| Shortlist fit drops after verification | 4, listed below |

### Shortlist drops after verification (fit, duplicate or scope)

Bush Kindy - National Bird Week on Eventbrite (Wed 2026-10-21 session at Karawatha; folded into the kept Trumba record for the Tue 2026-10-20 session, whose feed booking link covers the program); Halloween Activity at the Church of Jesus Christ of Latter-day Saints, Upper Coomera (the Eventbrite page carries no description beyond the title, so no honest listing can be written); Gold Coast Multicultural Expo 2026 (a service-provider and employment-pathways expo at Southport Sharks, weak family-activity fit); Lord Mayor's Photographic Awards 2026 exhibition (the fresh feed carries only today's 2026-10-19 occurrence with no verified run end date, so a record would expire the day it publishes).

## Verification method

- **BCC Trumba (6 keepers):** verified against a fresh OpenDataSoft CSV downloaded 2026-10-19 (2,000 rows). Every keeper was matched by subject, date, venue, cost, age text and geolocation in the fresh feed. Coordinates come from the feed geolocation column. The Dark Side of the Moon planetarium show in the same feed window was dropped at review again: the feed itself says it features mature themes and is not recommended for children.
- **Eventbrite (16 keepers):** all 21 shortlisted pages were fetched with a Chrome browser user agent. Every keeper shows JSON-LD `eventStatus: https://schema.org/EventScheduled`, a `startDate` in Australia/Brisbane matching the expected date, and structured `offers.availability: InStock` (four keepers carry it as an AggregateOffer availability string). Venue name, address and coordinates come from the page's embedded venue record. Prices come from the JSON-LD AggregateOffer lowPrice/highPrice. The words "sold out" in page text were not trusted; only the structured availability field decided.
- **Google Places:** every Eventbrite keeper venue was searched and confirmed `businessStatus: OPERATIONAL` (The Pines Elanora, Stockland Birtinya Shopping Centre, Kawana Shoppingworld, Historic Rivermill, St John's Anglican College Forest Lake, Kedron-Wavell, John Laws Park, Burleigh Heads Mowbray Park SLSC, The Well Upper Coomera, Toowoomba City Library, Sea World, Riesenweber Park, Maroochy Regional Bushland Botanic Garden, Robina Common, Varsity Central Park).
- **Prices:** 18 of 22 are free. Paid keepers are taken honestly from the source: Monster Hunt at Kawana A$5, PLAN + PLANT YOUR BUTTERFLY GARDEN - Children's Workshops A$10, Grand Diwali at Sea World from A$40.63. The Diwali Golden Glow Gathering shows free and ticketed options in its offer range (to A$266.03), so its price stays 0 with a "see official listing" note. Gumtreekids messy play shows "See website" in the council feed, so its price stays null with a see-website note.
- **Dates, venues, prices, coordinates, business details:** nothing invented. Australian English, AUD, Australia/Brisbane throughout.

## Per-event verification

| Event | Date(s) | Venue check | Price | Status |
|---|---|---|---|---|
| Bush Kindy: National Bird Week | 2026-10-20 | Karawatha Forest Discovery Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Bush Kindy: Stanley the Brush Turkey | 2026-10-20 | Downfall Creek Bushland Centre, feed-confirmed | Free, feed-confirmed, ages 3-5 | ✅ |
| Gumtreekids messy play - Halloween | 2026-10-20 | New Farm Park, feed-confirmed | See website, feed-confirmed, ages 6 months-5 | ✅ |
| Lord Mayor's City Hall Concerts: Going For Gold | 2026-10-20 | Brisbane City Hall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Gathering: Story : Song | 2026-10-21 | Queen Street Mall, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Scribble Station with Sunday Jemmott | 2026-10-21 | Museum of Brisbane, feed-confirmed | Free, feed-confirmed, all ages | ✅ |
| Fairy Rhyme Time (Elanora) | 2026-10-21 | The Pines Elanora — OPERATIONAL | Free, InStock | ✅ |
| Halloween Cookie Decorating (Birtinya) | 2026-10-31 | Stockland Birtinya — OPERATIONAL | Free, InStock | ✅ |
| Monster Hunt at Kawana | 2026-10-31 | Kawana Shoppingworld — OPERATIONAL | A$5, InStock | ✅ |
| Trick or Treat at Historic Rivermill | 2026-10-31 | Historic Rivermill — OPERATIONAL | Free, InStock | ✅ |
| World Festival of Magic | 2026-10-31 | St John's Anglican College — OPERATIONAL | Free, InStock | ✅ |
| Diwali Celebration - Golden Glow Gathering | 2026-10-31 | Kedron-Wavell — OPERATIONAL | Free/ticketed, InStock | ✅ |
| Sea Slug Survey in the Rocky Shores | 2026-11-03 | John Laws Park — OPERATIONAL | Free, InStock | ✅ |
| Movies Under the Stars: Cats in the Museum 2 | 2026-11-06 | Burleigh Beach / Burleigh Heads Mowbray Park SLSC — OPERATIONAL | Free, InStock | ✅ |
| Christmas Twilight Markets @ The Well | 2026-11-07 | The Well, Upper Coomera — OPERATIONAL | Free, InStock | ✅ |
| Fun Factory: Paper Zoo | 2026-11-07 | Toowoomba City Library — OPERATIONAL | Free, InStock | ✅ |
| Grand Diwali at Sea World | 2026-11-07 | Sea World — OPERATIONAL | From A$40.63, InStock | ✅ |
| Movies Under the Stars: Jumanji (Jacobs Well) | 2026-11-07 | Riesenweber Park — OPERATIONAL | Free, InStock | ✅ |
| Butterfly Garden Children's Workshops | 2026-11-07 | Maroochy Regional Bushland Botanic Garden — OPERATIONAL | A$10, InStock | ✅ |
| Pest Fishing Classic | 2026-11-07 | Robina Common — OPERATIONAL | Free, InStock | ✅ |
| Training Wheels to Two Wheels (Varsity Lakes) | 2026-11-08 | Varsity Central Park — OPERATIONAL | Free, InStock, ages 4+ | ✅ |
| Tweens Freedom to Ride (Varsity Lakes) | 2026-11-08 | Varsity Central Park — OPERATIONAL | Free, InStock, Grades 4-7 | ✅ |

## Verification failures (dropped)

| Candidate | Date | Failure |
|---|---|---|
| Sensory friendly sessions (The Corner, State Library) | 2026-10-25 | Structured `offers.availability: SoldOut` (third week running) |
| Free Halloween Kids Painting Workshop (Brendale) | 2026-10-30 | Structured `offers.availability: SoldOut` |

## Caveats

1. **7 of 22 records start within 7 days**, five of them on Tuesday 2026-10-20. Merge promptly.
2. **Tweens Freedom to Ride is listed for Grades 4-7** on Eventbrite. The record sets ages 9-12 and states the grade range in the description.
3. **Trick or Treat at Historic Rivermill** shows an 08:00 start in its structured data with trick-or-treating for costumed visitors. The record stores the date (2026-10-31) with a Full day duration; the app does not store a start time.
4. **Halloween Cookie Decorating and Monster Hunt at Kawana** run as short booked sessions (15 minutes in the structured data). Both records use an "Under 1 hour" duration.
5. **Movies Under the Stars: Jumanji (Jacobs Well)** sits at latitude -27.7799, just north of the zone helper's Gold Coast rectangle (-27.80). Its zone was set to Gold Coast manually, matching its region and the batch 6 treatment of the northern Gold Coast hinterland.
6. **The Urban List recovered this run** (1 candidate, 0 new) after two weeks of HTTP 403.
7. Eventbrite times were read from JSON-LD with +10:00 (AEST). Durations are coarse buckets per batch 1-6 convention.

## Files

- `scripts/events-batch-7.json` — 22 records, batch 1-6 schema (26 fields), unique IDs, no overlap with the 299 records in `data/activities.json`.
- Evidence (internal, under the goal workspace): fresh BCC CSV, 21 Eventbrite page dumps with a JSON-LD verification summary, Google Places results, the chronological review lists and the batch builder, all in `~/workspace/goals/the-queensland-adventure-app/hidden_files/batch7-2026-10-19/`.

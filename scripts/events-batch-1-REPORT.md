# Events batch 1 — curation report (2026-09-12)

**Batch file:** `scripts/events-batch-1.json` — 25 records, all `is_event: true`, `category: "events"`, `live: true`.
**Nothing else touched:** `data/activities.json`, `app.js` and all live files are unmodified. Nothing pushed.

## Funnel

- **503** candidates in `data/candidates.json` (300 trumba, 160 eventbrite, 40 weekendnotes, 3 urbanlist).
- **199** had `date` before 2026-09-12 (all 40 weekendnotes + all 3 urbanlist were past-dated — nothing future from those two sources).
- **304** future-dated candidates reviewed (153 eventbrite, 151 trumba).
- **25** kept. **279** dropped.

## Drop reasons (of the 304 future candidates)

| Reason | Count |
|---|---|
| Weaker fit / not shortlisted (general workshops, meetups, talks, tours with no clear kid hook) | 162 |
| Adult fitness/sport sessions (yoga, zumba, tai chi, aqua aerobics, boxing, trail runs, cycling, Bridge to Brisbane) | 76 |
| Civic/volunteer/adult-heritage (bushcare, green waste, grave cleaning, medal conservation, convict tours, greeters) | 14 |
| Parenting/childcare/religious/support groups (playgroups, kindy info, church fellowship, support groups) | 13 |
| Adult-oriented (Date Night!, hypnosis show, Diwali fashion sale, acupuncture, Lunch and Learn) | 6 |
| Outside Queensland (Ballina, Casino NSW listings) | 4 |
| Recurring term classes, not pop-ups (weekly French, circus term, athletics) | 3 |
| Cancelled in feed | 1 |
| Pet-focused, not kid-focused (Barktoberfest) | 1 |

Deliberately excluded despite being kid-adjacent: The Red Dress and Artist in Residence: Renee Kire (weaker kid hook, kept batch tight); Offspring 2026 (church musical, religious framing); Secret Garden (live-music event, not clearly kid-focused).

## Verification method

- **Trumba (15 events):** the trumba embed URLs do not render server-side, so each event was verified against a **fresh pull of the BCC OpenDataSoft CSV** (2026-09-12) — subject, start/end datetimes, cost and age fields all match the candidate. Date ranges were derived from the feed's occurrence rows (e.g. daily exhibition occurrences 12 Sep–15 Oct).
- **Eventbrite (10 events):** each page fetched with a browser User-Agent. Checked `og:title`, JSON-LD `startDate`/`endDate`, `eventStatus` (all `EventScheduled`), venue name, and scanned for ended/cancelled/sold-out markers — none found. Four pages had redirected to a newer canonical ticket ID; the canonical URL from the page is used in the batch.
- **Geocoding:** Eventbrite candidates carry no coordinates; all 10 venues were confirmed via Google Places (all OPERATIONAL where a status applied): Rocklea Showgrounds, Pimpama River Parklands, Sandstone Point Hotel, Dreamworld, Barrett Street Park, State Library of Queensland, Surfers Paradise Esplanade, 1/5 Pring St Ipswich, 47 Fleming Rd Chapel Hill, Stockland Aura (Bells Creek).
- **Duplicates:** checked against live `data/activities.json` names. The only overlaps are events *at* existing permanent venues (Dreamworld, Museum of Brisbane, Sir Thomas Brisbane Planetarium) — these are time-bound pop-ups at those venues, which is the point, not duplicates.
- **Prices:** 13 free (feed-confirmed), 2 planetarium shows at $11 (feed-confirmed), 10 left `null` with "See official listing for ticket details" — no prices invented.

## Per-event verification notes

| Event | Date(s) | What was checked |
|---|---|---|
| Bayside Spring Festival 2026 (George Clayton Park, Manly) | 12–13 Sep | Fresh BCC CSV: 12 Sep 10:00–21:00 + 13 Sep occurrence; Free; all ages |
| Brisbane Sculpture Festival 2026 (Botanic Gardens Mt Coot-tha) | 12 Sep–15 Oct | Fresh BCC CSV: daily occurrences; Free; all ages |
| Nundah Festival (Nundah Village) | 13 Sep | Fresh BCC CSV: 13 Sep 09:00–15:00; Free; all ages |
| Outdoor Cinema: A Minecraft Movie (Thompson Estate Reserve) | 12 Sep | Fresh BCC CSV: 12 Sep 18:00–22:00; Free; all ages |
| Shri Krishna Janmashtami 2026 (Bracken Ridge Hall) | 12 Sep | Fresh BCC CSV: 12 Sep 16:15–19:00; cost blank → price null; all ages |
| Stories You Wear: Magpie Goose (Museum of Brisbane) | 12 Sep–15 Oct | Fresh BCC CSV: daily occurrences; Free; all ages |
| Precious (Museum of Brisbane) | on now–2 Apr 2027 | Fresh BCC CSV: run ends 2027-04-02; Free; all ages. Candidate date was 2025-04-07 (exhibition start); date_start set to today |
| Little Artist's Eye Spy (Museum of Brisbane) | 12 Sep–15 Oct | Fresh BCC CSV: daily occurrences; Free; infants/toddlers/preschool/kids |
| Clock Tower Tour (Museum of Brisbane) | 12 Sep–15 Oct | Fresh BCC CSV: daily occurrences; Free; all ages |
| Perfect Little Planet (Planetarium) | 12 Sep (recurring) | Fresh BCC CSV: Adult $11, Child (3–14) $11; ages 4+; date_end null (recurring schedule) |
| Tycho Goes to Mars (Planetarium) | 12 Sep (recurring) | Fresh BCC CSV: Adult $11, Child (3–14) $11; ages 4+; date_end null |
| Wheely Fun (Fischer Family Park, Rochedale) | 12 Sep–3 Oct | Fresh BCC CSV: recurring sessions; Free; kids |
| Queen's Wharf Brisbane Art Prize (Petrie Terrace Gallery) | 12–13 Sep | Fresh BCC CSV: two occurrences; Free; all ages |
| Warrajamba (Museum of Brisbane) | 12 Sep–15 Oct | Fresh BCC CSV: daily occurrences; Free; all ages |
| Sailing and kayaking (Breakwater Park, Wynnum) | 12 Sep | Fresh BCC CSV: 12 Sep sessions; Free; all ages |
| Kidchella (Esplanade, Surfers Paradise) | 12–13 Sep | Eventbrite page: EventScheduled, 12 Sep 10:00 → 13 Sep 16:00; price not published → null |
| Monster Truck Family Spectacular (Rocklea Showgrounds) | 26 Sep | Eventbrite page: EventScheduled 17:00–19:00; price not published → null |
| Movies Under the Stars: The Magic Faraway Tree (Ormeau) | 26 Sep | Eventbrite page: EventScheduled 16:30–20:30; Free |
| Monster Jump Sandstone Point | 19 Sep | Eventbrite page: EventScheduled 09:30–15:30; page canonical ticket ID 1997929273239 used |
| Diwali Edition at Dreamworld (Coomera) | 19 Sep | Eventbrite page: EventScheduled 18:00–23:00; price not published → null |
| International Observe the Moon (Barrett St Park, Bracken Ridge) | 19 Sep | Eventbrite page: EventScheduled 17:00–22:00; SEQ Astronomical Society |
| Aura Monster Machine Day (Bells Creek, Sunshine Coast) | 26 Sep | Eventbrite page: EventScheduled 09:00–10:00; canonical ticket ID 1999355477053 used |
| Spring Fair 2026 (Ipswich) | 21 Sep | Eventbrite page: EventScheduled 09:00–14:00; canonical ticket ID 1991749624744 used |
| Forest Family Sundays THECA (Chapel Hill) | 13 Sep | Eventbrite page: EventScheduled 11:00–13:00; Mt Coot-tha forest |
| Sensory friendly sessions (The Corner, SLQ) | 20 Sep | Eventbrite page: EventScheduled 09:00–09:30; canonical ticket ID 1996061875803 used |

## Open questions / things I'm unsure about

- **Janmashtami + 10 Eventbrite events have `price_aud: null`** — prices weren't published in the feeds. Copy says "see official listing" rather than guessing.
- **Kidchella and today's (12 Sep) events** are partially underway already; they're valid but time-sensitive — a same-day push matters.
- **Precious** uses `date_start: 2026-09-12` (today) even though the exhibition opened in 2025 — honest as "on now", but flag if the app should show original start dates for ongoing exhibitions.
- **Planetarium shows** have `date_end: null` (recurring sessions, end of run unknown from the feed).
- **WeekendNotes/Urban List contributed zero** future candidates — the discovery adapters for those sources may need attention if events are the priority going forward.
- The batch is Brisbane/SEQ-heavy (13 of 25 in Brisbane CBD & Inner); regional Queensland pop-ups barely exist in the current candidate pool.

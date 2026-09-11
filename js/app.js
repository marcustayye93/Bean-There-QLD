/* The Queensland Adventure — v1 app logic. Dependency-free vanilla JS.
 *
 * Pure helpers live at the top (no DOM access) so they can be unit-tested
 * in node: `node -e "const t=require('./js/app.js'); ..."`. The DOM app
 * only boots when `document` exists.
 */
(() => {
'use strict';

/* ==================== pure helpers ==================== */

const DAY_NAMES = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const CATEGORIES = [
  ['soccer', 'Soccer'],
  ['basketball', 'Basketball'],
  ['craft', 'Craft'],
  ['camps', 'Holiday camps'],
  ['scouts', 'Scouts'],
  ['lego', 'Lego'],
  ['playgrounds', 'Playgrounds & parks'],
  ['museums', 'Museums & science'],
  ['animals', 'Animals & zoos'],
  ['theme-parks', 'Theme parks'],
  ['water', 'Water play'],
  ['shows', 'Shows & performing arts']
];

const INTERESTS = [
  ['soccer', 'Soccer'],
  ['basketball', 'Basketball'],
  ['lego', 'Lego'],
  ['craft', 'Craft'],
  ['animals', 'Animals'],
  ['theme-parks', 'Theme parks'],
  ['water', 'Water play'],
  ['science', 'Science'],
  ['outdoor', 'Outdoors'],
  ['scouts', 'Scouts'],
  ['shows', 'Shows']
];

/* ---- mood photos: decorative category stills, never a venue lookalike ---- */
const U = 'https://images.unsplash.com/';
const Q = '?w=900&q=70&auto=format&fit=crop';
const CATEGORY_PHOTOS = {
  water: [
    U + 'photo-1530549387789-4c1017266635' + Q, // swimmer in pool lanes
    U + 'photo-1576013551627-0cc20b96c2a7' + Q,  // resort pool
    U + 'photo-1507525428034-b723cf961d3e' + Q   // beach at sunset
  ],
  playgrounds: [
    'https://live.staticflickr.com/3794/9957671356_bd475e434a_b.jpg', // Toowoomba QLD playground (CC BY-SA)
    'https://live.staticflickr.com/3302/3338689843_22d84905f4_b.jpg', // playground structure (CC BY-SA)
    'https://live.staticflickr.com/4167/34262948212_47e8a944a7_b.jpg'  // park playground (CC0)
  ],
  soccer: [
    U + 'photo-1579952363873-27f3bade9f55' + Q, // ball on grass
    U + 'photo-1522778119026-d647f0596c20' + Q  // stadium
  ],
  basketball: [
    U + 'photo-1546519638-68e109498ffc' + Q,  // hoop
    U + 'photo-1519861531473-9200262188bf' + Q // ball on court
  ],
  craft: [
    U + 'photo-1513364776144-60967b0f800f' + Q, // paint brushes
    U + 'photo-1452860606245-08befc0ff44b' + Q   // craft supplies
  ],
  camps: [
    U + 'photo-1504280390367-361c6d9f38f4' + Q, // tent
    U + 'photo-1478131143081-80f7f84ca84d' + Q  // campfire
  ],
  scouts: [
    U + 'photo-1478131143081-80f7f84ca84d' + Q, // campfire
    U + 'photo-1504280390367-361c6d9f38f4' + Q  // tent
  ],
  lego: [
    U + 'photo-1558060370-d644479cb6f7' + Q, // lego build
    U + 'photo-1587654780291-39c9404d746b' + Q, // brick pile
    U + 'photo-1566140967404-b8b3932483f5' + Q  // minifigures
  ],
  museums: [
    U + 'photo-1566127444979-b3d2b654e3d7' + Q, // museum hall
    U + 'photo-1554907984-15263bfd63bd' + Q      // gallery wall
  ],
  animals: [
    U + 'photo-1546182990-dffeafbe841d' + Q, // lion
    U + 'photo-1459262838948-3e2de6c1ec80' + Q, // koala
    U + 'photo-1527118732049-c88155f2107c' + Q   // panda
  ],
  'theme-parks': [
    U + 'photo-1516051662687-567d7c4e8f6a' + Q // roller coaster
  ],
  shows: [
    U + 'photo-1507924538820-ede94a04019d' + Q, // theatre stage
    U + 'photo-1514306191717-452ec28c7814' + Q  // concert crowd
  ]
};
const HERO_PHOTO = 'https://live.staticflickr.com/42/112080998_d47077d191_b.jpg'; // Surfers Paradise, Gold Coast (CC BY-SA)

/* Deterministic photo pick per activity so cards are stable across renders. */
function photoFor(a) {
  const pack = CATEGORY_PHOTOS[a.category] || CATEGORY_PHOTOS.playgrounds;
  const s = String((a && a.id) || '');
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return pack[h % pack.length];
}

function esc(s) {
  return String(s == null ? '' : s).replace(/[&<>"']/g, c => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[c]));
}

function parseDay(s) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(s || '').trim());
  if (!m) return null;
  const d = new Date(+m[1], +m[2] - 1, +m[3], 12, 0, 0); // noon: immune to DST edges
  if (d.getFullYear() !== +m[1] || d.getMonth() !== +m[2] - 1 || d.getDate() !== +m[3]) return null;
  return d;
}

function startOfDay(d) {
  const x = new Date(d);
  x.setHours(0, 0, 0, 0);
  return x;
}

function daysBetween(a, b) {
  return Math.round((startOfDay(b) - startOfDay(a)) / 86400000);
}

function addDays(d, n) {
  const x = new Date(d);
  x.setDate(x.getDate() + n);
  return x;
}

function fmtDay(d) {
  return DAY_NAMES[d.getDay()] + ' ' + d.getDate() + ' ' + MONTH_NAMES[d.getMonth()];
}

function fmtDayYear(d) {
  return fmtDay(d) + ' ' + d.getFullYear();
}

function isoDay(d) {
  const p = n => String(n).padStart(2, '0');
  return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
}

function haversineKm(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const toRad = Math.PI / 180;
  const dLat = (lat2 - lat1) * toRad;
  const dLon = (lon2 - lon1) * toRad;
  const a = Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1 * toRad) * Math.cos(lat2 * toRad) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(a));
}

const DRIVE_KMH = 40; // honest heuristic: suburban driving with lights

function driveMinutes(km) {
  return (km / DRIVE_KMH) * 60;
}

function driveLabel(mins) {
  const r = Math.max(5, Math.round(mins / 5) * 5);
  return '~' + r + ' min drive (est.)';
}

function base64urlEncode(str) {
  let b64;
  if (typeof btoa !== 'undefined') {
    b64 = btoa(unescape(encodeURIComponent(str)));
  } else {
    b64 = Buffer.from(str, 'utf8').toString('base64');
  }
  return b64.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function base64urlDecode(s) {
  let b64 = String(s).replace(/-/g, '+').replace(/_/g, '/');
  while (b64.length % 4) b64 += '=';
  if (typeof atob !== 'undefined') {
    return decodeURIComponent(escape(atob(b64)));
  }
  return Buffer.from(b64, 'base64').toString('utf8');
}

function ageBounds(a) {
  const lo = typeof a.age_min === 'number' ? a.age_min : 0;
  const hi = typeof a.age_max === 'number' ? a.age_max : 16;
  return [lo, hi];
}

function suitsAge(a, age) {
  const [lo, hi] = ageBounds(a);
  return lo <= age && age <= hi;
}

function ageRangeLabel(a) {
  const [lo, hi] = ageBounds(a);
  return 'Ages ' + lo + '-' + hi;
}

function priceLabel(a) {
  if (a.price_aud === 0) return 'Free';
  if (a.price_aud == null) return 'Check with provider';
  return '$' + a.price_aud;
}

function categoryLabel(c) {
  const f = CATEGORIES.find(x => x[0] === c);
  return f ? f[1] : String(c || 'Other');
}

function indoorLabel(v) {
  if (v === 'indoor') return 'Indoors';
  if (v === 'outdoor') return 'Outdoors';
  if (v === 'both') return 'Indoor & outdoor';
  return '';
}

function bucketMinutes(b) {
  if (b === '15') return 15;
  if (b === '30') return 30;
  if (b === '60') return 60;
  if (b === '120') return 120;
  return Infinity;
}

function bucketLabel(b) {
  if (b === '15') return '15 min';
  if (b === '30') return '30 min';
  if (b === '60') return '1 hour';
  if (b === '120') return '2 hours';
  return 'any distance';
}

function activityDrive(a, loc) {
  if (!loc || a.lat == null || a.lng == null) return null;
  return driveMinutes(haversineKm(loc.lat, loc.lng, a.lat, a.lng));
}

/* ---- school holiday calendar ---- */

function holidayPeriods(holidays) {
  const ps = (holidays && holidays.periods) || [];
  return ps
    .filter(p => p && p.type === 'holiday' && parseDay(p.start) && parseDay(p.end))
    .sort((a, b) => (a.start < b.start ? -1 : a.start > b.start ? 1 : 0));
}

function holidayStatus(periods, today) {
  const t = startOfDay(today);
  const hol = holidayPeriods({ periods });
  for (const p of hol) {
    const s = startOfDay(parseDay(p.start));
    const e = startOfDay(parseDay(p.end));
    if (t >= s && t <= e) return { state: 'in', period: p, daysLeft: daysBetween(t, e) };
  }
  for (const p of hol) {
    const s = startOfDay(parseDay(p.start));
    if (s > t) return { state: 'before', period: p, daysAway: daysBetween(t, s) };
  }
  return { state: 'none' };
}

function lengthLabel(p) {
  const total = daysBetween(parseDay(p.start), parseDay(p.end)) + 1;
  if (total % 7 === 0) {
    const w = total / 7;
    return w + (w === 1 ? ' week' : ' weeks');
  }
  return total + (total === 1 ? ' day' : ' days');
}

function bannerText(st) {
  if (!st || st.state === 'none') return null;
  const p = st.period;
  if (st.state === 'in') {
    if (st.daysLeft <= 0) return p.name + ' ends today';
    return p.name + ' end ' + fmtDay(parseDay(p.end)) + ' — ' +
      st.daysLeft + (st.daysLeft === 1 ? ' day' : ' days') + ' left';
  }
  const when = st.daysAway <= 0 ? 'starts today'
    : st.daysAway === 1 ? 'starts tomorrow'
    : 'starts ' + fmtDay(parseDay(p.start)) + ' (' + st.daysAway + ' days away)';
  return p.name + ' — ' + lengthLabel(p) + ', ' + when;
}

/* ---- filtering / sorting (pure; f = filter args) ---- */

function filterActivities(list, f) {
  const q = (f.q || '').trim().toLowerCase();
  const out = list.filter(a => {
    if (f.category && a.category !== f.category) return false;
    if (f.freeOnly && a.price_aud !== 0) return false;
    if (q) {
      const hay = (a.name + ' ' + (a.description || '') + ' ' + (a.suburb || '')).toLowerCase();
      if (!hay.includes(q)) return false;
    }
    if (f.loc && f.bucketMin !== Infinity) {
      const mins = activityDrive(a, f.loc);
      if (mins == null || mins > f.bucketMin) return false;
    }
    return true;
  });

  const interestScore = a => {
    let s = 0;
    for (const i of (a.interests || [])) {
      if (f.c1Interests.includes(i)) s += 2;
      else if (f.c2Interests.includes(i)) s += 1;
    }
    return s;
  };
  const byName = (x, y) => String(x.name).localeCompare(String(y.name));

  if (f.sort === 'nearest' && f.loc) {
    out.sort((x, y) => {
      const dx = activityDrive(x, f.loc);
      const dy = activityDrive(y, f.loc);
      return (dx == null ? Infinity : dx) - (dy == null ? Infinity : dy) || byName(x, y);
    });
  } else if (f.sort === 'cheapest') {
    out.sort((x, y) =>
      (x.price_aud == null ? Infinity : x.price_aud) - (y.price_aud == null ? Infinity : y.price_aud) ||
      byName(x, y));
  } else if (f.sort === 'az') {
    out.sort(byName);
  } else { // suggested
    out.sort((x, y) =>
      interestScore(y) - interestScore(x) ||
      ((y.live ? 1 : 0) - (x.live ? 1 : 0)) ||
      byName(x, y));
  }
  if (f.forHolidays) {
    // stable: holiday-only programs float to the top of the current order
    out.sort((x, y) => ((y.holiday_only ? 1 : 0) - (x.holiday_only ? 1 : 0)));
  }
  return out;
}

function recommended(list, f) {
  // f: { c1Interests, loc, bucketMin }
  return list.filter(a => {
    if (a.live === false) return false; // never recommend sample listings
    if (!(a.interests || []).some(i => f.c1Interests.includes(i))) return false;
    if (f.loc && f.bucketMin !== Infinity) {
      const m = activityDrive(a, f.loc);
      if (m == null || m > f.bucketMin) return false;
    }
    return true;
  }).slice(0, 12);
}

/* ---- plan sharing ---- */

function encodePlan(plan) {
  return base64urlEncode(JSON.stringify(plan));
}

function decodePlan(s) {
  const arr = JSON.parse(base64urlDecode(s));
  if (!Array.isArray(arr)) throw new Error('plan is not an array');
  return arr.filter(e =>
    e && typeof e.id === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(e.date || '') && parseDay(e.date));
}

function blockDays(p) {
  const s = startOfDay(parseDay(p.start));
  const e = startOfDay(parseDay(p.end));
  const days = [];
  for (let d = s; d <= e; d = addDays(d, 1)) days.push(new Date(d));
  return days;
}

function planText(blockName, blockStart, blockEnd, days) {
  // days: [{ date: Date, items: [activity] }]
  const lines = [
    'The Queensland Adventure — holiday plan',
    blockName + ' (' + fmtDay(blockStart) + ' – ' + fmtDay(blockEnd) + ')',
    ''
  ];
  for (const d of days) {
    lines.push(fmtDay(d.date));
    if (!d.items.length) {
      lines.push('• Nothing planned yet');
    }
    for (const a of d.items) {
      lines.push('• ' + a.name + ' — ' + (a.suburb || 'Queensland') + ' — ' + priceLabel(a) +
        (a.booking_url ? ' — Book: ' + a.booking_url : ''));
    }
    lines.push('');
  }
  return lines.join('\n').trimEnd();
}

// Export pure API for node tests (no-op in browsers).
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    esc, parseDay, fmtDay, fmtDayYear, isoDay, daysBetween, addDays,
    haversineKm, driveMinutes, driveLabel, base64urlEncode, base64urlDecode,
    suitsAge, ageRangeLabel, ageBounds, priceLabel, categoryLabel, indoorLabel,
    bucketMinutes, bucketLabel, activityDrive,
    holidayPeriods, holidayStatus, lengthLabel, bannerText,
    filterActivities, recommended, encodePlan, decodePlan, blockDays, planText,
    CATEGORIES, INTERESTS, CATEGORY_PHOTOS, HERO_PHOTO, photoFor
  };
}
/* ==================== app state & DOM ==================== */

const LS_SETTINGS = 'btq-settings';
const LS_FAVS = 'btq-favourites';
const LS_PLAN = 'btq-plan';

const DEFAULT_SETTINGS = {
  child1: { name: 'Child 1', interests: [] },
  child2: { name: 'Child 2', interests: [] },
  postcode: ''
};

let settings, favourites, plan;
let activities = [];
let holidays = null;
let postcodes = null;
let postcodeLoc = null; // { suburb, lat, lng } | null
let postcodeState = 'unset'; // unset | ok | unknown | nolookup
let filters = { category: '', freeOnly: false, q: '', bucket: 'any', sort: 'suggested', forHolidays: false };
let currentTab = 'find';
let planBlockIdx = 0;
let plandateActivityId = null;
let searchTimer = null;
let toastTimer = null;

function $(id) { return document.getElementById(id); }

function loadSettings() {
  const out = JSON.parse(JSON.stringify(DEFAULT_SETTINGS));
  try {
    const raw = localStorage.getItem(LS_SETTINGS);
    if (!raw) return out;
    const s = JSON.parse(raw);
    for (const k of ['child1', 'child2']) {
      if (s[k]) {
        if (typeof s[k].name === 'string' && s[k].name.trim()) out[k].name = s[k].name.trim().slice(0, 24);
        if (Array.isArray(s[k].interests)) {
          out[k].interests = s[k].interests.filter(i => INTERESTS.some(x => x[0] === i));
        }
      }
    }
    if (typeof s.postcode === 'string' && /^\d{4}$/.test(s.postcode)) out.postcode = s.postcode;
  } catch (e) { /* corrupted: fall back to defaults */ }
  return out;
}

function loadFavs() {
  try {
    const v = JSON.parse(localStorage.getItem(LS_FAVS) || '[]');
    return Array.isArray(v) ? v.filter(x => typeof x === 'string') : [];
  } catch (e) { return []; }
}

function loadPlan() {
  try {
    const v = JSON.parse(localStorage.getItem(LS_PLAN) || '[]');
    if (!Array.isArray(v)) return [];
    return v.filter(e => e && typeof e.id === 'string' && parseDay(e.date));
  } catch (e) { return []; }
}

function saveSettings() { localStorage.setItem(LS_SETTINGS, JSON.stringify(settings)); }
function saveFavs() { localStorage.setItem(LS_FAVS, JSON.stringify(favourites)); }
function savePlan() { localStorage.setItem(LS_PLAN, JSON.stringify(plan)); }

/* ---------- boot ---------- */

function boot() {
  settings = loadSettings();
  favourites = loadFavs();
  plan = loadPlan();

  bindUI();
  buildInterestCheckboxes();
  renderCategoryChips();
  setStickTop();
  window.addEventListener('resize', setStickTop);

  loadAll().then(() => {
    resolvePostcode();
    defaultPlanBlock();
    renderAll();
    checkSharedPlan();
  });
}

function setStickTop() {
  const h = $('topbar').offsetHeight;
  document.documentElement.style.setProperty('--stick-top', h + 'px');
}

async function fetchJson(path) {
  try {
    const r = await fetch(path, { cache: 'no-store' });
    if (!r.ok) return null;
    return await r.json();
  } catch (e) {
    return null;
  }
}

async function loadAll() {
  const [a, h, p] = await Promise.all([
    fetchJson('data/activities.json'),
    fetchJson('data/holidays.json'),
    fetchJson('data/postcodes.json')
  ]);
  activities = (a && Array.isArray(a.activities)) ? a.activities : null;
  holidays = h;
  postcodes = p;
}

function renderAll() {
  if (activities === null) {
    $('results').innerHTML =
      '<div class="load-error"><p>We couldn\'t load the activities list. Check your connection and try again.</p>' +
      '<button type="button" class="btn" data-action="retry-load">Try again</button></div>';
    $('results-count').textContent = '';
    $('recommended').hidden = true;
    return;
  }
  renderBanner();
  renderPostcodeNote();
  renderResults();
  renderSaved();
  renderPlan();
  updateSavedCount();
}

/* ---------- holiday banner ---------- */

function renderBanner() {
  const banner = $('holiday-banner');
  if (!holidays || !holidays.periods) { banner.hidden = true; return; }
  const st = holidayStatus(holidays.periods, new Date());
  const text = bannerText(st);
  if (!text) { banner.hidden = true; return; }
  banner.hidden = false;
  $('holiday-banner-text').textContent = text;
  $('holidays-chip').setAttribute('aria-pressed', filters.forHolidays ? 'true' : 'false');
}

/* ---------- postcode resolution ---------- */

function resolvePostcode() {
  postcodeLoc = null;
  postcodeState = 'unset';
  const pc = settings.postcode;
  if (!pc) return;
  if (!postcodes || !postcodes.postcodes || Object.keys(postcodes.postcodes).length === 0) {
    postcodeState = 'nolookup';
    return;
  }
  const hit = postcodes.postcodes[pc];
  if (hit && hit.lat != null && hit.lng != null) {
    postcodeLoc = { suburb: hit.suburb || pc, lat: hit.lat, lng: hit.lng };
    postcodeState = 'ok';
  } else {
    postcodeState = 'unknown';
  }
}

function renderPostcodeNote() {
  const note = $('postcode-note');
  const travel = $('travel-select');
  const pcInput = $('postcode-input');
  pcInput.value = settings.postcode || '';

  if (postcodeState === 'ok') {
    note.hidden = false;
    note.innerHTML = '📍 Near ' + esc(postcodeLoc.suburb) + ' ' + esc(settings.postcode) +
      ' — drive times are estimates.';
    travel.disabled = false;
  } else if (postcodeState === 'unknown' || postcodeState === 'nolookup') {
    // Honest degradation: travel filter falls back to "Any distance".
    filters.bucket = 'any';
    travel.value = 'any';
    travel.disabled = true;
    note.hidden = false;
    const why = postcodeState === 'nolookup'
      ? 'Postcode lookup isn\'t available right now.'
      : 'We couldn\'t pin postcode ' + esc(settings.postcode) + ' — no location data for it.';
    note.innerHTML = esc(why) + ' Travel times are off for now.' +
      ' <button type="button" class="link-btn" data-action="open-settings">Re-enter postcode</button>';
  } else {
    travel.disabled = false;
    if (filters.bucket !== 'any') {
      note.hidden = false;
      note.innerHTML = 'Set your postcode to use travel-time estimates.' +
        ' <button type="button" class="link-btn" data-action="open-settings">Open settings</button>';
    } else {
      note.hidden = true;
      note.innerHTML = '';
    }
  }
}

/* ---------- filters UI ---------- */

function renderCategoryChips() {
  const el = $('category-chips');
  let html = '<button type="button" class="chip" data-action="set-category" data-category="" aria-pressed="' +
    (filters.category === '' ? 'true' : 'false') + '">All</button>';
  for (const [val, label] of CATEGORIES) {
    html += '<button type="button" class="chip" data-action="set-category" data-category="' + val +
      '" aria-pressed="' + (filters.category === val ? 'true' : 'false') + '">' + esc(label) + '</button>';
  }
  html += '<button type="button" class="chip chip-free" data-action="toggle-free" aria-pressed="' +
    (filters.freeOnly ? 'true' : 'false') + '">Free</button>';
  el.innerHTML = html;
}

function currentFilterArgs() {
  return {
    c1Interests: settings.child1.interests, c2Interests: settings.child2.interests,
    category: filters.category, freeOnly: filters.freeOnly, q: filters.q,
    bucketMin: bucketMinutes(filters.bucket), loc: postcodeLoc,
    sort: filters.sort, forHolidays: filters.forHolidays
  };
}

/* ---------- results ---------- */

function driveHTML(a) {
  if (postcodeLoc) {
    const mins = activityDrive(a, postcodeLoc);
    if (mins != null) return '<p class="drive">' + esc(driveLabel(mins)) + '</p>';
  }
  return '<p class="drive-hint">Set your postcode for drive times</p>';
}

function cardHTML(a, opts) {
  opts = opts || {};
  const fav = favourites.includes(a.id);
  const badges = [];
  if (a.live === false) badges.push('<span class="badge badge-sample">Sample listing</span>');
  if (a.holiday_only) badges.push('<span class="badge badge-holiday">School holidays only</span>');
  if (a.booking_required) badges.push('<span class="badge badge-booking">Booking required</span>');

  const meta = [];
  const where = [a.suburb, a.region].filter(Boolean).join(' · ');
  if (where) meta.push('<li><span class="k">📍</span> ' + esc(where) + '</li>');
  meta.push('<li><span class="k">👶</span> ' + esc(ageRangeLabel(a)) + '</li>');
  if (a.category) meta.push('<li><span class="k">🏷️</span> ' + esc(categoryLabel(a.category)) + '</li>');
  const indoor = indoorLabel(a.indoor);
  if (indoor) meta.push('<li><span class="k">🚪</span> ' + esc(indoor) + '</li>');
  meta.push('<li><span class="k">💰</span> ' + esc(priceLabel(a)) +
    (a.price_note ? ' <span class="k">(' + esc(a.price_note) + ')</span>' : '') + '</li>');
  if (a.duration) meta.push('<li><span class="k">⏱️</span> ' + esc(a.duration) + '</li>');

  let actions = '';
  if (a.booking_url) {
    actions += '<a class="btn btn-small" href="' + esc(a.booking_url) +
      '" target="_blank" rel="noopener">Book</a>';
  }
  if (fav || opts.alwaysPlan) {
    actions += '<button type="button" class="btn btn-small btn-secondary" data-action="open-plan-date" data-id="' +
      esc(a.id) + '">Add to plan</button>';
  }

  return '<article class="card">' +
    '<img class="card-img" src="' + esc(photoFor(a)) + '" alt="" loading="lazy">' +
    '<div class="card-top"><h3>' + esc(a.name) + '</h3>' +
    '<button type="button" class="heart" data-action="toggle-fav" data-id="' + esc(a.id) +
    '" aria-pressed="' + (fav ? 'true' : 'false') +
    '" aria-label="' + (fav ? 'Remove from favourites' : 'Save to favourites') + '">' +
    (fav ? '♥' : '♡') + '</button></div>' +
    (badges.length ? '<div class="badges">' + badges.join('') + '</div>' : '') +
    (a.description ? '<p class="desc">' + esc(a.description) + '</p>' : '') +
    '<ul class="meta">' + meta.join('') + '</ul>' +
    driveHTML(a) +
    (actions ? '<div class="card-actions">' + actions + '</div>' : '') +
    (a.source && a.source.label
      ? '<p class="source">Source: ' + (a.source.url
        ? '<a href="' + esc(a.source.url) + '" target="_blank" rel="noopener">' + esc(a.source.label) + '</a>'
        : esc(a.source.label)) + '</p>'
      : '') +
    '</article>';
}

function recoCardHTML(a) {
  const fav = favourites.includes(a.id);
  const mins = postcodeLoc ? activityDrive(a, postcodeLoc) : null;
  const url = a.booking_url || (a.source && a.source.url) || null;
  const img = '<img class="reco-img" src="' + esc(photoFor(a)) + '" alt="" loading="lazy">';
  const title = '<h3>' + esc(a.name) + '</h3>';
  return '<div class="reco-card">' +
    (url ? '<a class="reco-link" href="' + esc(url) + '" target="_blank" rel="noopener" aria-label="' + esc(a.name) + '">' + img + '</a>' : img) +
    '<button type="button" class="heart" data-action="toggle-fav" data-id="' + esc(a.id) +
    '" aria-pressed="' + (fav ? 'true' : 'false') +
    '" aria-label="' + (fav ? 'Remove from favourites' : 'Save to favourites') + '">' +
    (fav ? '♥' : '♡') + '</button>' +
    (url ? '<a class="reco-link" href="' + esc(url) + '" target="_blank" rel="noopener">' + title + '</a>' : title) +
    '<p class="reco-meta">' + esc([a.suburb, priceLabel(a)].filter(Boolean).join(' · ')) + '</p>' +
    (mins != null ? '<p class="reco-meta">' + esc(driveLabel(mins)) + '</p>' : '') +
    (a.live === false ? '<p class="reco-meta">Sample listing</p>' : '') +
    '</div>';
}

function resultsCountHTML(n, total) {
  const parts = [n + (n === 1 ? ' activity' : ' activities')];
  if (postcodeLoc && filters.bucket !== 'any') parts.push('under ' + bucketLabel(filters.bucket));
  if (filters.category) parts.push(categoryLabel(filters.category));
  if (filters.freeOnly) parts.push('free');
  if (filters.q) parts.push('matching “' + filters.q + '”');
  if (filters.forHolidays) parts.push('for the next school holidays');
  return parts.join(' · ');
}

function nextWiderBucket() {
  const order = ['15', '30', '60', '120', 'any'];
  const i = order.indexOf(filters.bucket);
  return i >= 0 && i < order.length - 1 ? order[i + 1] : null;
}

function emptyStateHTML() {
  const wider = nextWiderBucket();
  const bits = ['Nothing found'];
  if (postcodeLoc && filters.bucket !== 'any') bits.push('within ' + bucketLabel(filters.bucket));
  if (filters.category) bits.push('in ' + categoryLabel(filters.category));
  if (filters.freeOnly) bits.push('that’s free');
  if (filters.q) bits.push('matching “' + filters.q + '”');
  let html = '<div class="empty"><p>' + esc(bits.join(' ') + '.') + '</p><div class="empty-actions">';
  if (wider) {
    html += '<button type="button" class="btn btn-secondary" data-action="set-bucket" data-bucket="' + wider +
      '">Try under ' + esc(bucketLabel(wider)) + '</button>';
  }
  html += '<button type="button" class="btn btn-secondary" data-action="reset-filters">Show everything</button>';
  html += '</div></div>';
  return html;
}

function renderResults() {
  if (activities === null) return;
  const f = currentFilterArgs();
  const list = filterActivities(activities, f);

  $('results-count').textContent = resultsCountHTML(list.length, activities.length);

  // Recommended row: both children's interests, within the travel bucket.
  const recoBox = $('recommended');
  const recoInterests = [...new Set([...settings.child1.interests, ...settings.child2.interests])];
  if (recoInterests.length) {
    const recos = recommended(activities, {
      c1Interests: recoInterests, loc: postcodeLoc, bucketMin: bucketMinutes(filters.bucket)
    });
    if (recos.length) {
      recoBox.hidden = false;
      $('recommended-title').textContent = 'Recommended';
      $('recommended-row').innerHTML = recos.map(recoCardHTML).join('');
    } else {
      recoBox.hidden = true;
    }
  } else {
    recoBox.hidden = true;
  }

  $('results').innerHTML = list.length
    ? list.map(a => cardHTML(a)).join('')
    : emptyStateHTML();
}

/* ---------- saved tab ---------- */

function updateSavedCount() {
  const el = $('saved-count');
  el.hidden = favourites.length === 0;
  el.textContent = favourites.length;
}

function renderSaved() {
  const byId = Object.fromEntries(activities.map(a => [a.id, a]));
  const items = favourites.map(id => byId[id]).filter(Boolean);
  $('saved-empty').hidden = items.length > 0;
  $('saved-empty').textContent = items.length
    ? ''
    : 'No favourites yet — tap the heart on any activity to save it here.';
  $('saved-list').innerHTML = items.map(a => cardHTML(a, { alwaysPlan: true })).join('');
  updateSavedCount();
}

function toggleFav(id) {
  const i = favourites.indexOf(id);
  if (i >= 0) favourites.splice(i, 1);
  else favourites.push(id);
  saveFavs();
  renderResults();
  renderSaved();
}

/* ---------- plan tab ---------- */

function planBlocks() {
  return holidayPeriods(holidays);
}

function defaultPlanBlock() {
  const blocks = planBlocks();
  if (!blocks.length) return;
  const t = startOfDay(new Date());
  let idx = blocks.findIndex(p => startOfDay(parseDay(p.start)) > t);
  if (idx < 0) idx = blocks.length - 1; // all past: show the most recent
  const cur = blocks.findIndex(p => {
    const s = startOfDay(parseDay(p.start)), e = startOfDay(parseDay(p.end));
    return t >= s && t <= e;
  });
  planBlockIdx = cur >= 0 ? cur : idx;
}

function renderPlan() {
  const blocks = planBlocks();
  const sel = $('plan-block-select');
  const noHol = $('plan-noholidays');

  if (!blocks.length) {
    sel.innerHTML = '';
    noHol.hidden = false;
    noHol.textContent = holidays === null
      ? 'School holiday dates couldn’t be loaded. Your saved plan items are still listed below.'
      : 'No school holiday dates are listed in the data file yet.';
    renderPlanItemsOnly();
    return;
  }
  noHol.hidden = true;
  sel.innerHTML = blocks.map((p, i) =>
    '<option value="' + i + '"' + (i === planBlockIdx ? ' selected' : '') + '>' +
    esc(p.name) + ' (' + esc(fmtDay(parseDay(p.start))) + ' – ' + esc(fmtDay(parseDay(p.end))) + ')</option>'
  ).join('');

  const block = blocks[planBlockIdx];
  const byId = Object.fromEntries(activities.map(a => [a.id, a]));
  const days = blockDays(block).map(date => {
    const iso = isoDay(date);
    const items = plan.filter(e => e.date === iso).map(e => byId[e.id]).filter(Boolean);
    return { date, iso, items };
  });

  $('plan-days').innerHTML = days.map(d => {
    const items = d.items.length
      ? '<ul class="plan-items">' + d.items.map(a =>
        '<li><span>' + esc(a.name) + ' <span class="muted">· ' + esc(priceLabel(a)) + '</span></span>' +
        '<button type="button" class="plan-remove" data-action="remove-plan" data-id="' + esc(a.id) +
        '" data-date="' + d.iso + '" aria-label="Remove ' + esc(a.name) + ' from ' + esc(fmtDay(d.date)) + '">✕</button></li>'
      ).join('') + '</ul>'
      : '<p class="plan-nothing">Nothing planned yet</p>';
    return '<div class="plan-day"><div class="plan-day-head"><h3>' + esc(fmtDay(d.date)) +
      '</h3><span class="date-sub">' + esc(fmtDayYear(d.date)) + '</span></div>' + items + '</div>';
  }).join('');
}

function renderPlanItemsOnly() {
  // Fallback when no holiday blocks exist: list raw plan items by date.
  const byId = Object.fromEntries(activities.map(a => [a.id, a]));
  const sorted = plan.slice().sort((x, y) => (x.date < y.date ? -1 : 1));
  if (!sorted.length) {
    $('plan-days').innerHTML = '<p class="plan-nothing">Nothing planned yet.</p>';
    return;
  }
  $('plan-days').innerHTML = sorted.map(e => {
    const a = byId[e.id];
    const d = parseDay(e.date);
    return '<div class="plan-day"><div class="plan-day-head"><h3>' + esc(d ? fmtDay(d) : e.date) + '</h3></div>' +
      '<ul class="plan-items"><li><span>' + esc(a ? a.name : 'Unavailable listing') + '</span>' +
      '<button type="button" class="plan-remove" data-action="remove-plan" data-id="' + esc(e.id) +
      '" data-date="' + esc(e.date) + '" aria-label="Remove from plan">✕</button></li></ul></div>';
  }).join('');
}

function addToPlan(id, date) {
  if (!plan.some(e => e.id === id && e.date === date)) {
    plan.push({ id, date });
    savePlan();
  }
  renderPlan();
  if (currentTab === 'saved') renderSaved();
}

/* ---------- settings ---------- */

function buildInterestCheckboxes() {
  for (const kid of ['c1', 'c2']) {
    const box = $(kid + '-interests');
    box.innerHTML = INTERESTS.map(([val, label]) =>
      '<label><input type="checkbox" value="' + val + '"> ' + esc(label) + '</label>'
    ).join('');
  }
}

function fillSettingsForm() {
  $('c1-name').value = settings.child1.name;
  $('c2-name').value = settings.child2.name;
  $('settings-postcode').value = settings.postcode;
  for (const [kid, child] of [['c1', settings.child1], ['c2', settings.child2]]) {
    $(kid + '-interests').querySelectorAll('input').forEach(cb => {
      cb.checked = child.interests.includes(cb.value);
    });
  }
  $('settings-error').hidden = true;
  $('settings-warn').hidden = true;
}

function readInterests(kid) {
  return Array.from($(kid + '-interests').querySelectorAll('input:checked')).map(cb => cb.value);
}

function saveSettingsForm() {
  const err = $('settings-error'), warn = $('settings-warn');
  err.hidden = true; warn.hidden = true;

  const pc = $('settings-postcode').value.trim();
  if (pc && !/^\d{4}$/.test(pc)) {
    err.textContent = 'Postcode must be exactly 4 digits.';
    err.hidden = false;
    return;
  }

  const c1Name = $('c1-name').value.trim();
  const c2Name = $('c2-name').value.trim();
  if (!c1Name || !c2Name) {
    err.textContent = 'Both children need a name.';
    err.hidden = false;
    return;
  }

  settings.child1.name = c1Name.slice(0, 24);
  settings.child2.name = c2Name.slice(0, 24);
  settings.child1.interests = readInterests('c1');
  settings.child2.interests = readInterests('c2');
  settings.postcode = pc;

  if (pc && (pc < '4000' || pc > '4999')) {
    warn.textContent = 'That postcode is outside Queensland coverage (4000–4999) — saved anyway.';
    warn.hidden = false;
  }

  saveSettings();
  resolvePostcode();
  renderPostcodeNote();
  renderResults();
  $('settings-dialog').close();
  toast('Settings saved');
}

function resetSettings() {
  settings = JSON.parse(JSON.stringify(DEFAULT_SETTINGS));
  saveSettings();
  fillSettingsForm();
  resolvePostcode();
  renderPostcodeNote();
  renderResults();
  toast('Settings reset to defaults');
}
/* ---------- plan date dialog ---------- */

function openPlanDate(id) {
  const a = activities.find(x => x.id === id);
  if (!a) return;
  plandateActivityId = id;
  $('plandate-activity').textContent = a.name;
  const input = $('plandate-input');
  const blocks = planBlocks();
  if (blocks.length) {
    const block = blocks[planBlockIdx];
    input.min = block.start;
    input.max = block.end;
    input.value = block.start;
  } else {
    input.removeAttribute('min');
    input.removeAttribute('max');
    input.value = isoDay(new Date());
  }
  $('plandate-error').hidden = true;
  const dlg = $('plandate-dialog');
  if (typeof dlg.showModal === 'function') dlg.showModal();
}

function savePlanDate() {
  const err = $('plandate-error');
  err.hidden = true;
  const date = $('plandate-input').value;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !parseDay(date)) {
    err.textContent = 'Pick a valid date.';
    err.hidden = false;
    return;
  }
  addToPlan(plandateActivityId, date);
  $('plandate-dialog').close();
  toast('Added to your plan');
}

/* ---------- sharing ---------- */

async function copyText(str, okMsg) {
  try {
    await navigator.clipboard.writeText(str);
  } catch (e) {
    const ta = document.createElement('textarea');
    ta.value = str;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); } catch (e2) { /* give up silently */ }
    document.body.removeChild(ta);
  }
  toast(okMsg);
}

function shareLink() {
  const base = /^https?:$/.test(location.protocol) ? location.origin + location.pathname : location.href.split('#')[0];
  const url = base + '#plan=' + encodePlan(plan);
  copyText(url, plan.length ? 'Share link copied' : 'Share link copied (plan is empty)');
}

function shareText() {
  const blocks = planBlocks();
  let text;
  if (blocks.length) {
    const block = blocks[planBlockIdx];
    const byId = Object.fromEntries(activities.map(a => [a.id, a]));
    const days = blockDays(block).map(date => {
      const iso = isoDay(date);
      const items = plan.filter(e => e.date === iso).map(e => byId[e.id]).filter(Boolean);
      return { date, items };
    });
    text = planText(block.name, parseDay(block.start), parseDay(block.end), days);
  } else {
    text = 'The Queensland Adventure — holiday plan\n\n' +
      (plan.length ? plan.map(e => '• ' + e.date).join('\n') : 'Nothing planned yet.');
  }
  copyText(text, 'Itinerary copied as text');
}

function checkSharedPlan() {
  const h = location.hash || '';
  if (!h.startsWith('#plan=')) return;
  const box = $('plan-import');
  let decoded = null;
  try { decoded = decodePlan(h.slice(6)); } catch (e) { /* fall through */ }
  if (!decoded || !decoded.length) {
    box.hidden = false;
    box.innerHTML = 'That plan link didn’t contain anything usable. <button type="button" class="link-btn" data-action="dismiss-plan">Dismiss</button>';
    return;
  }
  box.hidden = false;
  box.dataset.sharedPlan = JSON.stringify(decoded);
  box.innerHTML = 'This link has a holiday plan (' + decoded.length +
    (decoded.length === 1 ? ' activity' : ' activities') + '). ' +
    '<button type="button" class="btn btn-small" data-action="load-plan">Load plan</button> ' +
    '<button type="button" class="link-btn" data-action="dismiss-plan">Keep mine</button>';
  history.replaceState(null, '', location.pathname + location.search);
}

function loadSharedPlan() {
  const box = $('plan-import');
  try {
    plan = JSON.parse(box.dataset.sharedPlan || '[]');
  } catch (e) { plan = []; }
  savePlan();
  box.hidden = true;
  box.innerHTML = '';
  defaultPlanBlock();
  renderPlan();
  switchTab('plan');
  toast('Plan loaded');
}

/* ---------- tabs & toast ---------- */

function switchTab(name) {
  currentTab = name;
  for (const t of document.querySelectorAll('.tab')) {
    const active = t.dataset.tab === name;
    t.classList.toggle('is-active', active);
    if (active) t.setAttribute('aria-current', 'page');
    else t.removeAttribute('aria-current');
  }
  $('view-find').hidden = name !== 'find';
  $('view-saved').hidden = name !== 'saved';
  $('view-plan').hidden = name !== 'plan';
  window.scrollTo(0, 0);
  setStickTop();
}

function toast(msg) {
  const el = $('toast');
  el.textContent = msg;
  el.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.hidden = true; }, 2600);
}

/* ---------- events ---------- */

function bindUI() {
  // Tabs
  document.querySelectorAll('.tab').forEach(t =>
    t.addEventListener('click', () => switchTab(t.dataset.tab)));

  // Search (debounced)
  $('search-input').addEventListener('input', e => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {
      filters.q = e.target.value;
      renderResults();
    }, 120);
  });

  // Postcode in filter bar: apply on change
  $('postcode-input').addEventListener('change', e => {
    const v = e.target.value.trim();
    if (v && !/^\d{4}$/.test(v)) {
      toast('Postcode must be 4 digits');
      e.target.value = settings.postcode || '';
      return;
    }
    settings.postcode = v;
    saveSettings();
    resolvePostcode();
    if (!v) { filters.bucket = 'any'; $('travel-select').value = 'any'; }
    renderPostcodeNote();
    renderResults();
  });

  $('travel-select').addEventListener('change', e => {
    filters.bucket = e.target.value;
    renderPostcodeNote();
    renderResults();
  });

  $('sort-select').addEventListener('change', e => {
    filters.sort = e.target.value;
    renderResults();
  });

  // Banner holidays chip
  $('holidays-chip').addEventListener('click', () => {
    filters.forHolidays = !filters.forHolidays;
    $('holidays-chip').setAttribute('aria-pressed', filters.forHolidays ? 'true' : 'false');
    renderResults();
    if (filters.forHolidays) toast('Holiday programs first');
  });

  // Settings
  $('settings-btn').addEventListener('click', () => {
    fillSettingsForm();
    const dlg = $('settings-dialog');
    if (typeof dlg.showModal === 'function') dlg.showModal();
  });
  $('settings-close').addEventListener('click', () => $('settings-dialog').close());
  $('settings-reset').addEventListener('click', resetSettings);
  $('settings-form').addEventListener('submit', e => {
    e.preventDefault();
    saveSettingsForm();
  });

  // Plan date dialog
  $('plandate-cancel').addEventListener('click', () => $('plandate-dialog').close());
  $('plandate-form').addEventListener('submit', e => {
    e.preventDefault();
    savePlanDate();
  });

  // Plan tab
  $('plan-block-select').addEventListener('change', e => {
    planBlockIdx = parseInt(e.target.value, 10) || 0;
    renderPlan();
  });
  $('copy-link-btn').addEventListener('click', shareLink);
  $('copy-text-btn').addEventListener('click', shareText);

  // Delegated actions (cards, empty states, notices)
  document.addEventListener('click', e => {
    const el = e.target.closest('[data-action]');
    if (!el) return;
    const action = el.dataset.action;
    if (action === 'toggle-fav') toggleFav(el.dataset.id);
    else if (action === 'open-plan-date') openPlanDate(el.dataset.id);
    else if (action === 'open-settings') { fillSettingsForm(); const dlg = $('settings-dialog'); if (typeof dlg.showModal === 'function') dlg.showModal(); }
    else if (action === 'set-category') {
      filters.category = el.dataset.category;
      renderCategoryChips();
      renderResults();
    }
    else if (action === 'toggle-free') {
      filters.freeOnly = !filters.freeOnly;
      renderCategoryChips();
      renderResults();
    }
    else if (action === 'set-bucket') {
      filters.bucket = el.dataset.bucket;
      $('travel-select').value = filters.bucket;
      renderPostcodeNote();
      renderResults();
    }
    else if (action === 'reset-filters') {
      filters = { category: '', freeOnly: false, q: '', bucket: 'any', sort: 'suggested', forHolidays: filters.forHolidays };
      $('search-input').value = '';
      $('travel-select').value = 'any';
      $('sort-select').value = 'suggested';
      renderCategoryChips();
      renderResults();
    }
    else if (action === 'remove-plan') {
      plan = plan.filter(p => !(p.id === el.dataset.id && p.date === el.dataset.date));
      savePlan();
      renderPlan();
    }
    else if (action === 'load-plan') loadSharedPlan();
    else if (action === 'dismiss-plan') {
      const box = $('plan-import');
      box.hidden = true;
      box.innerHTML = '';
    }
    else if (action === 'retry-load') {
      loadAll().then(() => {
        resolvePostcode();
        defaultPlanBlock();
        renderAll();
        checkSharedPlan();
      });
    }
  });
}

// Boot only in a browser (node test harness requires this file without a DOM).
if (typeof document !== 'undefined' && typeof window !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
}

})();

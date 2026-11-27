# CLAUDE.md — fathomm.org

Static site for **fathomm.org**. No build step, no framework. The host serves every file
as-is.

`README.md` covers the file layout, the local preview, the deploy step, and how to
regenerate the clinic data. This file covers only the design system and the conventions to
hold to when you edit the site.

## Design system

Gold and navy luxury theme, applied site-wide:

- Background: deep navy `#0a1628` (radial `#0d2847→#0a1628→#060e1a`). Gold accent `#c9a84c`
  (light `#e0c872`). Cyan micro-labels `#0ef5e3`. Text `#f0f0f0`, muted
  `rgba(240,240,240,.6)`.
- Typeface: **Cormorant Garamond** (serif display and headings) with **Inter** (body and
  labels), both from Google Fonts. Logotype: the `FATHOMM` wordmark, serif, gold,
  letter-spaced, uppercase.
- Nav (minimal, sitewide): brand `FATHOMM` (→ `/`) · **Clinics** (`/atlas`) · **Voyages**
  (`/voyage`) · **Join Waitlist** (gold-outline CTA).
- The atlas keeps its light-theme CSS. A `GOLD / NAVY LUXURY RESKIN` override block at the
  end of its `<style>` repaints it. Grade colors A–E stay as they are, and the map uses
  CARTO `dark_all` tiles.

## Pages

- `/` — the FATHOMM pitch narrative: problem, solution, experience, science pipeline, tiers,
  legal framework, market and why-now, team, vision, waitlist. The confidential deck
  financials (the ask, the projections, the unit economics) stay off this page on purpose.
- `/voyage` — the full luxury 24-hour medical-voyage experience: timeline, tiers,
  membership, FAQ.
- `/atlas` — the medical-tourism atlas (full parallax map) plus the **searchable directory**
  (`#directory`): 311 clinics in 35 countries — Fathomm's trust-scored entries plus listed
  hospitals compiled from accreditation directories — with region/search filters, a credited
  **Data & sources** block, and a **Submit a clinic** CTA.
- `/submit` — clinic-submission form → **Netlify Forms** (`clinic-submission`), honeypot spam
  protection, AJAX with a `/thank-you` (`thank-you.html`) no-JS fallback. Submissions are a
  moderation queue, not auto-published.

## Clinic directory data
`data/directory.json` is built by merging the curated `data/clinics.json` (trust-scored) with
`data/directory_sources.psv` (listed hospitals), de-duplicated, then inlined into `/atlas`:
```
python3 tools/build_directory.py     # -> data/directory.json
python3 tools/inject_directory.py    # inlines it into atlas/index.html (#directory)
```
Keep the directory data inlined (no runtime fetch), same as the map. Netlify Forms needs
**Forms → Enable form detection** turned on in the Netlify dashboard (one-time), then a redeploy.

## Waitlist

`index.html` carries a `#waitlist` form. Paste your form endpoint into the
`WAITLIST_ENDPOINT` constant in the page's `<script>`, from Formspree, Tally, or a Google
Form POST URL. Until you set it, the form runs its confirmation animation and sends nowhere.

## Conventions

- Keep it dependency-light. Only Leaflet (cdnjs), Google Fonts, and CARTO tiles load at
  runtime.
- The atlas page and the embeddable widget stay self-contained: the clinic data is inlined,
  so neither fetches at runtime. Keep it that way.
- Trust Score = evidence 30 · accreditation 25 · transparency 15 · track record 15 ·
  safety 15. It is a decision aid, not medical advice. Keep the experimental and discredited
  labels intact.
- Commit the regenerated `data/*` and both HTML files together, never one without the other.

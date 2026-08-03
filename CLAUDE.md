# CLAUDE.md — fathomm.org

Static site for **fathomm.org**. **No build step, no framework.** Every file is served as-is.

## Design system
Gold / navy luxury theme, applied site-wide:
- Background: deep navy `#0a1628` (radial `#0d2847→#0a1628→#060e1a`); gold accent `#c9a84c` (light `#e0c872`); cyan micro-labels `#0ef5e3`; text `#f0f0f0`, muted `rgba(240,240,240,.6)`.
- Typeface: **Cormorant Garamond** (serif display/headings) + **Inter** (body/labels), Google Fonts. Logotype: `FATHOMM` wordmark (serif, gold, letter-spaced, uppercase).
- Nav: brand `FATHOMM` (→ `/`) · **Global Clinics** (`/atlas`) · **Ocean Voyages** (`/ocean`) · **Join Waitlist** (gold-outline CTA). The homepage nav also lists its in-page sections (Vision, Experience, Treatments, Science, Membership, FAQ).
- The atlas keeps its light-theme CSS but is repainted by a `GOLD / NAVY LUXURY RESKIN` override block at the end of its `<style>` (grade colors A–E kept; map uses CARTO `dark_all` tiles).

## Layout
- `index.html` — homepage: FATHOMM luxury 24-hour medical voyages from San Francisco (gene therapy + peptides) — vision, experience, treatment tiers, science, membership, FAQ, waitlist → `/`.
- `ocean/index.html` — Ocean Voyages: the "Dive deeper" recovery-at-sea landing → `/ocean`.
- `atlas/index.html` — Global Clinics: the trust-scored atlas (full parallax page) → `/atlas`.

## Waitlist
`index.html` has a `#waitlist` form. Paste your form endpoint into the `WAITLIST_ENDPOINT`
constant in the page's `<script>` (Formspree / Tally / Google Form POST URL). Until it is set,
the form runs its confirmation animation without sending anywhere.
- `embeds/fathomm-map.html` — embeddable map widget (iframe) → `/embeds/fathomm-map.html`.
- `data/clinics.json` / `clinics.csv` — clinic dataset (115 providers, 20 countries, trust-scored 0–100).
- `tools/build_data.py` — regenerates `data/clinics.{json,csv}` from source.
- `tools/inject.py` — injects `data/clinics.json` into the two HTML files (from `tools/*_template.html`).
- `CNAME` (`fathomm.org`), `.nojekyll` — GitHub Pages custom domain + path serving.

The atlas page and widget are **self-contained**: clinic data is inlined, no runtime fetch.

## Deploy
Push to `origin/main` (GitHub Pages serves it). Live URLs:
`https://fathomm.org/atlas` and `https://fathomm.org/embeds/fathomm-map.html`.

## Update clinic data
```
python3 tools/build_data.py    # rewrites data/clinics.json + .csv
python3 tools/inject.py        # rebuilds atlas/index.html + embeds/fathomm-map.html
```
Commit the regenerated `data/*` and both HTML files together.

## Conventions
- Keep it dependency-light: only Leaflet (cdnjs), Google Fonts, and CARTO tiles load at runtime.
- Trust Score = evidence 30 · accreditation 25 · transparency 15 · track record 15 · safety 15.
  It is a decision aid, not medical advice; keep experimental/discredited labels intact.

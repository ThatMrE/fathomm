# CLAUDE.md — fathomm.org

Static site for **fathomm.org**. **No build step, no framework.** Every file is served as-is.

## Layout
- `index.html` — landing placeholder (leave unchanged unless asked).
- `atlas/index.html` — the Medical-Tourism Atlas (full parallax page) → `/atlas`.
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

# Fathomm

The Fathomm website (fathomm.org). A plain static site. Deploying it needs no build step.

## Structure

```
index.html                 Homepage — the FATHOMM pitch narrative                    →  fathomm.org/
voyage/index.html          Voyages — the luxury 24-hour medical-voyage experience    →  fathomm.org/voyage
atlas/index.html           Clinics — atlas map + searchable 311-clinic directory     →  fathomm.org/atlas
submit/index.html          Submit a clinic — Netlify Forms submission page           →  fathomm.org/submit
thank-you.html             Submission confirmation (form no-JS fallback)             →  fathomm.org/thank-you
embeds/fathomm-map.html    Embeddable map widget (iframe-ready)                     →  fathomm.org/embeds/fathomm-map.html
data/clinics.json          Curated clinic dataset (coordinates, pricing, trust scores)
data/clinics.csv           Same data, spreadsheet form
data/directory.json        Full directory = clinics.json + directory_sources.psv (merged)
data/directory_sources.psv Listed hospitals (name|city|country|region|specialty|website|accreditation)
tools/build_data.py        Regenerates data/clinics.{json,csv} from source
tools/inject.py            Injects data/clinics.json into the atlas + widget
tools/build_directory.py   Builds data/directory.json (merge + dedup)
tools/inject_directory.py  Inlines data/directory.json into atlas/index.html (#directory)
tools/*_template.html      Templates (contain a data placeholder) used by the inject scripts
CNAME                      Custom domain. .nojekyll serves folders/paths as-is.
.nojekyll                  Serve folders/paths as-is
```

## Hosting & submissions

The site is hosted on **Netlify** (project `fathomm`, git-connected to `main` — every push
deploys). Clinic submissions on `/submit` use **Netlify Forms** (`clinic-submission`). To
activate: Netlify dashboard → **Forms → Enable form detection**, then redeploy. Submissions
appear in the Forms tab (and email, if a notification is configured); they are a moderation
queue — approve, then add to `data/directory_sources.psv` and rebuild.

The atlas page and the widget are **fully self-contained**. The clinic data is inlined, so
each file works on its own with no server code and no data fetch.

## View locally

```bash
python3 -m http.server 8000
# then open:
#   http://localhost:8000/atlas/
#   http://localhost:8000/embeds/fathomm-map.html
```

## Embed the map on another page

```html
<div style="position:relative;width:100%;max-width:1200px;margin:0 auto;
            height:min(80vh,760px);min-height:560px;">
  <iframe src="https://fathomm.org/embeds/fathomm-map.html"
    title="Fathomm Medical-Tourism Trust Map" loading="lazy"
    style="position:absolute;inset:0;width:100%;height:100%;border:0;border-radius:16px;"
    allowfullscreen></iframe>
</div>
```

## Update the clinic data

```bash
# 1. edit the C(...) entries in tools/build_data.py
#    (last five numbers per clinic = pillar scores:
#     evidence /30, accreditation /25, transparency /15, track record /15, safety /15)
python3 tools/build_data.py     # regenerates data/clinics.json + data/clinics.csv
python3 tools/inject.py         # rebuilds atlas/index.html + embeds/fathomm-map.html
```

Commit the regenerated `data/*` and the two HTML files together.

## Runtime dependencies (CDN)

Both HTML files load Leaflet (cdnjs), Google Fonts, and CARTO map tiles at runtime.
If you add a strict Content-Security-Policy, allow-list those origins or self-host them.
The four `<link>` and `<script>` src lines at the top of each file are the only ones to
repoint.

## Trust Score

Composite 0–100 estimate per provider: evidence 30 · accreditation 25 · transparency 15 ·
track record 15 · safety 15. A decision aid, **not** an endorsement or medical advice.
The experimental categories (exosomes, stem-cell, most "life-extension", gene therapy) carry
a not-FDA/EMA-approved label. Discredited entries appear only as cautionary items.

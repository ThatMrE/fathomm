# Fathomm

The Fathomm website (fathomm.org). Plain static site — no build step required to deploy.

## Structure

```
index.html                 Landing placeholder (unchanged)
atlas/index.html           The Medical-Tourism Atlas — full parallax experience  →  fathomm.org/atlas
embeds/fathomm-map.html    Embeddable map widget (iframe-ready)                    →  fathomm.org/embeds/fathomm-map.html
data/clinics.json          Clinic dataset (coordinates, links, pricing, trust scores)
data/clinics.csv           Same data, spreadsheet form
tools/build_data.py        Regenerates data/clinics.{json,csv} from source
tools/inject.py            Injects data/clinics.json into the two HTML files
tools/*_template.html      Templates (contain a data placeholder) used by inject.py
CNAME                      Custom domain (GitHub Pages). Safe to delete on other hosts.
.nojekyll                  Serve folders/paths as-is (GitHub Pages)
```

The atlas page and the widget are **fully self-contained** — the clinic data is inlined, so
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
If a strict Content-Security-Policy is added, allow-list those origins or self-host them
(the four `<link>`/`<script>` src lines at the top of each file are the only ones to repoint).

## Trust Score

Composite 0–100 estimate per provider — evidence 30 · accreditation 25 · transparency 15 ·
track record 15 · safety 15. A decision aid, **not** an endorsement or medical advice.
Experimental categories (exosomes, stem-cell, most "life-extension", gene therapy) are labeled
not FDA/EMA-approved; discredited entries appear only as cautionary items.

#!/usr/bin/env python3
"""Build data/directory.json = curated (trust-scored) clinics from data/clinics.json
merged with listed clinics from data/directory_sources.psv (deduped).
Run: python3 tools/build_directory.py   then   python3 tools/inject_directory.py
"""
import json, re, os
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REGION = {
  'Thailand':'Asia','India':'Asia','Malaysia':'Asia','Singapore':'Asia','South Korea':'Asia','Korea':'Asia',
  'Taiwan':'Asia','Philippines':'Asia','Indonesia':'Asia','Japan':'Asia','China':'Asia','Vietnam':'Asia',
  'Mexico':'Latin America','Costa Rica':'Latin America','Colombia':'Latin America','Brazil':'Latin America',
  'Panama':'Latin America','Argentina':'Latin America','Dominican Republic':'Latin America',
  'Cayman Islands':'Latin America','Honduras':'Latin America',
  'Turkey':'Europe','Turkiye':'Europe','Hungary':'Europe','Poland':'Europe','Spain':'Europe','Czechia':'Europe',
  'Czech Republic':'Europe','Lithuania':'Europe','Germany':'Europe','Greece':'Europe','Switzerland':'Europe',
  'United Kingdom':'Europe','UK':'Europe','Belgium':'Europe','Italy':'Europe','France':'Europe','Netherlands':'Europe',
  'Georgia':'Europe','Monaco':'Europe',
  'UAE':'Middle East','United Arab Emirates':'Middle East','Jordan':'Middle East','Israel':'Middle East',
  'Saudi Arabia':'Middle East','Qatar':'Middle East','Lebanon':'Middle East','Egypt':'Middle East',
  'USA':'North America','United States':'North America','Canada':'North America','South Africa':'Africa',
}

def norm_name(n):
    n = re.sub(r'\(.*?\)', '', n.lower())
    return re.sub(r'[^a-z0-9]+', ' ', n).strip()

def domain(u):
    if not u or u == 'unknown': return ''
    try:
        d = urlparse(u if '://' in u else 'http://' + u).netloc.lower()
        return d[4:] if d.startswith('www.') else d
    except Exception:
        return ''

raw = json.load(open(f"{ROOT}/data/clinics.json"))
cur = raw if isinstance(raw, list) else (raw.get('clinics') or next(v for v in raw.values() if isinstance(v, list)))
out, seen_names, seen_domains = [], set(), set()
for c in cur:
    country = c.get('country', '')
    region = REGION.get(country, 'Other')
    out.append({'name': c['name'], 'city': c.get('city',''), 'country': country, 'region': region,
                'specialty': c.get('specialty') or c.get('category',''), 'website': c.get('website','') or '',
                'accreditation': c.get('accreditations','') or '', 'status': 'scored',
                'trust_score': c.get('trust_score'), 'tier': c.get('tier'),
                'lat': c.get('lat'), 'lng': c.get('lng'), 'defunct': bool(c.get('defunct'))})
    seen_names.add(norm_name(c['name']))
    d = domain(c.get('website',''));
    if d: seen_domains.add(d)

added = skipped = 0
with open(f"{ROOT}/data/directory_sources.psv", encoding='utf-8') as f:
    next(f)
    for line in f:
        line = line.strip()
        if not line: continue
        p = [x.strip() for x in line.split('|')]
        if len(p) != 7: continue
        name, city, country, region, specialty, website, accr = p
        nn, dm = norm_name(name), domain(website)
        if nn in seen_names or (dm and dm in seen_domains):
            skipped += 1; continue
        seen_names.add(nn);
        if dm: seen_domains.add(dm)
        out.append({'name': name, 'city': city, 'country': country, 'region': region, 'specialty': specialty,
                    'website': '' if website == 'unknown' else website, 'accreditation': '' if accr == 'unknown' else accr,
                    'status': 'listed', 'trust_score': None, 'tier': None, 'lat': None, 'lng': None, 'defunct': False})
        added += 1

out.sort(key=lambda x: (0 if x['status']=='scored' else 1,
                        -(x['trust_score'] or 0) if x['status']=='scored' else 0, x['country'], x['name']))
json.dump(out, open(f"{ROOT}/data/directory.json", 'w'), ensure_ascii=False, indent=0)
print(f"scored={len(cur)} listed_added={added} dupes_skipped={skipped} TOTAL={len(out)}")

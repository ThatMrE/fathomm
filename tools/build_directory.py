#!/usr/bin/env python3
"""Build data/directory.json = curated (trust-scored) clinics from data/clinics.json
merged with listed clinics from data/directory_sources.psv (deduped).
Run: python3 tools/build_directory.py   then   python3 tools/inject_directory.py
"""
import json, re, os, math
from urllib.parse import urlparse

# Approximate city centroids for listed clinics whose city is not in the curated set.
# Used only to place directory pins at city level (listed entries are not precision-geocoded).
CENTROIDS = {
 ('Abu Dhabi','UAE'):(24.4539,54.3773),('Alicante','Spain'):(38.3452,-0.4810),('Amman','Jordan'):(31.9454,35.9284),
 ('Athens','Greece'):(37.9838,23.7275),('Bangalore','India'):(12.9716,77.5946),('Barcelona','Spain'):(41.3874,2.1686),
 ('Berlin','Germany'):(52.5200,13.4050),('Bogota','Colombia'):(4.7110,-74.0721),('Budapest','Hungary'):(47.4979,19.0402),
 ('Buenos Aires','Argentina'):(-34.6037,-58.3816),('Bursa','Turkiye'):(40.1826,29.0665),('Cali','Colombia'):(3.4516,-76.5320),
 ('Chennai','India'):(13.0827,80.2707),('Gurugram','India'):(28.4595,77.0266),('Haifa','Israel'):(32.7940,34.9896),
 ('Hamburg','Germany'):(53.5511,9.9937),('Heidelberg','Germany'):(49.3988,8.6724),('Irbid','Jordan'):(32.5556,35.8500),
 ('Istanbul','Turkiye'):(41.0082,28.9784),('Jeddah','Saudi Arabia'):(21.4858,39.1925),('Jerusalem','Israel'):(31.7683,35.2137),
 ('Kaunas','Lithuania'):(54.8985,23.9036),('Kocaeli','Turkiye'):(40.7654,29.9408),('Kochi','India'):(9.9312,76.2673),
 ('Krakow','Poland'):(50.0647,19.9450),('Makati','Philippines'):(14.5547,121.0244),('Medellin','Colombia'):(6.2442,-75.5812),
 ('Melaka','Malaysia'):(2.1896,102.2501),('Mexico City','Mexico'):(19.4326,-99.1332),('Monterrey','Mexico'):(25.6866,-100.3161),
 ('Mumbai','India'):(19.0760,72.8777),('Munich','Germany'):(48.1351,11.5820),('Muntinlupa','Philippines'):(14.3832,121.0409),
 ('New Delhi','India'):(28.6139,77.2090),('Pamplona','Spain'):(42.8125,-1.6458),('Pasig','Philippines'):(14.5764,121.0851),
 ('Pattaya','Thailand'):(12.9236,100.8825),('Penang','Malaysia'):(5.4164,100.3327),('Petah Tikva','Israel'):(32.0870,34.8882),
 ('Petaling Jaya','Malaysia'):(3.1073,101.6067),('Porto Alegre','Brazil'):(-30.0346,-51.2177),('Prague','Czechia'):(50.0755,14.4378),
 ('Puerto Vallarta','Mexico'):(20.6534,-105.2253),('Ramat Gan','Israel'):(32.0684,34.8248),('Riyadh','Saudi Arabia'):(24.7136,46.6753),
 ('San Jose','Costa Rica'):(9.9281,-84.0907),('San Juan','Philippines'):(14.6019,121.0355),('Sao Paulo','Brazil'):(-23.5505,-46.6333),
 ('Seongnam','South Korea'):(37.4201,127.1267),('Singapore','Singapore'):(1.3521,103.8198),('Subang Jaya','Malaysia'):(3.0567,101.5851),
 ('Taichung','Taiwan'):(24.1477,120.6736),('Taipei','Taiwan'):(25.0330,121.5654),('Tangerang','Indonesia'):(-6.1783,106.6319),
 ('Taoyuan','Taiwan'):(24.9936,121.3010),('Tel Aviv','Israel'):(32.0853,34.7818),('Thessaloniki','Greece'):(40.6401,22.9444),
 ('Valencia','Spain'):(39.4699,-0.3763),('Vellore','India'):(12.9165,79.1325),('Vilnius','Lithuania'):(54.6872,25.2797),
 ('Warsaw','Poland'):(52.2297,21.0122),
}

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

# --- Geocode listed entries at city level (curated city match first, then CENTROIDS) ---
# Build city->coord from scored entries that already have coordinates.
cur_coord = {}
for c in out:
    if c['status'] == 'scored' and c.get('lat') is not None and c.get('lng') is not None:
        cur_coord.setdefault((c['city'].strip().lower(), c['country'].strip().lower()), (c['lat'], c['lng']))
        cur_coord.setdefault((c['city'].strip().lower(),), (c['lat'], c['lng']))  # city-only fallback

def base_coord(city, country):
    key = (city.strip().lower(), country.strip().lower())
    if key in cur_coord: return cur_coord[key]
    if (city, country) in CENTROIDS: return CENTROIDS[(city, country)]
    ck = (city.strip().lower(),)
    if ck in cur_coord: return cur_coord[ck]
    return None

geo = ungeo = 0
city_idx = {}
for c in out:
    if c['status'] != 'listed': continue
    base = base_coord(c['city'], c['country'])
    if not base:
        ungeo += 1; continue
    k = (c['city'].strip().lower(), c['country'].strip().lower())
    i = city_idx.get(k, 0); city_idx[k] = i + 1
    # deterministic sunflower jitter so co-located pins fan out (first pin sits on centre)
    r = 0.012 * math.sqrt(i)
    a = i * 2.399963229728653  # golden angle (rad)
    lat = round(base[0] + r * math.cos(a), 5)
    lng = round(base[1] + (r * math.sin(a)) / max(0.2, math.cos(math.radians(base[0]))), 5)
    c['lat'], c['lng'] = lat, lng
    geo += 1

out.sort(key=lambda x: (0 if x['status']=='scored' else 1,
                        -(x['trust_score'] or 0) if x['status']=='scored' else 0, x['country'], x['name']))
json.dump(out, open(f"{ROOT}/data/directory.json", 'w'), ensure_ascii=False, indent=0)
print(f"scored={len(cur)} listed_added={added} dupes_skipped={skipped} TOTAL={len(out)} geocoded_listed={geo} ungeocoded_listed={ungeo}")

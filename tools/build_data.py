#!/usr/bin/env python3
"""
Fathomm Medical-Tourism Atlas — master data builder.
Encodes the Fathomm Trust Score rubric and every researched provider,
then emits clinics.json + clinics.csv for the map, report, and web experience.

FATHOMM TRUST SCORE (0-100), five weighted pillars:
  evidence  (0-30): scientific evidence base of the PROCEDURE itself
  accred    (0-25): accreditation, licensing, practitioner board-certification, GMP labs
  transp    (0-15): named/verifiable practitioners, published pricing, honest disclaimers
  track     (0-15): years operating, patient volume, verifiable reviews
  safety    (0-15): regulatory recourse, safety record, absence of FDA/gov warnings or bans

Tiers:
  A 80-100  Verified · Well-Established
  B 65-79   Reputable · Do Your Diligence
  C 50-64   Proceed With Caution
  D 35-49   High Risk · Experimental
  E 0-34    Discredited / Avoid
"""
import json, csv, os, math

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

CITY = {
    "Tijuana": (32.5283, -117.0187), "Los Algodones": (32.7186, -114.7300),
    "Cancun": (21.1060, -86.7700), "Mexicali": (32.6245, -115.4523),
    "Playas de Rosarito": (32.3617, -117.0568), "San Luis Rio Colorado": (32.4539, -114.7722),
    "Bangkok": (13.7563, 100.5018), "Phuket": (7.8804, 98.3400), "Chiang Mai": (18.7883, 98.9853),
    "Bali-Uluwatu": (-8.8291, 115.0849), "Bali-Legian": (-8.7050, 115.1750),
    "Jakarta": (-6.2088, 106.8456), "Jakarta-PIK": (-6.1080, 106.7400),
    "Kuala Lumpur": (3.1390, 101.6869), "Manila-Makati": (14.5547, 121.0244),
    "Quezon City": (14.6760, 121.0437), "Ho Chi Minh City": (10.8231, 106.6297),
    "Istanbul": (41.0082, 28.9784), "Istanbul-Atasehir": (40.9923, 29.1244),
    "Istanbul-Beykoz": (41.1300, 29.1000), "Ankara": (39.9334, 32.8597), "Izmir": (38.4237, 27.1428),
    "Seoul": (37.4979, 127.0276), "Busan": (35.1587, 129.0600), "Jeju": (33.4996, 126.5312),
    "Montreux": (46.4312, 6.9107), "Le Mont-Pelerin": (46.4869, 6.8447), "Genolier": (46.4364, 6.2136),
    "Zurich": (47.3769, 8.5417), "Weggis": (47.0325, 8.4340), "Bad Ragaz": (47.0059, 9.5028),
    "Teufen": (47.3820, 9.3860), "Lugano": (46.0037, 8.9511), "Kilchberg": (47.3220, 8.5430),
    "Zollikon": (47.3405, 8.5760), "Monaco": (43.7384, 7.4246), "Dubai": (25.2048, 55.2708),
    "Naples FL": (26.1420, -81.7948), "San Diego": (32.7157, -117.1611), "Albir": (38.5710, -0.0490),
    "Tbilisi": (41.7151, 44.8271), "Wroclaw": (51.1079, 17.0385), "Brussels": (50.8503, 4.3517),
    "Dornstetten": (48.4667, 8.4956), "Cologne": (50.9375, 6.9603), "Bad Aibling": (47.8642, 12.0104),
    "Panama City": (8.9824, -79.5199), "George Town": (19.2866, -81.3744), "Roatan": (16.3400, -86.5300),
}

TIERS = [
    (80, "A", "Verified · Well-Established", "#1f9d6b"),
    (65, "B", "Reputable · Do Your Diligence", "#2f86c9"),
    (50, "C", "Proceed With Caution", "#d9a021"),
    (35, "D", "High Risk · Experimental", "#e07b39"),
    (0,  "E", "Discredited / Avoid", "#c0392b"),
]

def tier_for(score):
    for lo, letter, label, color in TIERS:
        if score >= lo:
            return letter, label, color
    return "E", "Discredited / Avoid", "#c0392b"

rows = []
_seen = {}
def C(name, cat, citykey, country, web, spec, price, plo, phi,
      accr, est, ev, ac, tr, tk, sf, coast, signals, flags, defunct=False):
    lat, lng = CITY[citykey]
    i = _seen.get(citykey, 0); _seen[citykey] = i + 1
    if i:
        lat += 0.014 * math.cos(i * 2.399); lng += 0.014 * math.sin(i * 2.399)
    total = ev + ac + tr + tk + sf
    letter, label, color = tier_for(total)
    rows.append({
        "name": name, "category": cat, "city": citykey.split("-")[0].replace(" FL", ", FL"),
        "country": country, "lat": round(lat, 4), "lng": round(lng, 4),
        "website": web, "specialty": spec, "price": price,
        "price_low": plo, "price_high": phi, "accreditations": accr, "established": est,
        "scores": {"evidence": ev, "accreditation": ac, "transparency": tr,
                   "track_record": tk, "safety": sf},
        "trust_score": total, "tier": letter, "tier_label": label, "tier_color": color,
        "coast": coast, "trust_signals": signals, "red_flags": flags, "defunct": defunct,
    })

# ============================ DENTISTRY — MEXICO ============================
D = "Dentistry"
C("Trust Dental Care", D, "Tijuana", "Mexico", "https://trustdentalcare.com/",
  "Implants, All-on-4/6, veneers, full-mouth", "Implant ~$799; All-on-4 $3,196-8,500; crown $450", 799, 8500,
  "US-licensed dentist (CA #33592067), AACD, ICOI, AAID", "15+ yrs",
  28, 20, 13, 12, 12, "Pacific - 20 mi from San Diego harbor",
  "Only US-licensed dentist in group; 5-yr warranty; free border limo; 4.7 stars/300+ reviews",
  "Some headline prices are implants-only - confirm inclusions")
C("Cancun Cosmetic Dentistry", D, "Cancun", "Mexico", "https://www.cancuncosmeticdentistry.com/",
  "All-on-4, implants, smile makeovers", "All-on-4 from $10,800; implant $880-1,200; crown $990", 880, 12500,
  "Dr. Arzate - ABOI Diplomate (verifiable); AAID/ADA", "25+ yrs",
  28, 21, 13, 13, 12, "Caribbean - Cancun marinas",
  "Verifiable board credential; trained by All-on-4 inventor P. Malo; 8,000+ cases; IV sedation",
  "Promo vs regular pricing gap on snap-in dentures")
C("Cosmetic & Implant Dentistry Center (Dr. Valenzuela)", D, "Los Algodones", "Mexico",
  "https://www.algodonesdentalimplants.com/", "Implants, All-on-4/6, full-mouth, same-day",
  "Implant from $1,400; crown $450-800; veneer $450-800", 1400, 8000,
  "American-trained, ADA-affiliated; 50-yr family legacy", "since 2002",
  28, 19, 12, 12, 12, "Inland (near Yuma) - not sailing-accessible",
  "One accountable American-trained dentist; 20-yr implant warranty; CEREC same-day",
  "Higher single-implant price; small family-practice capacity")
C("Dental Destinations Cancun (Dentaris / Dr. Berron)", D, "Cancun", "Mexico",
  "https://www.dentaldestinationscancun.com/", "Implants, All-on-4/6, oral rehab, makeovers",
  "Full case ~$22,000 vs ~$75,000 US (~55% less)", 900, 22000,
  "Dr. Berron - former LSU implant-fellowship professor; GCR Top Clinic MX", "30+ yrs",
  28, 19, 11, 13, 12, "Caribbean - Cancun marinas",
  "Highest academic pedigree (LSU faculty); ~75% repeat/referral; master-ceramist lab",
  "Front brand is a facilitator over the clinic - clarify who treats & bills you")
C("Dental Zamora", D, "Playas de Rosarito", "Mexico", "https://dentalzamora.com/",
  "Implants, crowns, ortho, endo, perio, surgery", "Implant + crown ~$1,250", 300, 1250,
  "Baja/Mexican dental assoc. leaders; faculty instructors", "since 1992",
  28, 17, 12, 13, 12, "Pacific beachfront - 40 mi from Ensenada port",
  "30-yr track record; named dentists w/ published resumes; accepts US insurance",
  "Dated website; general family practice, not implant mega-clinic")
C("Algodones Dental Center", D, "Los Algodones", "Mexico", "https://www.algodonesdentalcenter.com/",
  "Implants, All-on-4/6/8, zygomatic, full-mouth", "Implant $790; All-on-4 $8,110; crown $490", 790, 8110,
  "ADA/ITI/ICOI affiliations; Nobel/Straumann/Zimmer", "37+ yrs lead",
  28, 18, 11, 12, 12, "Inland (Colorado River) - not sailing-accessible",
  "40+ dentists; in-house lab; 2-5 yr warranty; CBCT/CAD-CAM; free border shuttle",
  "Managed by third-party medical-tourism company - verify treating dentist")
C("Sani Dental Group", D, "Los Algodones", "Mexico", "https://sanidentalgroup.com/",
  "All-on-4 (Nobel), implants, full-mouth restoration", "Implant ~$750+; All-on-4 ~$8,000-11,000/arch", 750, 11000,
  "Top MX/US-school-trained dentists; ADM standard", "since 1985",
  28, 16, 10, 13, 12, "Inland - not sailing-accessible",
  "One of oldest/largest Molar City groups; on-site lab; dedicated dental-vacation planning",
  "Homepage light on specifics/prices; verify individual dentist per case")
C("Ocean Dental Cancun", D, "Cancun", "Mexico", "https://oceandentalcancun.com/",
  "All-on-4, 3-on-6, implants, full-mouth", "Implant $900; All-on-4 $10,800/arch; crown $450", 900, 10800,
  "States US board-certified/US-trained; Nobel/Ivoclar", "since ~2015",
  28, 16, 11, 12, 12, "Caribbean - Hotel Zone on the water",
  "1,000+ certified reviews; in-house lab; strict sterilization; 2,000+ full-mouth cases",
  "'US Board Certified' claim not individually documented")
C("RamLanz Dental Clinic", D, "Mexicali", "Mexico", "http://www.ramlanzdental.com/",
  "Implants, prosthesis, crowns, endo, ortho", "Implant ~$800-1,300; crown ~$300-450", 300, 1300,
  "ADA-affiliated dentists; award recognition", "since ~1986",
  28, 16, 10, 13, 12, "Inland - not sailing-accessible",
  "Nearly four decades operating; ADA affiliation; US phone lines",
  "Older/basic website; no online price list")
C("Pacific Implant Center", D, "Tijuana", "Mexico", "https://www.pacificimplantcenters.com/",
  "Implants, All-on-4/6/X, crowns, veneers", "Quote on request; markets large savings", 700, 9000,
  "States dentists US-trained (Harvard/Loma Linda/USC)", "14+ yrs",
  28, 16, 10, 11, 11, "Pacific - 5 min from San Diego border",
  "In-house lab w/ certified techs; modern medical plaza; US financing",
  "US-training claims not individually documented; no public price list")
C("Dr. Mexico Dental Group", D, "Tijuana", "Mexico", "https://www.tijuanadentistcenter.com/",
  "Implants, All-on-4/6, full-mouth, makeovers", "40-70% below US; price list on site", 300, 9000,
  "Current MX Health Dept certifications", "since 2014",
  28, 16, 11, 11, 11, "Pacific - minutes from San Ysidro",
  "Two-doctor practice; treatment plan before travel; border pickup; PPO help",
  "No headline price list; no US-board credential claimed")
C("Cancun Dental Design", D, "Cancun", "Mexico", "https://www.cancundentaldesign.com/",
  "All-on-4/6, 3-on-6, veneers, crowns, Invisalign", "All-on-4 $11,000/arch; veneer $250-450", 250, 11000,
  "Dr. Zamora DDS,MS; team lists MX license IDs", "15+ yrs",
  28, 14, 12, 11, 11, "Caribbean - Hotel Zone on the water",
  "Free airport+hotel transport; in-house lab; 3D CBCT; PPO reimbursement help",
  "No US-board credential; two-trip implant model")
C("Marietta Dental Care", D, "Tijuana", "Mexico", "https://www.mariettadentalcare.com.mx/",
  "General, cosmetic, restorative; crowns, implants", "Implant ~$800-1,300; crown ~$300-450", 300, 1300,
  "ADA member (per listings); Mexican-licensed", "unknown",
  28, 15, 9, 9, 11, "Pacific - 10 min from San Ysidro",
  "Family-owned; modern tech (lasers, 3D scanners); positive reviews",
  "Thin web presence; no online price list; founding year unstated")
C("Dental del Rio", D, "Los Algodones", "Mexico", "https://dentaldelrioalgodones.com/",
  "Implants, All-on-4/6/8, crowns, dentures", "Implant $750 (Nobel $1,000); All-on-4 $8,900", 750, 11100,
  "Works to ADA standards; brand-name implants", "family-owned",
  28, 13, 12, 9, 11, "Inland - not sailing-accessible",
  "Very transparent price list; free shuttle + lodging rates; CBCT/CAD-CAM",
  "No named accreditations/dentist bios; smaller than big groups")
C("Smile Crafters (Algodones Dental Group)", D, "Los Algodones", "Mexico", "https://algodonesdentalgroup.com/",
  "All-on-4, 3-on-6, implants, veneers, crowns", "All-on-4 $11,000/arch; implant from $990", 990, 13000,
  "PPO accepted; 'certified bilingual specialists'", "10+ yrs",
  28, 13, 11, 10, 11, "Inland - not sailing-accessible",
  "5-star Google; on-site luxury lodging; scheduled shuttle; transparent pricing",
  "Higher All-on-4 pricing than local peers; accreditation detail thin")
C("Dental Art Tijuana", D, "Tijuana", "Mexico", "https://www.dentalarttijuana.com/",
  "Implants, crowns, veneers, root canals", "Crown $450; implant $765; root canal $260-300", 80, 765,
  "None listed (continuing education only)", "unknown",
  28, 9, 11, 8, 10, "Pacific - minutes from San Ysidro",
  "Transparent published price list; in-house lab; US phone line",
  "No accreditations or dentist credentials named; marketing-heavy")
C("LUXE Dental", D, "Playas de Rosarito", "Mexico", "https://luxedentalrosarito.com/",
  "Implantology, All-on-4/6, aesthetics, 11 specialties", "Quote on request; membership savings", 300, 9000,
  "Named specialist dentists; no boards listed", "since ~2023",
  28, 11, 9, 6, 10, "Pacific beachfront - 30 min from San Diego",
  "Modern facility; 11 specialties under one roof; same-day crown tech",
  "Very new; no online prices; limited review history")
C("Dental Jardon", D, "Playas de Rosarito", "Mexico", "https://dentaljardon.com/",
  "Implants, crowns, ortho, endo, surgery, IV sedation", "Quote on request", 300, 9000,
  "States specialists 'certified'; none named", "unknown",
  28, 10, 7, 8, 10, "Pacific - near the beach",
  "Same-day treatment; own patient transport; IV sedation",
  "No price list; no named accreditations; thin bios")
C("Estetica Dental y Ortodoncia", D, "Mexicali", "Mexico", "https://esteticadentalyortodoncia.com/",
  "Implants, maxillofacial surgery, ortho, endo, perio", "Free estimates; quote on request", 300, 9000,
  "None specifically listed; named dentists", "site since 2023",
  28, 9, 6, 7, 10, "Inland - not sailing-accessible",
  "Digital radiography, laser; lists US insurer acceptance; US toll-free line",
  "Website has placeholder 'lorem ipsum' text - credibility caution")

# ============================ HAIR TRANSPLANTS — TURKEY ============================
H = "Hair Transplant"
C("ASMED (Dr. Koray Erdogan)", H, "Istanbul-Atasehir", "Turkey", "https://www.hairtransplantfue.org/",
  "Manual FUE, high-density artistic restoration", "~$6,000-12,000+ (priced per graft)", 6000, 12000,
  "MoH; IAHRS + AHLA + HairTransplantMentor recommended", "since ~2005",
  27, 22, 14, 14, 14, "Bosphorus - Galataport cruise berth",
  "World-renowned surgeon; proprietary FUE innovations; heavy peer reputation",
  "Not a budget option; long waitlists")
C("Civas Hair Transplant (Dr. Ekrem Civas)", H, "Ankara", "Turkey", "https://civashairtransplant.com/",
  "FUE, DHI, Sapphire FUE", "~$5,000-10,000", 5000, 10000,
  "FISHRS (1st in Turkey), ABHRS board-certified", "since 2006",
  27, 23, 14, 13, 14, "Landlocked (~200 km inland) - not sailing-accessible",
  "Among Turkey's most credentialed surgeons; one procedure/day; dermatology background",
  "Low daily volume means limited availability")
C("DrT Hair Transplant (Dr. Oguzoglu)", H, "Istanbul-Beykoz", "Turkey", "https://drthair.com/",
  "FUE, DHI, beard/eyebrow", "~$5,000-9,000", 5000, 9000,
  "FISHRS, ABHRS Diplomate; ISHRS award", "since 1998",
  27, 22, 13, 13, 14, "Bosphorus - Galataport",
  "Named award-winning surgeon; exclusive focus on hair surgery",
  "Premium tier; limited capacity")
C("HLC - Hairline Clinic (Dr. Oztan)", H, "Ankara", "Turkey", "https://www.fue-hlc.com/",
  "FUE, refined FUT, physician-led team", "~$5,000-10,000", 5000, 10000,
  "MoH; recognized early FUE pioneer", "since 2002",
  27, 20, 13, 13, 14, "Landlocked - not sailing-accessible",
  "One of the oldest serious FUE clinics; strong peer reputation",
  "Ankara location inconvenient for coastal travelers")
C("Smile Hair Clinic", H, "Istanbul-Atasehir", "Turkey", "https://www.smilehairclinic.com/en/",
  "FUE, Sapphire FUE, DHI", "All-inclusive ~$2,500-4,500", 2500, 4500,
  "MoH; TEMOS A-Rated (Turkey's 1st for hair); ISHRS-assoc founders", "since 2018",
  27, 18, 13, 11, 13, "Bosphorus - Galataport",
  "Two named founding surgeons; TEMOS accreditation; publishes safety guidance",
  "High patient throughput; technician-assisted steps common")
C("Dr. Resul Yaman Clinic", H, "Istanbul", "Turkey", "https://resulyaman.com/",
  "Manual FUE, beard/eyebrow, facial hair", "~$3,500-7,000", 3500, 7000,
  "ISHRS associate member, IAHRS-listed", "since 2009",
  27, 18, 13, 11, 13, "Bosphorus - Galataport",
  "Hands-on manual FUE by the named surgeon; IAHRS peer vetting",
  "Lower-volume; premium of quality over price")
C("Dr. Serkan Aygin Clinic", H, "Istanbul", "Turkey", "https://www.drserkanaygin.com/",
  "FUE, Sapphire FUE, DHI, robotic, women's", "All-inclusive ~$2,500-4,500", 2500, 4500,
  "MoH; claims JCI hospital setting + ISO 9001", "since 1996",
  27, 16, 11, 13, 12, "Bosphorus - Galataport",
  "One of Turkey's earliest hair physicians; huge review base; dermatology background",
  "Very high volume/global marketing; verify JCI claim applies to the facility")
C("Cosmedica (Dr. Levent Acar)", H, "Istanbul", "Turkey", "https://cosmedica.com/",
  "Sapphire FUE, DHI, Micro Sapphire", "All-inclusive ~$2,500-5,000", 2500, 5000,
  "MoH; Dr. Acar ISHRS associate; ISO-referenced", "since ~2008",
  27, 16, 11, 12, 12, "Bosphorus - Galataport",
  "Named surgeon; large documented case volume; strong reviews",
  "High marketing/celebrity spend; verify surgeon's personal involvement")
C("Vera Clinic", H, "Istanbul", "Turkey", "https://www.veraclinic.net/",
  "Sapphire FUE, DHI (Oxycure)", "All-inclusive ~$2,500-4,500", 2500, 4500,
  "MoH; claims ISHRS/ABHRS/EBHRS registration; ISO", "since ~2013",
  27, 14, 10, 11, 11, "Bosphorus - Galataport",
  "30,000+ patients; heavy review presence; 5-star packages",
  "Very high volume; no single celebrity surgeon - technician-assisted model")
C("Dr. Cinik Hair Transplant", H, "Istanbul", "Turkey", "https://drcinik.com/",
  "FUE, Sapphire FUE, DHI", "All-inclusive ~$2,500-4,500", 2500, 4500,
  "MoH; states ISHRS membership", "since 2013",
  27, 14, 10, 12, 11, "Bosphorus - Galataport",
  "Named dermatologist; 50,000+ procedures; large review base",
  "28 operating rooms = very high throughput; technicians do most graft work")
C("Elithair (Dr. Balwi)", H, "Istanbul", "Turkey", "https://elithair.com/",
  "DHI-focused, FUE, Sapphire; Pre-Test System", "All-inclusive ~$2,000-4,000", 2000, 4000,
  "MoH; TUV-certified (German quality mark)", "since 2015",
  27, 14, 9, 12, 11, "Bosphorus - Galataport",
  "TUV certification; very large volume; strong German-market presence + aftercare app",
  "'Biggest clinic in the world' throughput signal; surgery delegated to technicians")
C("Hair of Istanbul", H, "Istanbul", "Turkey", "https://www.hairofistanbul.com/",
  "FUE, Sapphire FUE, DHI", "All-inclusive ~$3,000-5,500", 3000, 5500,
  "MoH; plastic-surgeon supervision + anaesthesiologist", "since 2014",
  27, 13, 10, 10, 12, "Bosphorus - Galataport",
  "Premium branding; procedures planned under plastic-surgeon supervision",
  "'Surgeon-supervised' is not surgeon-performed - confirm who operates")
C("Asli Tarcan Clinic", H, "Istanbul", "Turkey", "https://aslitarcanclinic.com/",
  "FUE, DHI, Sapphire, beard/eyebrow, mesotherapy", "All-inclusive ~$2,500-4,500", 2500, 4500,
  "Turkish MoH accreditation", "2010s",
  27, 13, 10, 10, 12, "Bosphorus - Galataport",
  "Boutique, limited daily volume; personalized hairline design; strong Trustpilot",
  "No internationally-famous named surgeon - verify who operates")
C("Longevita", H, "Izmir", "Turkey", "https://www.longevitahairtransplant.com/",
  "FUE, DHI, Sapphire FUE", "All-inclusive ~$2,000-3,500", 2000, 3500,
  "MoH; UK-registered facilitator (UK aftercare)", "since ~2012",
  27, 12, 8, 11, 11, "Aegean - Alsancak cruise port / Cesme marina",
  "UK-facing follow-up presence; 40,000+ procedures; flexible payment",
  "Primarily a health-tourism facilitator - you may not know the surgeon until arrival")
C("Este Medical Group", H, "Istanbul", "Turkey", "https://www.estemedicalgroup.com/",
  "FUE, DHI, Sapphire FUE + cosmetic add-ons", "All-inclusive ~$2,500-4,500", 2500, 4500,
  "MoH; UK trading presence", "since ~2013",
  27, 12, 9, 10, 11, "Bosphorus - Galataport",
  "UK + Turkey footprint for follow-up; 20,000+ procedures; group scale",
  "Multi-service group/facilitator breadth; confirm operating surgeon")
C("Clinicana", H, "Istanbul", "Turkey", "https://www.clinicana.com/",
  "Sapphire FUE, DHI", "All-inclusive ~$2,500-4,500", 2500, 4500,
  "Turkish MoH", "since 2011",
  27, 12, 9, 10, 11, "Bosphorus - Galataport",
  "Long-running; established English/Arabic patient base",
  "No single famous named surgeon; technician-assisted volume model")
C("Heva Clinic", H, "Istanbul", "Turkey", "https://www.dentalhairclinicturkey.com/",
  "FUE, DHI, afro-textured & women's hair", "All-inclusive ~$2,000-4,000", 2000, 4000,
  "MoH; ISHRS-affiliated medical director (per clinic)", "2010s",
  27, 13, 10, 9, 12, "Bosphorus - Galataport",
  "Afro/curly-hair expertise (a genuine technical niche)",
  "Domain also markets dental tourism - confirm surgeon credentials directly")
C("Estenove", H, "Istanbul", "Turkey", "https://www.estenove.com/",
  "FUE, Sapphire FUE, DHI, beard/eyebrow", "All-inclusive ~$2,000-4,000", 2000, 4000,
  "Turkish MoH", "2010s",
  27, 11, 9, 9, 11, "Bosphorus - Galataport",
  "All-inclusive packages; personalized planning; multilingual coordination",
  "No prominently named lead surgeon; standard high-volume model")
C("Hermest Clinic", H, "Istanbul", "Turkey", "https://www.hermestclinic.com/",
  "FUE, Sapphire FUE, DHI", "All-inclusive ~$2,000-4,000", 2000, 4000,
  "Turkish MoH", "2010s",
  27, 11, 10, 9, 11, "Bosphorus - Galataport",
  "Transparent published price pages; all-inclusive packages",
  "No prominently named lead surgeon; tourism-volume model")
C("Medart Hair", H, "Istanbul", "Turkey", "https://www.medarthair.com/",
  "FUE, Sapphire FUE, DHI", "All-inclusive ~$2,000-3,500", 2000, 3500,
  "Turkish MoH", "2010s",
  27, 11, 10, 9, 11, "Bosphorus - Galataport",
  "Publishes useful Turkish law/regulation education content",
  "No named star surgeon; volume model")
C("Istanbul Vita", H, "Istanbul", "Turkey", "https://istanbulvita.com/",
  "Sapphire FUE (Vita zoning), DHI", "All-inclusive ~$2,000-4,000", 2000, 4000,
  "Turkish MoH", "2010s",
  27, 11, 9, 9, 11, "Bosphorus - Galataport",
  "Structured donor-analysis methodology; all-inclusive packages",
  "No prominently named lead surgeon; technique branding is marketing")
C("Hayatmed Clinic", H, "Istanbul", "Turkey", "https://www.hayatmed.com/",
  "FUE, DHI, Sapphire + plastic surgery", "All-inclusive ~$1,900-3,500", 1900, 3500,
  "Turkish MoH", "since 2016",
  27, 11, 9, 9, 11, "Bosphorus - Galataport",
  "All-inclusive packages; multi-specialty facility; published price guides",
  "Multi-specialty tourism operator; no prominently named hair surgeon")

# ============================ COSMETIC SURGERY — KOREA ============================
K = "Cosmetic Surgery"
C("JK Plastic Surgery", K, "Seoul", "South Korea", "https://www.jkplastic.com/en",
  "Facial contouring, two-jaw, rhino, eyes, breast", "Double eyelid $2,500-4,500; rhino $5,000-9,000", 2500, 22000,
  "MOHW foreign-patient institution; KAHF accredited", "since 1998",
  26, 22, 13, 14, 13, "Incheon port ~40 km",
  "Board-certified surgeons 20+ yrs; on-site anesthesiologists; ~4,000 foreign patients/yr",
  "Premium pricing; high-volume international operation - confirm named surgeon")
C("Banobagi Plastic Surgery", K, "Seoul", "South Korea", "https://eng.banobagi.com",
  "Facial contouring, rhino, eyes, breast, lifts", "Double eyelid $2,000-4,000; rhino $4,500-8,000", 2000, 18000,
  "MOHW foreign-patient institution; SNU-grad directors", "since 2000",
  26, 20, 14, 13, 13, "Incheon port ~40 km",
  "Explicit anti-ghost-surgery 'Real-Name System'; resident anesthesiologist; 8-language",
  "Book directly to avoid broker commission markups")
C("ID Hospital", K, "Seoul", "South Korea", "https://www.idhospital.com/en",
  "Facial bone contouring / orthognathic, FFS, rhino", "Contouring/two-jaw $12,000-25,000", 2000, 25000,
  "MOHW foreign-patient institution; KRI volume records", "since 1999",
  26, 19, 12, 13, 12, "Incheon port ~40 km",
  "15+ board-certified surgeons + anesthesiologists named; hospital-grade OR; 10-language",
  "Very high throughput - insist on one named operating surgeon (ghost-surgery risk)")
C("Dream Plastic Surgery", K, "Seoul", "South Korea", "https://en.e-dream.co.kr",
  "Eyes, rhino, contouring/two-jaw, breast, body", "Double eyelid $1,800-3,800; rhino $4,000-7,500", 1800, 18000,
  "MOHW foreign-patient institution; SNU-grad founders", "since 1999",
  26, 18, 12, 13, 13, "Incheon port ~40 km",
  "States 20+ yrs w/ no medical accidents; 9 monitored ORs; on-site anesthesiologists",
  "Standard Gangnam caveats - verify surgeon certification")
C("VIP Plastic Surgery (Dr. Lee)", K, "Jeju", "South Korea", "https://www.vippskorea.com",
  "Deep-plane facelift, rib rhino, eyes, contouring", "Rhino $5,000-9,000; deep-plane facelift $12,000-20,000", 2000, 20000,
  "MOHW foreign-patient institution", "since 2001",
  26, 18, 13, 12, 13, "Jeju Island - Jeju/Seogwipo ports (sailing fit)",
  "Led by Dr. M.J. Lee (MD, PhD, 25+ yrs); in-house anesthesiologist; all-inclusive packages",
  "Boutique single-surgeon model - limited capacity")
C("HERSHE Plastic Surgery & Dermatology", K, "Seoul", "South Korea", "https://hershebeauty.com",
  "Facelift/lifting, breast, rhino, eyes, derma", "Double eyelid $2,000-4,000; facelift $9,000-15,000", 2000, 15000,
  "MOHW foreign-patient institution; Yonsei/Severance", "since ~1996",
  26, 18, 11, 13, 12, "Incheon port ~40 km",
  "Surgeons trained at Yonsei; Severance-certified chief director; strong lifting track record",
  "English domain is JS-rendered - confirm it loads before relying on it")
C("JW Plastic Surgery", K, "Seoul", "South Korea", "https://jwbeauty.net",
  "Revision (eyes/nose/breast), rhino, contouring", "Rhino $4,500-8,500 (revision higher); breast $6,000-9,000", 2000, 9000,
  "MOHW foreign-patient institution", "since ~2000",
  26, 17, 12, 12, 12, "Incheon port ~40 km",
  "Board-certified surgeons; noted for revision/corrective work; 5-language coordinators",
  "Standard Gangnam caveats")
C("VIEW Plastic Surgery", K, "Seoul", "South Korea", "https://www.viewplasticsurgery.com",
  "Facial contouring/two-jaw, breast, rhino, eyes", "Double eyelid $2,000-4,000; contouring $10,000-20,000", 2000, 20000,
  "MOHW foreign-patient institution", "since 2005",
  26, 17, 11, 12, 12, "Incheon port ~40 km",
  "Board-certified surgeons; dedicated 19-story building; international patient center",
  "Confirm the operating surgeon; avoid broker packages")
C("Wonjin Plastic Surgery", K, "Seoul", "South Korea", "https://wonjinbeauty.com/en",
  "Contouring, rhino, eyes, breast, lipo, anti-aging", "Double eyelid $1,800-3,800; contouring $9,000-18,000", 1800, 18000,
  "MOHW foreign-patient institution", "since 1999",
  26, 17, 11, 13, 11, "Incheon port ~40 km",
  "Positions as Korea's largest general PS hospital; specialized centers; 10-language support",
  "Large marketing-heavy operation - verify surgeon board certification")
C("Girin Plastic Surgery", K, "Seoul", "South Korea", "https://www.girinpsen.com",
  "Contouring, breast, lipo/body, eyes, rhino", "Double eyelid $1,800-3,800; contouring $9,000-17,000", 1800, 17000,
  "KIMA-certified under MOHW; foreign-patient institution", "2010s",
  26, 17, 11, 11, 12, "Incheon port ~40 km",
  "Full-time anesthesiologists; specialist teams; open Sundays; interpreters",
  "Standard Gangnam caveats")
C("GNG Hospital", K, "Seoul", "South Korea", "https://en.gnghospital.com",
  "Rhino / revision rhino, contouring, eyes", "Double eyelid $2,000-4,000; rhino $4,500-8,500", 2000, 19000,
  "MOHW foreign-patient institution", "2010s",
  26, 17, 11, 11, 12, "Incheon port ~40 km",
  "Board-certified plastic surgeons + ENT (functional + cosmetic nose)",
  "Standard Gangnam caveats")
C("She's Plastic Surgery (Busan)", K, "Busan", "South Korea", "https://www.shesps.com/eng",
  "Facelift/anti-aging, eyes, rhino, lifting", "Double eyelid $1,500-3,500; facelift $8,000-14,000", 1500, 14000,
  "MOHW foreign-patient institution", "since 2000",
  26, 16, 11, 12, 12, "Busan - major cruise/yacht port (sailing fit)",
  "Board-certified surgeons; 6-language interpreters; established Busan clinic",
  "Smaller regional clinic - verify surgeon credentials for major procedures")
C("Grand Plastic Surgery", K, "Seoul", "South Korea", "https://eng.grandsurgery.com",
  "Contouring, rhino, eyes, breast, body", "Double eyelid $2,000-4,000; contouring $10,000-20,000", 2000, 20000,
  "MOHW foreign-patient institution", "2010s",
  26, 16, 10, 12, 11, "Incheon port ~40 km",
  "~20-surgeon team incl. anesthesiologists; 21-story facility; 7-language consultants",
  "Very high-volume celebrity-marketing clinic - confirm named surgeon")
C("DA Plastic Surgery", K, "Seoul", "South Korea", "https://daprseng.com",
  "Rhino, contouring, lifting, eyes, body", "Double eyelid $2,000-4,000; rhino $4,000-8,000", 2000, 18000,
  "MOHW foreign-patient institution", "2010s",
  26, 16, 11, 11, 12, "Incheon port ~40 km",
  "Board-certified surgeons; established international sites & coordinators",
  "Standard Gangnam caveats - verify surgeon certification")
C("Cinderella Plastic Surgery", K, "Seoul", "South Korea", "https://cindyhospital.com",
  "Contouring, rhino, eyes, anti-aging, body", "Double eyelid $1,800-3,800; contouring $9,000-17,000", 1800, 17000,
  "MOHW-registered / govt-certified institution", "2000s",
  26, 16, 10, 12, 12, "Incheon port ~40 km",
  "Board-certified surgeons; multiple domestic awards; on-site interpreters",
  "Standard Gangnam caveats")
C("Braun Plastic Surgery", K, "Seoul", "South Korea", "https://www.braunps.com",
  "Rhino, contouring, eyes, lifting, breast, body", "Double eyelid $1,800-3,800; rhino $4,000-8,000", 1800, 18000,
  "MOHW foreign-patient institution", "2010s",
  26, 16, 10, 11, 12, "Incheon port ~40 km",
  "Board-certified surgeons; dedicated multi-floor Braun Building",
  "Standard Gangnam caveats")
C("DESIGN Plastic Surgery (Busan)", K, "Busan", "South Korea", "https://designprsglobal.com",
  "Eyes, rhino, contouring, lifting, body", "Double eyelid $1,500-3,500; contouring $8,000-15,000", 1500, 15000,
  "MOHW foreign-patient institution", "2010s",
  26, 14, 9, 10, 11, "Busan - major cruise/yacht port (sailing fit)",
  "English 'global' site + consultation team; central Seomyeon district",
  "Small clinic; limited public credential detail - request KSPRS verification")
C("AB Plastic Surgery", K, "Seoul", "South Korea", "https://abplasticsurgerykorea.com",
  "Eyes, rhino, contouring, breast, body, derma", "Double eyelid $1,800-3,800; rhino $4,000-7,500", 1800, 17000,
  "MOHW foreign-patient institution", "since 2020",
  26, 15, 11, 9, 12, "Incheon port ~40 km",
  "30+ specialists; in-house English interpreters; travel/accommodation support",
  "Newer clinic (2020) - shorter track record; verify board certification")
C("Link Plastic Surgery", K, "Seoul", "South Korea", "https://www.linkpskorea.com",
  "Eyes, rhino, contouring, breast, body, anti-aging", "Double eyelid $1,800-3,800; rhino $4,000-7,500", 1800, 17000,
  "MOHW foreign-patient institution", "2010s",
  26, 15, 10, 10, 12, "Incheon port ~40 km",
  "Board-certified surgeons; dedicated international-patient service",
  "Smaller clinic - confirm surgeon volume/credentials for complex procedures")

# ============================ EXOSOMES — SOUTHEAST ASIA ============================
X = "Exosomes / Regenerative"
C("Healthi Life (Urban Longevity House)", X, "Bangkok", "Thailand", "https://healthi-life.com/services/exosome-therapy-bangkok",
  "MSC exosome IV, facial, hair; stem cell; NAD+/peptide", "Exosome IV ~$1,000-4,300; stem cell from ~$12,000", 1000, 12000,
  "GMP/ISO partner labs (claimed); named physicians", "unknown",
  10, 12, 13, 8, 10, "Gulf of Thailand - Pattaya marinas ~2 hrs",
  "Unusually candid: states exosome therapy is investigational & not FDA-approved; transparent pricing",
  "EXPERIMENTAL / not FDA-approved; uses cosmetic exosome brand; award is promotional")
C("Nexus Clinic KL", X, "Kuala Lumpur", "Malaysia", "https://www.nexus-clinic.com/regenerative/stem-cell-therapy-malaysia/",
  "UC-MSC stem cell IV, exosome-enhanced, hormones", "MSC RM15,000-75,000 ($3,400-17,000)", 3400, 17000,
  "MOH-compliant sources; MMC-registered doctors; accredited labs", "unknown",
  10, 13, 14, 9, 10, "Inland - Port Klang / Port Dickson marina ~1.5 hr",
  "Most clinically literate site: cites evidence levels, references, 'avoid absolute-cure claims'",
  "EXPERIMENTAL; anti-aging cell indications remain investigational; allogeneic donor cells")
C("Cervantes Dermcenter", X, "Manila-Makati", "Philippines", "https://cervantesclinic.com/exosomes",
  "Exosome skin/hair (ASCE+) via microneedle, laser", "Exosome facial ~$150-400", 150, 400,
  "Board-certified dermatologists; Korean ASCE+ product", "site 2022",
  10, 13, 13, 9, 11, "Manila Bay - Manila Yacht Club",
  "Most evidence-cautious PH site: states injectables 'not FDA approved'; lists references",
  "EXPERIMENTAL; ASCE+ is a cosmetic-grade product, not an approved drug")
C("SOMA Aesthetics & Longevity Club", X, "Bali-Uluwatu", "Indonesia", "https://www.somalongevityclub.com/exosome-therapy-bali",
  "Autologous + GMP exosomes, PRP, IV, secretome", "Exosomes from $460; autologous $490-735", 185, 735,
  "Licensed Klinik Utama; GMP Korean exosomes; MBChB physician", "unknown",
  10, 13, 13, 8, 10, "Uluwatu coast - Benoa Harbour ~45 min (sailing fit)",
  "Most transparent pricing; cites PMIDs; discusses cold-chain/sourcing; warns of fake exosomes",
  "EXPERIMENTAL; 'autologous exosome' extraction claim exceeds what a centrifuge can isolate")
C("Revival Clinic Bangkok", X, "Bangkok", "Thailand", "https://www.revivalclinicbangkok.com/",
  "Exosome IV/facial/hair, stem cell, plasma, NAD+", "Exosome IV ~$900-1,400; stem cell several $k", 900, 4000,
  "Thai-physician-led; marketing awards", "since ~2013",
  9, 11, 11, 10, 10, "Gulf of Thailand - Pattaya marinas ~2 hrs",
  "Transparent published pricing; doctor-led; 'we don't jump to unproven treatments' messaging",
  "EXPERIMENTAL; awards are pay-to-enter; young-blood plasma offering outside proven medicine")
C("LYFE Medical Wellness", X, "Phuket", "Thailand", "https://www.lyfemedical.com/regenerative-medicine/exosome-therapy/",
  "MSC exosome IV + injection, UC-MSC, PRP, NAD+, HBOT", "Exosome IV ~$1,000-3,000 (quote-based)", 1000, 3000,
  "Physician licensed by Medical Council of Thailand", "unknown",
  10, 12, 10, 8, 10, "Phuket - Andaman Sea, direct marina access (sailing fit)",
  "Physician-led; two named clinics; honest 'we advise what evidence supports' language",
  "EXPERIMENTAL; prices gated behind consult; broad indication list; allogeneic exosomes")
C("Medeze Medical (Vietnam)", X, "Ho Chi Minh City", "Vietnam", "https://medezemedical.vn/en/ve-chung-toi/",
  "Stem cell, NK cell, cell-level anti-aging, PRP, NAD+", "Custom quote (region $1,750-68,000)", 1750, 68000,
  "MoH-licensed model; named medical director; Japanese advisors", "since ~2021",
  9, 13, 9, 10, 10, "Saigon River - Vung Tau coast ~2 hrs",
  "Regional group w/ lab & advisory infrastructure; named credentialed physicians",
  "EXPERIMENTAL; NK-cell & anti-aging claims unproven; celebrity-doctor marketing; opaque pricing")
C("Asia Stem Cell Center", X, "Jakarta", "Indonesia", "https://asiastemcellcenter.com/",
  "GMP lab: exosome, secretome, NK, MSC for skin/organ", "Quote on consult", 2000, 20000,
  "MoH operational permit; GMP-certified processing lab", "since ~2019",
  9, 14, 10, 10, 9, "Java Sea coast - Ancol marina",
  "Genuine GMP cell-manufacturing lab w/ MoH permit; hospital partnership; publishes research",
  "EXPERIMENTAL; markets stem cells for autism/stroke/Parkinson's - claims outrun approval")
C("NuLook Clinic", X, "Bali-Legian", "Indonesia", "https://nulook.co.id/services/nu-capture-youth-booster",
  "Exosome facial/skin, SVF stem cell, PRP, aesthetics", "Exosome from ~$185/cc", 185, 2000,
  "Licensed aesthetic/plastic-surgery clinic", "exosome page 2024",
  9, 11, 11, 10, 10, "Legian beachfront - Benoa yacht harbour ~30-40 min",
  "Clear pricing; medical disclaimer; named doctors; established multi-service Bali clinic",
  "EXPERIMENTAL; exosome as topical 'booster' (weakest evidence tier); sourcing undisclosed")
C("The M.A.C. Clinic", X, "Kuala Lumpur", "Malaysia", "https://www.mac-clinic.my/exosome",
  "Exosome skin & hair (injection/topical/combo)", "Quote on consult (region ~$300-900)", 300, 900,
  "Aesthetic-doctor-led; multi-branch KL brand", "unknown",
  8, 11, 9, 10, 9, "Inland - Port Klang / Port Dickson ~1.5 hr",
  "Well-known multi-location KL aesthetics group; doctor-administered",
  "EXPERIMENTAL; light on sourcing/evidence; purely aesthetic framing")
C("Plenary Longevity Wellness", X, "Phuket", "Thailand", "https://plenarywellness.com/en/cellular-therapy-with-exosome/",
  "Exosome IV + injection, stem cell, NK, placenta, NAD+", "Quote-based (~$1,000-3,500/session)", 1000, 3500,
  "Licensed physician-led; multilingual", "site since ~2023",
  8, 10, 8, 8, 8, "Nai Harn coast - Chalong Bay marina (sailing fit)",
  "Detailed pre/post protocols; honest 'what exosome therapy does NOT do' section",
  "EXPERIMENTAL; full menu of unproven modalities (NK, placenta); opaque pricing")
C("Cell Quest (Gleneagles KL)", X, "Kuala Lumpur", "Malaysia", "https://cellquest.com.my/",
  "Stem-cell infusion, exosome, NK cancer immuno, NAD+", "Cell therapy RM8,000-80,000 (on consult)", 1800, 18000,
  "Delivered at JCI-accredited Gleneagles Hospital KL", "since ~2015",
  9, 13, 8, 9, 10, "Inland - Port Klang / Port Dickson ~1.5 hr",
  "Hospital-based delivery (Gleneagles); allergy/immunology clinician backing",
  "EXPERIMENTAL; testimonials claim stroke/liver/psoriasis recovery - cure-adjacent overreach")
C("Idara Aesthetics", X, "Manila-Makati", "Philippines", "https://idara.ph/exosomes-exoten-for-skin-glow-advanced-regenerative-facial-treatment/",
  "Exosome facial ('Exoten', amniotic) for skin glow", "~$60-200/session", 60, 200,
  "Medically guided; distributor-exclusive product", "unknown",
  8, 9, 8, 9, 9, "Manila Bay - Manila Yacht Club",
  "Large branch network; medical-supervision framing; cites literature",
  "EXPERIMENTAL; mall-based medi-spa scale; amniotic exosome sourcing questions")
C("RCERT (Regional Cell Research & Therapy Centre)", X, "Kuala Lumpur", "Malaysia", "https://rcertherapeutics.com/therapies-for-exosome/",
  "MSC exosome IV/injection/scalp, MSC infusion, NK, HBOT", "Quote on consult", 2000, 20000,
  "Registered biotech; cGMP labs (claimed); UNIMAS + China ties", "since 2024",
  8, 11, 8, 6, 8, "Inland - Port Klang / Port Dickson ~1.5 hr",
  "Research-company framing; named professors; flags neuro use as 'investigational'",
  "EXPERIMENTAL; very new (2024); China cell-tech partner; broad anti-aging/immune claims")
C("Biothera Stemcell Clinic", X, "Jakarta-PIK", "Indonesia", "https://www.biotherastemcell.id/en",
  "Stem cell + secretome + exosome + NK; anti-aging", "Quote on consult", 2000, 20000,
  "Delivered at 'BPOM-licensed clinics'; named specialists", "site 2025",
  7, 9, 6, 7, 7, "Java Sea (PIK) coast - Ancol/PIK marina",
  "Named specialist physicians; positions as medically supervised",
  "EXPERIMENTAL; very broad disease claims (Parkinson's, ALS, cancer via NK); placeholder socials")
C("R3 Stem Cell Philippines", X, "Quezon City", "Philippines", "https://r3stemcell.com/philippines/",
  "UC-MSC + exosome via IV, injection, intrathecal", "From ~$5,250", 5250, 20000,
  "US-HQ franchise; claims 'exceeds FDA QA' (not approval)", "PH program recent",
  6, 8, 6, 9, 5, "Manila Bay - Manila Yacht Club",
  "High procedure volume; structured intake; states therapy is 'experimental, not FDA-approved'",
  "EXPERIMENTAL - STRONGEST RED FLAGS: markets cells for autism/ALS/stroke/CP with emotive testimonials")
C("Jakarta Stemcell Centre", X, "Jakarta", "Indonesia", "https://jakartastemcellcentre.id/",
  "Allograft regenerative, secretome/EV, UC & amniotic MSC", "Quote on consult", 2000, 20000,
  "Not verifiable from live page", "unknown",
  8, 9, 5, 7, 8, "Java Sea coast - Ancol marina",
  "Focus on cell-free secretome/EV therapy; established local brand",
  "EXPERIMENTAL; minimal public transparency - accreditation/pricing/physician unverifiable")
C("Boston Health Longevity", X, "Chiang Mai", "Thailand", "https://bostonhealthlongevity.com/longevity-library/treatments/exosome-therapy",
  "Exosome IV & injection, stem cell, NAD+, DNA-age test", "30-70% below Western (~$1,000-3,500)", 1000, 3500,
  "None specific published", "unknown",
  8, 8, 6, 8, 8, "Chiang Mai inland (use Phuket branch for sailing)",
  "Positions around measurable biomarkers (methylation testing); two locations",
  "EXPERIMENTAL; heavy '#1' superlatives; thin verifiable accreditation")
C("Exosomes Thailand", X, "Chiang Mai", "Thailand", "https://exosomesthailand.com/",
  "Exosome IV therapy & injection", "Region ~$1,000-3,000", 1000, 3000,
  "Not verifiable from site", "unknown",
  8, 7, 5, 6, 8, "Chiang Mai - landlocked",
  "Domain focused solely on exosomes",
  "EXPERIMENTAL; '#1' branding; near-zero hard content or licensing/pricing transparency")

# ============================ LIFE EXTENSION — SWITZERLAND + PEERS ============================
L = "Life Extension / Longevity"
C("Human Longevity, Inc. (Health Nucleus)", L, "San Diego", "USA", "https://www.humanlongevity.com",
  "Whole-genome + full-body MRI, multi-omic, executive", "Executive from ~$8,000; full program $15,000-25,000", 8000, 25000,
  "US-licensed precision-medicine clinics", "since 2013",
  18, 18, 13, 13, 14, "Pacific - San Diego Bay marinas (sailing fit)",
  "Deep genomics pedigree (J. Craig Venter); peer-reviewed whole-body screening data",
  "Screening-overdiagnosis risk; 'add years to your life' outpaces proof; very high cost")
C("Metabolic (GluCare) - Longevity", L, "Dubai", "UAE", "https://metabolic.health/longevity/",
  "100+ biomarker testing/imaging, peptides, HRT/TRT", "Membership ~$2,000-8,000/yr", 2000, 8000,
  "UAE MOHAP-licensed; physician-ordered labs", "2020s",
  16, 17, 14, 11, 13, "Persian Gulf - Dubai Harbour marinas (sailing fit)",
  "Genuinely diagnostics-led; transparent; insurance-free; multi-specialty physician team",
  "Peptides/HRT + heavy testing risk over-treatment; marketing outruns lifespan evidence")
C("Clinique La Prairie", L, "Montreux", "Switzerland", "https://www.cliniquelaprairie.com",
  "Cell therapy 'Revitalisation', longevity diagnostics", "7-day program ~$37,000-75,000+", 37000, 75000,
  "Swiss-licensed private clinic; luxury networks", "since 1931",
  14, 16, 12, 15, 13, "Lake Geneva - Mediterranean via Genoa ~270 km",
  "50+ on-site physicians; 90+ yr track record; genetic/epigenetic testing; licensed stem cell",
  "Flagship 'revitalisation' descends from unproven fresh-cell therapy; extreme cost")
C("Fountain Life", L, "Naples FL", "USA", "https://www.fountainlife.com",
  "Whole-body MRI, coronary CTA, 100+ biomarkers, genome", "CORE ~$6,500; APEX ~$19,500-21,500/yr", 6500, 21500,
  "US-licensed physicians/imaging", "since 2020",
  16, 17, 13, 11, 13, "Gulf of Mexico - Naples City Dock marinas (sailing fit)",
  "High-end validated imaging (MRI/CTA) with real early-detection value; physician review",
  "Whole-body MRI in healthy people risks incidentalomas; regenerative/stem-cell upsell")
C("Clinique Nescens (Genolier)", L, "Genolier", "Switzerland", "https://www.nescens.com",
  "Preventive longevity medicine, epigenetics, better-aging", "~$5,000-25,000+ (quote-based)", 5000, 25000,
  "Swiss Medical Network hospital-adjacent; academic founder", "since ~2000",
  16, 17, 12, 12, 13, "Lake Geneva - Mediterranean via Genoa ~280 km",
  "Founded by biology-of-aging academic (Prof. Proust); emphasis on validated diagnostics",
  "Some regenerative/stem-cell offerings outpace hard outcome evidence")
C("Grand Resort Bad Ragaz - Tamina Health", L, "Bad Ragaz", "Switzerland", "https://www.resortragaz.ch/en/tamina-health",
  "Longevity, detox, check-up, thermal/spa medicine", "~$3,000-20,000+ + accommodation", 3000, 20000,
  "30+ physicians/specialists; Swiss-licensed medical resort", "modern center",
  15, 16, 12, 13, 13, "Rhine valley - Lake Constance ~45 km",
  "Large multidisciplinary medical/rehab team; genuine diagnostic & rehab capability",
  "Longevity branding layered on spa/rehab; some naturopathy units with limited evidence")
C("SHA Wellness Clinic", L, "Albir", "Spain", "https://shawellnessclinic.com",
  "Advanced Longevity program, hypoxia, NAD, nutrition", "~EUR 3,000-20,000+ incl. stay (Longevity ~EUR 12,000)", 3300, 22000,
  "Spanish-licensed medical clinic; internationally awarded", "since 2008",
  14, 16, 13, 13, 13, "Mediterranean - Altea/Benidorm marinas (sailing fit)",
  "Large medical staff; structured diagnostics; macrobiotic-nutrition heritage",
  "NAD/hyperbaric/hypoxia lack lifespan-extension proof; luxury pricing")
C("Seegarten Clinic - Longevity Center Zurich", L, "Kilchberg", "Switzerland", "https://www.sgk.swiss/en/longevity-center-zurich.html",
  "Cause-oriented preventive medicine, longevity check-ups", "Check-ups ~$920-2,300; programs higher", 920, 8000,
  "Swiss-licensed medical clinic (Canton Zurich)", "recent focus",
  16, 16, 13, 11, 13, "Lake Zurich - Mediterranean via Genoa ~330 km",
  "Transparent check-up pricing; physician-led; prevention-focused (no miracle-cure marketing)",
  "'Longevity' programs still rest on standard preventive medicine; limited outcome data")
C("Thermes Marins Monte-Carlo", L, "Monaco", "Monaco", "https://www.thermesmarinsmontecarlo.com",
  "Preventive-health medical spa, diagnostics, thalasso", "Programs ~$2,000-10,000+ + accommodation", 2000, 10000,
  "Monaco SBM group; medical team of doctors/nutritionists", "since 1895",
  12, 15, 12, 13, 13, "Mediterranean - Port Hercule, Monaco (ideal embarkation)",
  "Long institutional heritage; multidisciplinary medical/sports team; 7-pillar framework",
  "Thalasso/'wellbeing' claims are relaxation-grade, not life-extension; resort pricing")
C("Longevity Center Switzerland (Zurich)", L, "Zurich", "Switzerland", "https://longevity-center.eu/longevity-center-switzerland/",
  "Longevity diagnostics, biomarker/bio-age panels, IHHT", "Packages ~$3,000-15,000+ (quote-based)", 3000, 15000,
  "Swiss-licensed; European Longevity Center network", "2020s",
  15, 16, 12, 9, 13, "Lake Zurich - Mediterranean via Genoa ~330 km",
  "Board-certified medical director; structured biomarker evaluation; science-based positioning",
  "Many modalities improve short-term biomarkers only; no proof of lifespan benefit")
C("LaCLINIQUE of Switzerland (Lugano)", L, "Lugano", "Switzerland", "https://www.lacliniqueofswitzerland.ch",
  "Aesthetic/regenerative, autologous stem-cell anti-aging", "Programs ~$3,000-20,000+", 3000, 20000,
  "Swiss-licensed; GMP cell-processing lab in Zurich", "2000s",
  12, 15, 11, 11, 12, "Lake Lugano - Mediterranean via Genoa ~190 km",
  "GMP-regulated cell processing; licensed surgeons; defined pathway for autologous cells",
  "Primarily aesthetic surgery with a 'longevity' overlay; anti-aging cell claims exceed evidence")
C("Chenot Palace Weggis", L, "Weggis", "Switzerland", "https://www.chenot.com/chenot-palace/weggis/",
  "Medical spa/detox (Chenot Method), diagnostics", "From ~EUR 1,200/day; 7-night ~$9,000-34,000+", 9000, 34000,
  "Swiss-licensed medical spa; 'best detox' awards", "property 2020",
  11, 14, 11, 11, 12, "Lake Lucerne - Mediterranean via Genoa ~300 km",
  "On-site medical team + diagnostics; structured 5,000 sqm medi-spa; physician oversight",
  "'Detox' is a marketing construct; bioenergetics blend; limited peer-reviewed evidence")
C("Swiss Center for Health & Longevity", L, "Zollikon", "Switzerland", "https://health-longevity-center.com",
  "Preventive & functional medicine, longevity diagnostics", "Assessments ~$3,000-15,000+", 3000, 15000,
  "Swiss-licensed private center", "2020s",
  13, 14, 11, 9, 12, "Lake Zurich - Mediterranean via Genoa ~330 km",
  "Physician-led preventive model; structured diagnostics; Lake Zurich setting",
  "Functional-medicine tests/supplements of limited evidentiary value; newer entrant")
C("The Longevity Suite (Lugano)", L, "Lugano", "Switzerland", "https://thelongevitysuite.com/en/centres/lugano/",
  "Biohacking, cryotherapy, ozone/IV, check-ups", "Sessions/bundles ~$1,000-10,000+", 1000, 10000,
  "Registered Swiss medical practice (Ticino)", "brand since ~2018",
  10, 12, 10, 10, 11, "Lake Lugano - Mediterranean via Genoa ~190 km",
  "Physician-supervised check-ups; standardized protocols across a chain",
  "Core 'biohacking' stack has no proven lifespan benefit; retail-wellness positioning")
C("Clinique Lemana", L, "Le Mont-Pelerin", "Switzerland", "https://lemana.com",
  "Revitalization (organ-extract injections), detox, epigenetics", "On request (typically low-to-mid 5 figures)", 8000, 40000,
  "Swiss-licensed; references some device approvals", "since 1952",
  8, 12, 8, 12, 10, "Lake Geneva - Mediterranean via Genoa ~270 km",
  "70-yr operating history; physician-supervised; epigenetic bio-age testing",
  "Core organ-extract injections biologically implausible; markets bioresonance/'Metatron' pseudoscience")
C("Paracelsus Clinic Lustmuhle", L, "Teufen", "Switzerland", "https://www.paracelsus.com",
  "'Biological medicine', integrative, cancer support", "Programs ~$5,000-20,000+", 5000, 20000,
  "Swiss-licensed clinic; integrative reputation", "since 1958",
  7, 11, 8, 12, 9, "Appenzell foothills - Lake Constance ~30 km",
  "One-campus multidisciplinary team; decades of operation",
  "'Rebuilds body cell by cell' + alt cancer claims unsupported; 'results you can't get anywhere else'")

# ============================ FRINGE — PHAGE / CANCER / STEM CELL / GENE ============================
P = "Phage Therapy"
CA = "Alt./Immuno Cancer"
SC = "Stem Cell"
G = "Gene / Other Fringe"
C("Hirszfeld Institute - Phage Therapy Unit", P, "Wroclaw", "Poland", "https://hirszfeld.pl/en/structure/iitd-pan-medical-center/phage-therapy-unit/",
  "Ethics-approved experimental phage therapy for resistant infections", "Cost-recovery / on request", 2000, 8000,
  "Polish Academy of Sciences institute; bioethics-committee governed", "PTU since 2005",
  18, 16, 13, 14, 14, "Baltic via Szczecin ~370 km",
  "Gold standard for ethically-governed EU phage therapy; extensive peer-reviewed literature",
  "Not an approved therapy; access restricted & slow by design; not a walk-in service")
C("Queen Astrid Military Hospital - Phage Program", P, "Brussels", "Belgium", "https://www.bacteriophage.news/database/queen-astrid-military-hospital/",
  "Magistral (compounded) phage for severe resistant infections", "Compassionate use only", 0, 0,
  "Belgian military hospital; national magistral legal framework; GMP", "phage since 2007",
  18, 17, 12, 13, 15, "North Sea via Zeebrugge/Ostend ~110 km",
  "Model of responsible physician-gated phage access; peer-reviewed workflow; rigorous selection",
  "Not accessible as tourism; extremely selective; long waits; case-by-case only")
C("Eliava Phage Therapy Center", P, "Tbilisi", "Georgia", "https://eptc.ge/",
  "Personalized bacteriophage therapy; in-clinic + distance courses", "Low thousands per course (on request)", 1500, 6000,
  "Clinical arm of the G. Eliava Institute (state research institute)", "institute since 1923",
  17, 14, 11, 14, 12, "Black Sea via Batumi ~370 km",
  "Most legitimate name in phage tourism; world's largest phage library; peer-reviewed case series",
  "Efficacy claims outpace controlled trials; mailing phages internationally is dubious; unlicensed in West")
C("Phage Therapy Center", P, "Tbilisi", "Georgia", "https://www.phagetherapycenter.com/",
  "Commercial phage therapy for international patients", "Among pricier phage options (on request)", 3000, 12000,
  "Private commercial clinic sourcing Georgian phages", "since 2004",
  15, 9, 7, 11, 10, "Black Sea via Batumi ~370 km",
  "Long operating history; large self-reported patient volume (120+ countries)",
  "Marketing-heavy ('95%+ success') with non-peer-reviewed stats; less academically anchored than Eliava")
C("IOZK - Immun-Onkologisches Zentrum Koln", CA, "Cologne", "Germany", "https://www.iozk.de/en/",
  "Individualized multimodal immunotherapy (dendritic vaccine + NDV + hyperthermia)", "Tens of thousands EUR (on request)", 25000, 80000,
  "German section-13 AMG manufacturing license for its vaccine; GMP lab", "since 1985",
  12, 15, 10, 12, 11, "North Sea via Rhine to Rotterdam ~230 km",
  "More scientifically serious than most: real manufacturing license, published clinical experience",
  "EXPERIMENTAL; evidence is uncontrolled single-institution case series; out-of-pocket")
C("Klinik St. Georg (Bad Aibling)", CA, "Bad Aibling", "Germany", "https://www.klinik-st-georg.de/en/",
  "Integrative oncology - hyperthermia, IPT low-dose chemo, PDT", "Multi-week packages tens of thousands", 20000, 60000,
  "Licensed German specialist hospital (internal med/oncology)", "since 1987",
  10, 13, 9, 11, 10, "Landlocked Bavaria - Adriatic via Trieste ~400 km",
  "Licensed inpatient hospital; hyperthermia is a real adjunct in specific settings",
  "EXPERIMENTAL; IPT low-dose chemo & 'integrative' package lack robust efficacy evidence")
C("Stem Cell Institute (Panama)", SC, "Panama City", "Panama", "https://www.cellmedicine.com/",
  "UC-MSC 'Golden Cells' IV/local for autism, MS, OA, anti-aging", "~$20,000-30,000+ per protocol", 20000, 30000,
  "Panama-operated; affiliated Medistem lab; not FDA-approved", "since ~2007",
  8, 13, 9, 12, 9, "Pacific - Panama Canal / Balboa port (sailing fit)",
  "One of the most prominent stem-cell destinations; some pilot work; higher profile than most",
  "UNPROVEN; broad disease claims exceed proven indications; FDA/ISSCR warn against this marketing")
C("Hallwang Clinic", CA, "Dornstetten", "Germany", "https://www.hallwang-clinic.com/en/",
  "'Personalized' experimental immunotherapy, off-label checkpoint inhibitors, hyperthermia", ">$120,000; ~80% deposit up-front", 120000, 250000,
  "German private clinic license; treatments largely off-label", "since ~2011",
  8, 11, 6, 10, 8, "Inland Black Forest - Mediterranean (Genoa) ~450 km",
  "Uses some real drug classes administered by licensed physicians",
  "EXPERIMENTAL; no published survival data; extreme cost; largest drain on UK cancer crowdfunding")
C("Verita Life (Bangkok)", CA, "Bangkok", "Thailand", "https://veritalife.com/",
  "Multimodal integrative oncology - hyperthermia, immuno, metabolic", "Multi-week packages tens of thousands", 20000, 60000,
  "Private integrative clinic group", "first clinic 2014",
  6, 10, 7, 9, 7, "Gulf of Thailand via Laem Chabang ~100 km",
  "Organized international group; hyperthermia has limited evidence",
  "EXPERIMENTAL; core 'integrative' package lacks controlled-trial efficacy; no published outcomes")
C("DVC Stem", SC, "George Town", "Cayman Islands", "https://www.dvcstem.com/",
  "IV allogeneic UC-MSC (300M+ cells) for anti-aging, autoimmune, neuro", "~$25,000 (up to ~$45,000)", 25000, 45000,
  "Cayman 'IRB-approved' protocol; cells from a US cGMP lab", "since ~2016",
  7, 12, 9, 10, 9, "Caribbean - Seven Mile Beach / George Town port (sailing fit)",
  "cGMP-sourced cells; markets an ethics/IRB framework",
  "UNPROVEN; scientists (P. Knoepfler) flag it as marketing unproven therapy; 'IRB' is not efficacy")
C("ProgenCell - Stem Cell Therapies", SC, "Tijuana", "Mexico", "https://progencell.com/",
  "Autologous & allogeneic MSC for MSK, autoimmune, metabolic", "Varies by protocol (on request)", 8000, 30000,
  "COFEPRIS-compliant (MX regulator); not FDA-approved", "since 2008",
  7, 12, 8, 11, 9, "Pacific - near San Diego border",
  "Regulator-registered; long operating history; near US border",
  "UNPROVEN; broad indications without controlled-trial support; FDA safety concerns apply")
C("Hope4Cancer", CA, "Tijuana", "Mexico", "https://hope4cancer.com/",
  "'Non-toxic integrative' - sonodynamic/PDT, IV vitamin C, ozone, coffee enemas", "~$45,000-60,000 for 3-week program", 45000, 60000,
  "Licensed Mexican (COFEPRIS) non-surgical hospital", "since 2000",
  4, 9, 6, 10, 5, "Pacific - Playas de Tijuana on the coast",
  "Licensed facility; inpatient care",
  "DISCREDITED APPROACH; core modalities have zero credible cancer efficacy; funded via crowdfunding of desperate patients")
C("GARM Clinic (Roatan)", SC, "Roatan", "Honduras", "https://www.garmclinic.com/",
  "Adipose (fat-derived) stem cells, 'biocellular' regenerative", "On request", 10000, 40000,
  "Honduran clinic; US board-certified surgeons on staff", "2010s",
  6, 11, 7, 9, 8, "Caribbean island - Parrot Tree marina (sailing fit)",
  "US-trained surgeons; established island facility",
  "UNPROVEN; testimonial-driven marketing; offshore to avoid FDA; also a Minicircle gene-therapy site")
C("DNA Health & Wellness (Dubai)", G, "Dubai", "UAE", "https://dnahealthcorp.com/",
  "Longevity IV - NAD+, ozone, peptides, exosomes, HBOT", "On request", 3000, 20000,
  "UAE-licensed wellness clinic", "unknown",
  8, 12, 9, 9, 9, "Persian Gulf - Dubai marinas (sailing fit)",
  "Physician-staffed licensed clinic in a high-end medical-tourism hub",
  "UNPROVEN; NAD+/ozone/exosome anti-aging claims unproven; ozone & exosomes drew FDA alerts")
C("Immunity Therapy Center", CA, "Tijuana", "Mexico", "https://www.immunitytherapycenter.com/",
  "'Natural/alternative' cancer program - IV, ozone/oxygen, off-label", "3-week from ~$18,995 (inpatient ~$30,000)", 18995, 30000,
  "Licensed Mexican clinic (COFEPRIS)", "since ~2007",
  4, 9, 7, 8, 5, "Pacific - Tijuana coast",
  "Licensed; more affordable than German clinics",
  "HIGH RISK; positions unproven therapies as alternatives to chemo/radiation - real danger of forgoing effective care")
C("Oasis of Hope Hospital", CA, "Tijuana", "Mexico", "https://www.oasisofhope.com/",
  "Faith-based integrative oncology - Laetrile/'B17', IPT, ozone, vitamin C", "~$20,000-40,000 for ~3-week program", 20000, 40000,
  "Licensed Mexican hospital; long-running", "since 1963",
  2, 9, 6, 11, 4, "Pacific - Playas ~10 km",
  "Longevity and licensure; offers some conventional care alongside",
  "DISCREDITED; built on Laetrile - NCI/FDA confirm no anticancer activity + cyanide-poisoning deaths")
C("CMN Hospital (Alt. Cancer)", CA, "San Luis Rio Colorado", "Mexico", "https://www.cmnalternativecancertreatment.com/",
  "Alternative/integrative protocols for advanced cancers", "~$25,000-45,000 (on request)", 25000, 45000,
  "Licensed full-service Mexican hospital", "unknown",
  4, 10, 5, 8, 5, "Sea of Cortez via Puerto Penasco ~210 km",
  "Full-service licensed hospital setting",
  "HIGH RISK; unproven 'alternative cancer' protocols marketed to advanced/terminal patients; no outcome data")
C("Minicircle (Prospera)", G, "Roatan", "Honduras", "https://minicircle.io/",
  "Non-viral plasmid gene therapy - Follistatin for muscle/'epigenetic age'", "~$25,000 (follistatin)", 25000, 25000,
  "None - states therapies are investigational, not FDA-reviewed", "since ~2020",
  5, 7, 8, 6, 5, "Caribbean island (Prospera zone)",
  "Oddly transparent that it is investigational; high-profile backers",
  "ETHICALLY CONTESTED; single-arm company data; scientists warn follistatin could risk cancer/liver failure; regulatory arbitrage")
C("Bio-Medical Center (Hoxsey)", CA, "Tijuana", "Mexico", "https://www.hoxseybiomedical.com/",
  "Hoxsey herbal 'tonic', escharotic pastes, diet, chelation", "~$4,000-5,000 initial + supplements", 4000, 8000,
  "Licensed Mexican clinic; therapy FDA-banned in US", "since 1963",
  1, 7, 6, 11, 3, "Pacific - Tijuana coast",
  "Historical continuity only",
  "DISCREDITED QUACKERY; Hoxsey FDA-banned 1960 as 'worthless'; escharotic pastes cause tissue damage")
C("Ambrosia ('young plasma') - cautionary case", G, "Naples FL", "USA", "https://en.wikipedia.org/wiki/Ambrosia_(company)",
  "Young-donor plasma transfusion to 'reverse aging' (DEFUNCT)", "Was $8,000/L; halted 2019", 8000, 12000,
  "None meaningful", "2016-2019 (defunct)",
  2, 4, 5, 4, 3, "N/A (defunct)",
  "Included as the canonical 'young plasma' cautionary tale",
  "FDA-WARNED 2019: no proven benefit + infectious/cardiovascular risks; company halted treatments",
  defunct=True)

# ---- emit ----
rows.sort(key=lambda r: (-r["trust_score"], r["category"]))
with open(os.path.join(OUT, "clinics.json"), "w", encoding="utf-8") as f:
    json.dump({"generated": "2026-08-02", "count": len(rows),
               "rubric": {
                   "pillars": {"evidence": 30, "accreditation": 25, "transparency": 15,
                               "track_record": 15, "safety": 15},
                   "tiers": [{"min": t[0], "letter": t[1], "label": t[2], "color": t[3]} for t in TIERS]},
               "clinics": rows}, f, indent=2, ensure_ascii=False)

cols = ["name","category","city","country","lat","lng","website","specialty","price",
        "price_low","price_high","accreditations","established","trust_score","tier",
        "tier_label","coast","trust_signals","red_flags","defunct"]
with open(os.path.join(OUT, "clinics.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(cols + ["evidence","accreditation","transparency","track_record","safety"])
    for r in rows:
        s = r["scores"]
        w.writerow([r[c] for c in cols] + [s["evidence"],s["accreditation"],s["transparency"],s["track_record"],s["safety"]])

from collections import Counter
cat = Counter(r["category"] for r in rows); tier = Counter(r["tier"] for r in rows)
print("TOTAL:", len(rows))
print("BY CATEGORY:", dict(cat))
print("BY TIER:", dict(sorted(tier.items())))
print("COUNTRIES:", len(set(r["country"] for r in rows)))
print("score range:", min(r["trust_score"] for r in rows), "-", max(r["trust_score"] for r in rows))

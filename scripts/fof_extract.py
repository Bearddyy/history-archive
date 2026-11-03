#!/usr/bin/env python3
"""Re-derive raw/S-fof-abstracts/inbounds.json from the fetched abstract pages.

Bound (agreed 2026-10-26): Stanstead Abbots, Thele, Hunsdon, Ware/Wareside,
Widford, Roydon/Easneye, Eastwick, Amwell (Gt & Lt), Rye House/Meads,
St Margarets. Stansted MOUNTFITCHET is a different place and is EXCLUDED.
"""
import re, html, json, glob, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "..", "raw", "S-fof-abstracts")
PAGES = os.path.join(BASE, "abstracts")

BOUND = [
    ("P-stanstead-abbots", r"stanstede(?:'? )?(?:abb\w*|abbot)|stansted(?:'? )?abb\w*|\bstanstede\b|\bstansted\b"),
    ("P-thele",            r"\bthele\b"),
    ("P-hunsdon",          r"hunesdon|onesdon|onnesdon|odesdon|honsdon|hunsdon|unesdon"),
    ("P-ware",             r"\bware\b|\bwara\b"),
    ("P-widford",          r"wydeford|widford"),
    ("P-roydon",           r"roydon|roidon"),
    ("P-eastwick",         r"eastwick|estwike|estwick"),
    ("P-amwell",           r"amewell|amuelle|amwell"),
    ("P-rye-house",        r"\braurethe\b|\breylegh\b|\bryeh\b"),
    ("P-easneye",          r"easney|esenhe"),
    ("P-st-margarets",     r"stanstede\W?thele"),
]
MOUNTFIT = re.compile(r"moun\w*fich|montf")
MONTHS = dict(january=1, february=2, march=3, april=4, may=5, june=6, july=7,
              august=8, september=9, october=10, november=11, december=12)

def clean(t):
    return re.sub(r"\s+", " ", t).strip().rstrip(".") if t else None

def main():
    recs = {}
    for f in sorted(glob.glob(os.path.join(PAGES, "*"))):
        raw = open(f, encoding="latin-1", errors="ignore").read()
        txt = re.sub(r"<[^>]+>", " ", html.unescape(raw)).replace("&nbsp;", " ")
        txt = re.sub(r"\s+", " ", txt)
        for m in re.finditer(
            r"(CP 25/1/[\d/]+, number (\d+))\.(.+?)(?=CP 25/1/[\d/]+, number \d+\.|Some notes|Introduction|$)",
            txt):
            ref, body = m.group(1), m.group(3)
            if ref in recs or "Parties:" not in body:
                continue
            g = lambda pat: clean(re.search(pat, body).group(1)) if re.search(pat, body) else None
            date = g(r"Date:\s*(.*?)\.\s*Parties:")
            if not date:
                continue
            ym = re.search(r"(\d{4})\]|\[(\d{4})", date)
            year = int(ym.group(1) or ym.group(2)) if ym else None
            dm = re.search(r"\[(\d{1,2})\s+([a-z]+)", date)
            iso = None
            if year and dm and dm.group(2) in MONTHS:
                iso = "%d-%02d-%02d" % (year, MONTHS[dm.group(2)], int(dm.group(1)))
            elif year:
                iso = str(year)
            pm = re.search(r"Property:\s*(.*?)\.\s*Action:", body)
            prop = clean(pm.group(1)) if pm else ""
            hits = sorted({pid for pid, pat in BOUND if re.search(pat, prop.lower())})
            if not hits or MOUNTFIT.search(prop.lower()):
                continue
            recs[ref] = dict(
                ref=ref, year=year, date_iso=iso, date=date,
                parties=g(r"Parties:\s*(.*?)\.\s*Property:"),
                property=prop,
                action=g(r"Action:\s*(.*?)\.\s*Agreement:"),
                agreement=g(r"Agreement:\s*(.*?)(?:\s+(?:And besides|For this|Warranty:)|\s+Standardised|$)"),
                consideration=g(r"For this:?\s*(.*?)\.\s+(?:Standardised|$)"),
                standardised=g(r"Standardised forms of names\..*?Persons:\s*(.*?)Places:"),
                places=hits)
    out = os.path.join(BASE, "inbounds.json")
    json.dump(list(recs.values()), open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"{len(recs)} in-bounds fines -> {out}")

if __name__ == "__main__":
    main()

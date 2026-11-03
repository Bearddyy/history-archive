#!/usr/bin/env python3
"""Historical-research knowledge-base query helper (stdlib only)."""
import argparse, json, sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

def load(name):
    p = DATA / name
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []

def cmd_variants(_):
    seen = {}
    for f in ("places.json", "people.json"):
        for e in load(f):
            if str(e.get("status","")).startswith("merged-into"):
                continue
            name = e.get("name","?")
            for v in e.get("variants", []):
                sp = v.get("spelling","")
                if sp and sp not in seen:
                    seen[sp] = name
            if name not in seen:
                seen[name] = name
    for sp, name in sorted(seen.items()):
        print(f"{sp}\t# {name}")

def cmd_show(args):
    for f in ("places.json","people.json","events.json","sources.json"):
        for e in load(f):
            if e.get("id") == args.id:
                print(json.dumps(e, indent=2, ensure_ascii=False))
                return
    sys.exit(f"id not found: {args.id}")

def cmd_grep(args):
    q = args.term.lower()
    for f in ("places.json","people.json","events.json","sources.json"):
        for e in load(f):
            blob = json.dumps(e, ensure_ascii=False).lower()
            if q in blob:
                label = e.get("name") or e.get("title") or e.get("type")
                print(f"{e['id']}  [{f}]  {label}")

def cmd_events(args):
    evs = load("events.json")
    places = {p["id"]: p for p in load("places.json")}
    for ev in sorted(evs, key=lambda x: x.get("year") or 0):
        if args.person and not any(p["person_id"] == args.person for p in ev.get("parties", [])):
            continue
        if args.place and not any(p["place_id"] == args.place for p in ev.get("places", [])):
            continue
        parties = "; ".join(f"{p['person_id']}:{p.get('role','?')}" for p in ev.get("parties", []))
        pls = "; ".join(p["place_id"] for p in ev.get("places", []))
        print(f"{ev.get('year','?'):>6}  {ev['id']:<28} {ev.get('type','?'):<12} "
              f"places=[{pls}] parties=[{parties}]")

def cmd_sources(_):
    for s in load("sources.json"):
        tag = "SEARCHABLE" if s.get("searchable") else "-"
        print(f"{s['id']:<28} {tag:<10} {s.get('kind','?'):<18} {s.get('title','')[:70]}")

ap = argparse.ArgumentParser()
sub = ap.add_subparsers(dest="cmd", required=True)
sub.add_parser("variants").set_defaults(fn=cmd_variants)
p = sub.add_parser("show"); p.add_argument("id"); p.set_defaults(fn=cmd_show)
p = sub.add_parser("grep"); p.add_argument("term"); p.set_defaults(fn=cmd_grep)
p = sub.add_parser("events")
p.add_argument("--person"); p.add_argument("--place"); p.set_defaults(fn=cmd_events)
sub.add_parser("sources").set_defaults(fn=cmd_sources)
args = ap.parse_args()
args.fn(args)

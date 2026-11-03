#!/usr/bin/env python3
"""Render historical-research JSON entries as human-readable Markdown.

Usage:
    python scripts/export_md.py data/places.json                # whole file
    python scripts/export_md.py data/places.json --id P-example-place
    python scripts/export_md.py data/places.json -o olives.md
    python scripts/export_md.py all                              # all four, combined

Output is self-contained: variant tables, chronological attestations with
source titles (hyperlinked where a URL exists), related events, and a
"where this comes from" footer. No dependencies beyond the stdlib.
"""
import argparse
import json
import sys
from pathlib import Path

ORDER = ["places.json", "people.json", "events.json", "sources.json"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class Ctx:
    """Holds all datasets so entities can cross-reference each other."""

    def __init__(self, datadir: Path):
        self.files = {}
        for name in ORDER:
            p = datadir / name
            self.files[name] = load_json(p) if p.exists() else []
        self.sources = {s.get("id"): s for s in self.files.get("sources.json", [])}
        self.people = {s.get("id"): s for s in self.files.get("people.json", [])}
        self.places = {s.get("id"): s for s in self.files.get("places.json", [])}
        self.events = {s.get("id"): s for s in self.files.get("events.json", [])}
        self.used_sources = []          # ordered, for footers

    def entity_name(self, eid):
        for table in (self.places, self.people, self.events):
            if eid in table:
                return table[eid].get("name") or table[eid].get("id")
        return eid

    def cite(self, sid):
        """Render a source id as a readable citation, remembering it for the footer."""
        s = self.sources.get(sid)
        if not s:
            return f"`{sid}`"
        if s not in self.used_sources:
            self.used_sources.append(s)
        title = s.get("title", sid)
        url = s.get("url")
        label = f"[{title}]({url})" if url and "{" not in url else title
        status = s.get("status")
        if status == "referenced-only":
            label += " *(cited by others — not yet obtained)*"
        elif status == "unavailable":
            label += " *(not yet accessible)*"
        return label

    def provenance(self, item):
        """'via X, quoting Y' chain for a variant/attestation dict."""
        bits = []
        if item.get("via"):
            bits.append(f"via {self.cite(item['via'])}")
        if item.get("cites"):
            bits.append(f"quoting {self.cite(item['cites'])}")
        return f" ({'; '.join(bits)})" if bits else ""


def fmt_year(e):
    return str(e.get("year") or (e.get("date") or "")[:4] or "?")


def variants_table(variants):
    if not variants:
        return "*(no spelling variants recorded yet)*"
    lines = ["| Spelling as found | Year | Where it comes from |",
             "|---|---|---|"]
    for v in variants:
        yr = v.get("year", "—")
        note = f" — {v['note']}" if v.get("note") else ""
        lines.append(f"| **{v.get('spelling','?')}** | {yr} | {Ctx_cite(v.get('src'))}{(_ctx.provenance(v) if _ctx else '')}{note} |")
    return "\n".join(lines)


# Cite is needed inside helpers; a module-level hook set by render_* funcs.
_ctx = None
def Ctx_cite(sid):
    return _ctx.cite(sid) if sid else "—"


def attestation_list(atts):
    if not atts:
        return "*(no dated attestations recorded yet)*"
    out = []
    for a in sorted(atts, key=lambda x: x.get("year") or 0):
        conf = f" _({a['confidence']})_" if a.get("confidence") else ""
        who = ""
        ids = [p for p in a.get("person_ids", []) if p in (_ctx.people or {}) or True]
        if a.get("person_ids"):
            names = ", ".join(_ctx.entity_name(p) for p in a["person_ids"])
            who = f" — people: {names}"
        ev = ""
        if a.get("event_ids"):
            ev = " — events: " + ", ".join(a["event_ids"])
        prov = _ctx.provenance(a) if _ctx else ""
        out.append(f"- **{fmt_year(a)}** — {a.get('text','')}{who}{ev}{prov} {conf}\n"
                   f"  Source: {Ctx_cite(a.get('src'))}")
    return "\n".join(out)


def etymology_block(et):
    if not et:
        return None
    els = []
    for e in et.get("elements", []):
        els.append(f"`{e.get('string','?')}` ({e.get('lang','?')}) — {e.get('gloss','?')}")
    body = "\n".join(f"- {e}" for e in els) or "- *(none recorded)*"
    status = {"attested": "attested", "proposed": "proposed (not proven)",
              "open": "unresolved"}.get(et.get("status"), et.get("status", "?"))
    note = f"\n\n_Note: {et['note']}_" if et.get("note") else ""
    return f"**Etymology** — status: {status}\n\n{body}{note}"


def related_events(ent_id):
    rel = []
    for ev in _ctx.events.values():
        hit = any(p.get("person_id") == ent_id for p in ev.get("parties", [])) or \
              any(p.get("place_id") == ent_id for p in ev.get("places", []))
        if hit:
            rel.append(ev)
    if not rel:
        return None
    lines = []
    for ev in sorted(rel, key=lambda x: x.get("year") or 0):
        def pname(p):
            if p.get("person_id"):
                return f"{_ctx.entity_name(p['person_id'])} ({p.get('role','?')})"
            return f"{p.get('name_raw','?')} ({p.get('role','?')}, identity unresolved)"
        parties = ", ".join(pname(p) for p in ev.get("parties", []))
        places = ", ".join(
            _ctx.entity_name(p["place_id"]) for p in ev.get("places", []))
        bits = [f"- **{ev.get('date') or fmt_year(ev)}** — _{ev.get('type','?')}_"]
        if parties:
            bits.append(f"parties: {parties}")
        if places:
            bits.append(f"property: {places}")
        if ev.get("consideration"):
            bits.append(f"consideration: {ev['consideration']}")
        bits.append(f"source: {Ctx_cite(ev.get('src'))}")
        lines.append(" · ".join(bits))
    return "\n".join(lines)


def render_place(p):
    _ctx.used_sources = []
    head = [f"## {p.get('name')}"]
    meta = " · ".join(x for x in [
        p.get("type"),
        f"parish: {p['parish']}" if p.get("parish") else None,
        f"grid ref {p['ngr']}" if p.get("ngr") else None,
        f"status: {p['status']}" if p.get("status") else None] if x)
    if meta:
        head.append(f"_{meta}_")
    if p.get("confidence"):
        head.append(f"_Evidence status: {p['confidence']}_")
    body = [p.get("description") or ""]
    et = etymology_block(p.get("etymology"))
    if et:
        body += ["", et]
    body += ["", "**Name variants found**", "", variants_table(p.get("variants"))]
    body += ["", "**Attestations (chronological)**", "", attestation_list(p.get("attestations"))]
    rel = related_events(p.get("id"))
    if rel:
        body += ["", "**Transactions involving this place**", "", rel]
    subs = [i for i in p.get("member_ids", []) if i != p.get("id")]
    if subs:
        body += ["", "**Associated places**: " + ", ".join(
            _ctx.entity_name(i) for i in subs)]
    return "\n".join(head) + "\n\n" + "\n".join(body) + "\n\n---\n", list(_ctx.used_sources)


def render_person(p):
    _ctx.used_sources = []
    head = [f"## {p.get('name')}"]
    meta = " · ".join(x for x in [
        p.get("role"),
        f"floruit: {p['fl']}" if p.get("fl") else None] if x)
    if meta:
        head.append(f"_{meta}_")
    body = [p.get("description") or ""]
    if p.get("variants"):
        body += ["", "**Name variants found**", "", variants_table(p.get("variants"))]
    body += ["", "**Attestations (chronological)**", "", attestation_list(p.get("attestations"))]
    rel = related_events(p.get("id"))
    if rel:
        body += ["", "**Transactions involving this person**", "", rel]
    if p.get("relations"):
        body += ["", "**Relations**: " + "; ".join(
            f"{r.get('type','?')} of {_ctx.entity_name(r['to_id'])}"
            for r in p["relations"])]
    return "\n".join(head) + "\n\n" + "\n".join(body) + "\n\n---\n", list(_ctx.used_sources)


def render_event(e):
    _ctx.used_sources = []
    head = [f"## {e.get('date') or fmt_year(e)} — {e.get('type','event')}",
            f"_{e.get('id')}_"]
    lines = []
    if e.get("property"):
        lines.append(f"**Property:** {e['property']}")
    if e.get("parties"):
        lines.append("**Parties:**")
        for pt in e["parties"]:
            if pt.get("person_id"):
                lines.append(f"- {_ctx.entity_name(pt['person_id'])} — _{pt.get('role','?')}_")
            else:
                lines.append(f"- {pt.get('name_raw','?')} — _{pt.get('role','?')}_ (identity unresolved — generic medieval forename)")
    if e.get("places"):
        lines.append("**Places:**")
        for pl in e["places"]:
            lines.append(f"- {_ctx.entity_name(pl['place_id'])} — _{pl.get('role','?')}_")
    if e.get("consideration"):
        lines.append(f"**Consideration:** {e['consideration']}")
    if e.get("tenure"):
        lines.append(f"**Tenure:** {e['tenure']}")
    if e.get("quote"):
        lines.append(f"> {e['quote']}")
    lines.append(f"**Source:** {Ctx_cite(e.get('src'))}")
    return "\n".join(head) + "\n\n" + "\n".join(lines) + "\n\n---\n", list(_ctx.used_sources)


def render_source(s):
    head = [f"## {s.get('title')}"]
    lines = [f"_{s.get('id')}_ · kind: {s.get('kind','?')}"]
    if s.get("holder"):
        lines.append(f"**Held by:** {s['holder']}")
    if s.get("ref"):
        lines.append(f"**Reference:** {s['ref']}")
    if s.get("date"):
        lines.append(f"**Date/coverage:** {s['date']}")
    if s.get("url"):
        lines.append(f"**Link:** {s['url']}")
    if s.get("access"):
        lines.append(f"**Access:** {s['access']}")
    if s.get("searchable"):
        sc = s["searchable"]
        lines.append(f"**How to query:** method `{sc.get('method','?')}` — `{sc.get('template','(see notes)')}`")
        if sc.get("notes"):
            lines.append(f"_{sc['notes']}_")
    if s.get("notes"):
        lines.append(f"**Notes:** {s['notes']}")
    return "\n".join(head) + "\n\n" + "\n".join(lines) + "\n\n---\n", []


RENDERERS = {
    "places.json": render_place,
    "people.json": render_person,
    "events.json": render_event,
    "sources.json": render_source,
}


def export(datadir: Path, filename: str, ent_id=None, title=None):
    global _ctx
    _ctx = Ctx(datadir)
    entries = _ctx.files.get(filename, [])
    if not entries:
        sys.exit(f"no entries found for {filename} in {datadir}")
    if ent_id:
        entries = [e for e in entries if e.get("id") == ent_id]
        if not entries:
            sys.exit(f"id {ent_id!r} not found in {filename}")
    renderer = RENDERERS.get(filename, render_source)

    all_sources = []
    out = [title or f"# {Path(filename).stem.capitalize()} — heritage notes"]
    if not ent_id and len(entries) > 1:
        names = ", ".join(e.get("name") or e.get("id") for e in entries)
        out.append(f"_Contents: {names}_" if len(names) < 600
                   else f"_Contents: {len(entries)} entries_")
    for e in entries:
        md, used = renderer(e)
        out.append(md)
        for s in used:
            if s not in all_sources:
                all_sources.append(s)
    if all_sources:
        out.append("\n## Where this comes from\n")
        for s in all_sources:
            url = s.get("url")
            label = s.get("title", s.get("id"))
            link = f"[{label}]({url})" if url and "{" not in url else label
            extra = f" — {s['holder']}" if s.get("holder") else ""
            st = {"referenced-only": " — *not yet obtained, cited second-hand*",
                  "unavailable": " — *not yet accessible*"}.get(s.get("status"), "")
            out.append(f"- {link}{extra}{st}")
    out.append("\n---\n_Compiled from the historical-research evidence database._")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="JSON data file (e.g. data/places.json) or 'all'")
    ap.add_argument("--id", help="export a single entry id (e.g. P-example-place)")
    ap.add_argument("-o", "--out", help="write to file instead of stdout")
    ap.add_argument("--data-dir", help="override the data directory")
    args = ap.parse_args()

    p = Path(args.path)
    if args.path == "all":
        datadir = Path(args.data_dir) if args.data_dir else Path(__file__).resolve().parent.parent / "data"
        parts = ["# Heritage research notes\n",
                 "_A structured record of places, people, events, and the sources that document them._\n\n---\n"]
        for name in ["places.json", "people.json", "events.json"]:
            if (datadir / name).exists():
                parts.append(export(datadir, name))
        text = "\n".join(parts)
    else:
        if not p.exists():
            sys.exit(f"file not found: {p}")
        datadir = Path(args.data_dir) if args.data_dir else p.parent
        text = export(datadir, p.name, args.id)
    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"wrote {args.out} ({len(text)} chars)")
    else:
        print(text)


if __name__ == "__main__":
    main()

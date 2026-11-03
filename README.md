# history-archive

Structured knowledge base for local-historical research around
**Stanstead Abbots / Stanstead St Margarets (with Hailey) / Hunsdon**, Hertfordshire —
field names, farms, families, and the documentary trail between them.

## What this repo is

A git-tracked, agent-friendly archive of **research methods and documentation**.
The machine-queryable JSON index in `data/` and downloaded/source material in
`raw/` are local working data and are intentionally excluded from Git because
they can grow substantially. `docs/` holds narrative notes. The design goal:
when a *new* source repository is found (e.g. Feet of Fines at
medievalgenealogy.org.uk, an online tithe database, a printed Cal. Inq. p.m.), you run
every indexed name through the new source and merge hits back into the index with one
update pass — see `docs/WORKFLOW.md`.

## Layout

```
archive-kb/
├── data/
│   └── schema.md          # field-level definitions; local JSON files are gitignored
├── raw/                   # local source downloads/transcriptions (gitignored)
├── docs/
│   ├── WORKFLOW.md        # how to ingest a new source; query recipes
│   ├── research-notes.md  # narrative findings (Slap Ladies, Olives Farm, Briggens…)
│   └── DESIGN.md          # rationale, alternatives considered, future ideas
└── scripts/
    └── kb.py              # query tool: name lookup, variant expansion, source dump
```

## Local research data

The files `data/events.json`, `data/people.json`, `data/places.json`, and
`data/sources.json`, along with everything under `raw/`, are deliberately not
stored in this repository. They remain on your machine, but a fresh clone will
not include them. Create or restore the JSON files using the definitions in
[`data/schema.md`](data/schema.md) before running the KB query or export scripts.
Keep an independent backup of this local research data.

## Data model (short version)

- **Source** (`S-*`): anything a name can be found *in* — an archive bundle
  (HALS `DE/B1630/T41`), a search repository (Feet of Fines abstracts), a book
  (VCH Herts III), a website. Sources have a `searchable` block recording *how* to
  query them programmatically, so future agents can re-run all names against them.
- **Place / Person** (`P-*`, `PPL-*`): a canonical entity with a description, an
  array of **variants** (each with the spelling and the year/source it was seen in),
  and an array of **attestations** (who/what/where, cited to a source id).
- **Event** (`E-*`): a dated transaction linking people to places
  (transfer, purchase, bequest, conveyance) — the deeds/title-tracking layer.

Full definitions: [`data/schema.md`](data/schema.md). The JSON records described
there are local-only and are not included in Git.

## Tools

`scripts/kb.py` (stdlib Python 3):

```
python scripts/kb.py variants            # every variant string — paste into a new source's search box
python scripts/kb.py show P-olive-farm   # one entity, fully expanded with citations
python scripts/kb.py grep briggen        # substring across names/variants/descriptions
python scripts/kb.py events --person PPL-spark
python scripts/kb.py sources --searchable  # repositories that can be re-queried
```

Related external tooling: `tna-search` CLI (separate repo
`C:\Users\Byrne\tna-discovery-search`) for the UK National Archives Discovery API,
rate-limited + cached.

## Conventions

- IDs are stable forever; never renumber. Deprecate with `"status": "merged-into: X"`.
- Every fact carries `src` → a source id, and quotes **exact spellings** in variants.
- Dates: ISO where possible (`1343-10-13`), else the regnal/original string plus
  `year` for sorting.
- Uncertainty is a field, not a vibe: `confidence` ∈ {attested, inferred, tradition}.

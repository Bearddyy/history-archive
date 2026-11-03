# History Archive

A reusable, source-driven toolkit and schema for historical research about
places, people, and the documentary evidence connecting them. The notes in this
repository document one current case study; the data model and workflow are not
limited to that location or its record types.

## What this repo is

This repository tracks the research methods, schema, scripts, and documentation.
The machine-queryable JSON index in `data/` and downloaded/source material in
`raw/` are local working data and are intentionally excluded from Git because
they can grow substantially. For each research area, register sources, search
them systematically for known names and variants, and cite any findings back
to the source. See [`docs/WORKFLOW.md`](docs/WORKFLOW.md).

## Layout

```
history-archive/
├── data/
│   └── schema.md          # field-level definitions; local JSON files are gitignored
├── raw/                   # local source downloads/transcriptions (gitignored)
├── docs/
│   ├── WORKFLOW.md        # reusable source-ingestion workflow
│   ├── research-notes.md  # current case-study narrative and open questions
│   └── DESIGN.md          # rationale, alternatives considered, future ideas
└── scripts/
    └── kb.py              # query tool: name lookup, variant expansion, source dump
```

`scripts/fof_extract.py` is a source-specific parser for the current case study,
not a general-purpose ingestion tool.

## Local research data

The files `data/events.json`, `data/people.json`, `data/places.json`, and
`data/sources.json`, along with everything under `raw/`, are deliberately not
stored in this repository. They remain on your machine, but a fresh clone will
not include them. Create or restore the JSON files using the definitions in
[`data/schema.md`](data/schema.md) before running the KB query or export scripts.
Keep an independent backup of this local research data.

## Data model (short version)

- **Source** (`S-*`): anything an entity or fact can be found in — an archive
  item, database, book, map, website, or other source. Sources can have a
  `searchable` block recording how to query them programmatically.
- **Place / Person** (`P-*`, `PPL-*`): a canonical entity with a description, an
  array of **variants** (each with the spelling and the year/source it was seen in),
  and an array of **attestations** (who/what/where, cited to a source id).
- **Event** (`E-*`): a dated transaction linking people to places
  (for example a transfer, purchase, bequest, or other documented event).

Full definitions: [`data/schema.md`](data/schema.md). The JSON records described
there are local-only and are not included in Git.

## Tools

`scripts/kb.py` (stdlib Python 3):

```
python scripts/kb.py variants            # every variant string — paste into a new source's search box
python scripts/kb.py show P-example      # one entity, fully expanded with citations
python scripts/kb.py grep example        # substring across names/variants/descriptions
python scripts/kb.py events --person PPL-example
python scripts/kb.py sources --searchable  # repositories that can be re-queried
```

External search tools and access instructions are specific to each source; keep
them in the corresponding source record or case-study notes.

## Conventions

- IDs are stable forever; never renumber. Deprecate with `"status": "merged-into: X"`.
- Every fact carries `src` → a source id, and quotes **exact spellings** in variants.
- Dates: ISO where possible (`1343-10-13`), else the regnal/original string plus
  `year` for sorting.
- Uncertainty is a field, not a vibe: `confidence` ∈ {attested, inferred, tradition}.

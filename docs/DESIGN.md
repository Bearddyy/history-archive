# Design notes & open ideas

## Why JSON (decided 2026-10-26)
Quote-heavy records favour YAML ergonomics, but the KB is written mostly by
agents, and YAML's failure mode is *silent reinterpretation* (`no`→False,
bare dates→datetime, unquoted `&`/`*` nodes) — unacceptable for an evidence
trail. JSON either parses or hard-fails. Mitigation: if hand-writing becomes
painful, add an ingest shim accepting Markdown/YAML notes → normalise to
strict JSON on commit; stored form stays JSON.

SQLite or a graph DB can be a *derived view* (export script) if the corpus
outgrows flat files; JSON stays source of truth.

## Open ideas / TODO
- `kb.py rewire` — mechanical id-merge rewriting.
- Sweep runner: read `S-*.searchable`, replay `kb.py variants` output, write a
  hits CSV for triage (respect each source's access notes).
- Scans/photos: `scans/` convention (probably gitignored, synced separately),
  referenced from source `notes`.
- A person disambiguation policy per century ("John Olive I/II") — currently
  by `-1`/`-2` suffix, first-attested year ordering.
- Consider a `P-*` `tithe_plot` field once IR 29/15/90 is transcribed — plots
  244/287/288/331/332 are the spine connecting the friend's email to documents.
- Geodata: NGRs are stored; a GeoJSON export (derived) would let QGIS view the
  field system over 1898-1914 OS maps when more plots are pinned.

## Sensitivity
Nothing here is personal data of living persons. If census transcription adds
named individuals born <100 yrs ago, keep those files in `raw/` (gitignored)
until out of the data-protection window.

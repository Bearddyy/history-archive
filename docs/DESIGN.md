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
- A consistent person-disambiguation policy for people with similar names.
- Optional location geometry and GIS exports as derived views when coordinates
  or boundaries are available.

## Current case-study ideas
- Review the person disambiguation convention (currently numbered suffixes,
  ordered by first-attested year) against other periods and name patterns.
- Consider adding a source-specific field for tithe plot references once the
  relevant schedule is fully transcribed.

## Sensitivity
Assess privacy, copyright, and access restrictions for each project and source.
Do not add sensitive personal data or restricted source material to public
version control; keep permitted local copies outside Git and follow applicable
retention and access rules.

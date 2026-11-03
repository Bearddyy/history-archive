# Workflow

## Golden rule
Every fact enters the KB through a **source**. No source → it goes in
`docs/research-notes.md` as narrative, or as `confidence: tradition` with the
book that says it.

## Ingesting a new source repository (the "Fleet of Fines pattern")

1. **Register the source** in `data/sources.json` — most importantly the
   `searchable` block: method, URL template with `{query}` placeholder, which
   fields exist, wildcards, auth/access quirks.
   The JSON index files in `data/` are local-only and gitignored; keep an
   independent backup. `data/schema.md` documents their format.
2. **Generate the probe list**:
   ```
   python scripts/kb.py variants            # all spellings, deduped
   ```
   Prefer the *earliest* variant + canonical name for each entity; try
   wildcard stems (`Brigg*`, `Stanstead`, `Olyue`/`Olive`).
3. **Run the sweep** against the new repository, one query per stem, polite
   delays. Save raw responses under `raw/<source-id>/` (gitignore is fine for
   bulk) and note in the source entry where the raw dump lives.
4. **Merge hits**: for each hit, decide which entity it belongs to, add a
   `variants[]` item (exact spelling, year, `src`) and an `attestations[]` item
   (quoted text). If it's a transaction, create an `E-*` event with typed
   parties/places instead of prose.
5. **Re-render** the human view and commit:
   ```
   python scripts/export_md.py all -o docs/ALL-NOTES.md
   git add -A && git commit -m "ingest <source-id>: +N attestations"
   ```

## Adding a document you read on paper (HALS/Kew)
1. Add its `S-hals-…` entry (shelfmark, title verbatim from the catalogue).
2. Add variant/attestation records quoting the transcript (or the calendar
   entry text, cited to the print series if you didn't see the original —
   mark `confidence` accordingly).
3. Photograph/scan → drop path in the source entry `notes` (keep images out of
   git unless small; suggest a separate `scans/` dir or cloud folder).

## Splitting/merging entities
- Two ids turn out to be one place: keep the older id, set
  `"status": "merged-into: P-x"` on the other, move its attestations across
  (they keep their own `src`).
- One id covering two people (e.g. two Thomas Blackmores): split into
  `…-1` / `…-2` and fix references (`kb.py rewire` TODO — until then, grep).

## Known access quirks (as of Oct 2026)
- HALS catalogue: Cloudflare — desktop preview pane works, curl/headless fail.
- TheGenealogist tithe collection: paywalled + Cloudflare. Tithe apportionments
  free at Kew reading room (IR 29 series).
- Feet of Fines abstracts: plain curl works; paginate with `&s=<offset+1>`.
- TNA Discovery API: use `tna-search` CLI (1 req/s, 3000/day, boot-scoped cache;
  exit code 4 = day's quota gone — stop, don't retry).
- british-history.ac.uk (VCH): plain curl works.

## Search recipes worth remembering
- Feet of fines Stanstead/Herts sweep: place=Stanstead, county=Hertfordshire →
  45 entries incl. the 1343 Olyue/Spark fine (CP 25/1/89/79 no. 274).
- TNA compound query for Briggens: `("Briggen" OR "Briggens" OR "Newgates")`
  — one query, split results locally.
- HALS wants `DP/102/27` with slashes, not `DP102/27`.

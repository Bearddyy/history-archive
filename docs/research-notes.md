# Research notes (narrative)

These notes record the current Hertfordshire case study and are not a general
research template.

Structured claims live in `data/*.json`; this file is for the story-in-progress,
dead ends, and reasoning that isn't yet an attestation. Rendered views of the
structured data go to `ALL-NOTES.md` (generated — do not hand-edit).

## Olives Farm question (Oct 2026)
- NHLE/HER/RCHM tradition: "John Olive obtained land in the parish in 1344" —
  single source-chain (RCHM 1911 → listing → HER), treat as one tradition.
- Independent: CP 25/1/89/79 no. 274 (13 Oct 1343): John Olyue + Joan recover
  1 messuage + 15ac + 4d rent in Stanstead Abbots from William Spark + Joan,
  20 marks. This is likely *the* 1344 event; note the fine says Stanstead
  Abbots, listing says Hunsdon parish — the farm straddles (ancient boundary
  on the track), so both can be right.
- First known *house* owner: John Shelley d.1486 (holds of Waltham Abbey) —
  so house history ≠ family-name history; the name likely attached to the
  land/tenure first.
- Definitive source: Palmer 2011 unpublished farm history (HER SHT18129) via
  SALHS / M. Dymock Jan 2026 talk. Not yet obtained.
- HALS "Olive Farm" search: still pending (Cloudflare; rerun via desktop).

## Little Briggens question (Oct 2026)
- Identity chain: Nether Bredons → Newgates alias Little Briggens (1781) →
  Little Briggins (1705-1943 docs) → Gatsby house c.1895 on the site.
- Earliest name-evidence: 1696 Crowley "of Briggens"; earliest deed bundle
  DE/B1630/T41 1705-1852 (pull this first at HALS). Bredons undated in VCH.
- No Feet-of-Fines hit for Bred*/Brigg* places in Herts to 1509 — earlier
  attestations must come from DE/B1630 deeds themselves or manor rolls.
- Field names surrounding it (1787, DE/Bx/T35) overlap the Slap Ladies
  landscape (Dung Field etc.) — see places.json.

## Slap Ladies / causeway (Oct 2026)
Standing question: OE *slaep/hlep* + *lad/lode* thesis (friend's email;
Gelling 1984/1992). Key refs in places.json (P-slap-ladies) and sources.json
(tithe IR 29/15/90, DE/B888/T1, DE/Ch/P5 1791 manor map, QS/E/62).
UPDATE Oct 2026: 1839 schedule digitised (S-salh-tithe-schedule) — 331 'Slap
Ladles' / 332 'Privis Lees' now attested; see ingest note below.
Caution: Millstream is an artificial leat (c.1300) — dating the *causeway* by
association with it is weak; the *name* can still be OE.

## Feet of Fines sweep (Oct 2026) — bounds agreed with user
Interest area: Stanstead Abbots, Roydon, Hunsdon, Wareside, Widford, Briggens,
Eastwick, Amwell (Gt & Lt), Rye House/Meads, Easneye, St Margarets.
Stansted MOUNTFITCHET deliberately excluded (different place, similar name).
Outcome: 43 abstract pages mirrored to raw/S-fof-abstracts/abstracts/, 81
in-bounds fines (1273-1460) parsed via scripts/fof_extract.py into 88 events;
place entities + spelling variants added for the parishes/tithings (Thele,
Amewell, Wydeford, Hunesdon etc.). Parties with generic forenames (Alice,
Joan...) are kept inline on the event as name_raw, flagged unresolved — NOT
minted as people entities (avoids 100 phantom 'Alices'). People with surnames
kept: Rokesburgh, Melleward, Blake, Morewell, Louetost, Fraunceys, Scrope,
Conyers, de Stratton, Grey (+ the Olive/Spark four already there).
Note: John Olyue querent count includes the 1343 fine itself — his '13 events'
count was inflated by spouse rows; check events list, not counter.

## 1839 tithe award schedule ingest (Oct 2026)
Digitised schedule (user's CSV, SALH_Map) registered as S-salh-tithe-schedule;
raw copy in raw/S-salh-tithe-schedule/schedule.csv. 603 plots (1-591, gap 566;
lettered sub-plots; spill-over rows = extra owners/occupiers). +54 new P-*
field entities, 76 places now carry 1839 attestations, event
E-1839-tithe-stanstead-abbots.
Headlines:
- **Slap Ladies attested**: plot 331 'Slap Ladles' (Streatfield/Allin) next to
  332 'Privis Lees' (Bigg). Friend's note had 331 = 'Cappell Lane' — wrong slot;
  Chapel Lane is not a plot name in this award. Privis Lees neighbour pairing
  now solid; Privis=Prior's still inferred (cf. P-priors-lees).
- Friend's plot guesses 287 Lucerne / 288 Warrax: 287 confirmed; 288 = house
  & garden. **Warrax is NEGATIVE in the award** — commons appear as How Field,
  Garretts Field, Dung Field, Wheelers Ley Commons. Don't grep the schedule for
  Warrax again. Ballard likewise negative.
- Estates as named units: Fillets, Bonningtons, Ollives, Lodge Farm (7
  co-owners — undivided Fielde/White/Carew/Somerville inheritance), Stanstead
  Bury, Briggins (Phelips), Warren and Halving Farms (Wilkinson). New entities
  for Bonningtons/Lodge Farm/Bury/Warren; Ollives estate plots 22-38 etc.
- Big commons quantified: Rye Mead 85 plots, How Field Common 21, Innings 19,
  Garretts 17, Wheelers Ley 16, Dung Field 13.
- Notable new names: Chaceway by Easney Park (174), Moat Wood/Moat Field at
  Fillets (5/7 — moated site, HER check?), Pogdens spans Ollives+Lodge Farm,
  Terbert Hills, Kirkshurst, Dimsdailes, Hexions, Derbyshire Lands, Joy House
  Meads, Hayley Spring (153) — Hailey-name east of the Lea?
- Acreages/rent charges NOT transcribed — if needed, they're in the award text
  (retrieval item 1 still half-open for quantities).

## Ballard's Wood — will read, NO link established (Oct 2026)
PROB 11/183/570 downloaded & transcribed (retrieval item 4 read). Robert
Ballard, Clerk, of Stanstead Abbots, will May 1640, proved 14 Jul 1642
(George Martin surrogate; administration to executor Sir Edward Bush knight).
Bequests: daughter Anne a freehold dwelling + appurtenant freehold land in
Stanstead (in tenure of one George [?]), £400 at 21/marriage; heir-son John
"all my other lands"; servant Margit Dodds £30; poor of Stansted 40s; poor of
Great [Wilbraham?] co. Cambridge 30s. Witnesses Thomas Humphrey, William
Parry. Second will on same page (Richard Willis) = different testator, loose
end.
USER CALL (agreed): the will does NOT name a wood or identify land by
abuttals, so it is NO evidence the wood is this Robert's. It only proves a
Ballard (a clerk — but note: 'Clerk' may mean clergyman OR clerk in
chancery/chancery-style literate layman) held freehold in Stanstead c.1640.
Same for the 1443 Whites-manor Ballards. Confidence path forward: the gap
1640→1873 needs an estate document naming the wood itself (DE/Bx bundle,
1858 sale particulars item 28, or the 1791/1865 maps) — name-source stays
OPEN.

## HALS 'Ballard' catalogue sweep (Oct 2026, via desktop preview pane)
Search `Ballard` = 9 pages of hits; `Ballard Stanstead` = 3 hits (all fuzzy
noise, none actually Ballard+Stanstead); `Ballard Hunsdon` = ZERO.
VERDICT: no HALS catalogue entry ties any Ballard to Stanstead Abbots or
Hunsdon. Consistent with the 1839 award negative. Do NOT re-run these two
queries expecting a hit — the catalog simply doesn't name a Stanstead Ballard.
Hits that looked tempting and are NOT ours:
- DE/P 9/1/22/8 'Ballard's house... Read Mead (Vernon-Hooker-Basill-Field-
  Dimsdale)' 1685-1720 — related place = HERTFORD St Andrews/Hertingfordbury
  (Cowper deeds); the Dimsdales there are the Hertford Quaker family, NOT our
  Dimsdailes Field. False friend, both names.
- DE/P/T186-T190 + DZ/13/Z10-11: Elizabeth/John Ballard of Cheshunt
  (chandler), Hertingfordbury 'Ballard's house' 1672-1720 — different county-
  wide family; but note this is a worked example of a house kept alive in
  catalogue titles by its family name, exactly what our Stanstead one lacks.
- DE/L/180, /200, /4496(+A): John Ballard of Hertford Heath/Amwell Heath
  (labourer) 1822-1836, Manor of Great/Little Amwell — in-area (Amwell is in
  bounds) but Amwell not Stanstead; co-parties include Matthias Gilbertson
  (namesake of our 1839 Stanstead owner Matthias Gilbertson? possible kin —
  worth ONE look at some point, low priority).
- DE/Hx/E15 1883 valuation, Hertford Heath, 'Mr Ballard' tenant, Hailey Lane —
  same warning: Hailey Lane here is at Hertford Heath, NOT our Hailey. Note
  DE/Hx is the series that also holds E812 (Warrax House, Stanstead) — worth
  browsing that series index sometime for Stanstead lots generally.
Implication: the house-name in the 1640 will has no catalogue-level carrier.
Remaining routes are OCR-side (better read of the underlined word) or a deed
reading inside the big estate bundles (DE/Bx, D/EX297/Z1) — not name search.

## Next actions (any session)
0. FoF surname sweep done Oct 2026 (S-fof-surname-sweep): Spark is a ONE-OFF in
   Herts (1343 only) — family-memory 'William Spark' must come from census/deeds,
   not medieval fines. Olive likewise thin (1411 Henkesworthe is outside bound).
   CP25/2 1509-47 published abstracts: zero in-bounds hits — don't re-run.
   Land Registry 1862 Register: dead end (Hunsdon title 3208 = blank stub).
1. HALS pull: DE/B1630/T41, DE/Bx/T35, D/EH/P17 image if reproducible.
2. TheGenealogist (subscription?) or Kew: IR 29/15/90 + IR 29/15/56 —
   transcribe plots & occupiers incl. Olive/Spark/Briggins names.
3. Email SALHS re Palmer history / Dymock talk.
4. Sweep `kb.py variants` through Land Registry 1862 register (Hunsdon titles).

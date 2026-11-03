# Data schema

All files are JSON arrays of objects. UTF-8. IDs are permanent.

## sources.json — `S-*`

| field | type | notes |
|---|---|---|
| id | str | `S-tna-ir29` etc. |
| title | str | |
| kind | enum | `archive-bundle` \| `search-repository` \| `series` \| `book` \| `web` \| `map` \| `oral` |
| holder | str? | archive holding it (HALS, TNA…) |
| ref | str? | shelfmark / call number |
| url | str? | |
| date | str? | coverage of the source itself |
| searchable | obj? | how to re-query it: `{"method":"GET","template":"https://…place={query}…","fields":["place","surname"],"wildcards":true,"notes":"…"}` — `{query}` placeholder. This is what makes "run all our names through the new source" a scriptable step. |
| access | str? | `free`, `paywalled`, `on-site`, `blocked-curl` etc. |
| status | str? | `verified` (we have seen/hold it) \| `unavailable` (exists, we lack access — paywall, not yet requested) \| `referenced-only` (we only know it exists because another source cites it; contents unverified). Default: verified. |
| cited_by | str? | for `referenced-only` sources: the source id that mentions it |
| notes | str? | |

## places.json — `P-*`

| field | type | notes |
|---|---|---|
| id | str | `P-olive-farm`, `P-dung-field` |
| name | str | canonical modern form |
| type | enum | `farm` \| `field` \| `manor` \| `house` \| `lane` \| `watercourse` \| `wood` \| `hamlet` \| `parish` \| `other` |
| parish | str? | |
| ngr | str? | grid ref |
| status | str? | `active`, `demolished`, `renamed`, `built-over` |
| description | str | what it is / what we think it is |
| etymology | obj? | `{elements:[{string,lang,gloss,source}], status: "attested"|"proposed"|"open", note}` |
| variants | list | `{spelling, year?, src, via?, cites?}` — every spelling ever seen, oldest first, each cited to a source id. |
| also_known_as | list[str]? | alias ids/strings not tied to a dated attestation |
| attestations | list | `{year?, date?, text (quote/summary), src, via?, cites?, person_ids?, place_ids?, event_ids?}` |
| confidence | enum | `attested` \| `inferred` \| `tradition` \| `unverified` |
| parent_id / member_ids | str/list? | hierarchy (farm ⊃ field) |

### Provenance fields on variants/attestations (citation chains)
- `src` (required): the source **we actually looked at** (even if that source is
  itself a blog/secondary piece).
- `via` (optional): intermediate source id when we got it second-hand through
  something we did see (e.g. we saw an article that quoted a book).
- `cites` (optional): the **underlying primary source the carrier claims**,
  which we do NOT hold — usually points at a `status: referenced-only` source.
  A fact with `cites` and no direct `src`-verification is at best `tradition`;
  mark it `unverified` if the carrier itself is unreliable.

## people.json — `PPL-*`

Same shape idea: `id, name, role?, fl (floruit), variants[{spelling,year,src}],
attestations[…], relations[{to_id, type: spouse|child|tenant_of|…}], confidence`.
One entity per *person*, not family; a family-level entity is allowed (`PPL-olive-family`)
with `member_ids` when the individual links are uncertain.

## events.json — `E-*`  (deed / title transfer tracking)

| field | type | notes |
|---|---|---|
| id | str | `E-1343-olive-spark` |
| date | str? | ISO if resolvable |
| year | int | sort key |
| type | enum | `conveyance` \| `fine`(legal) \| `purchase` \| `lease` \| `release` \| `bequest` \| `inheritance` \| `sale-estate` \| `valuation` \| `tenure` \| `other` |
| parties | list | `{person_id, role: grantor|grantee|deforiant|querent|witness|executor…}` |
| places | list | `{place_id, role: property|abutter|manor-of}` |
| consideration | str? | "20 marks of silver", "£340" |
| property | str? | "1 messuage, 15 acres…" |
| tenure | str? | freehold / copyhold of the manor of X |
| src | str | source id |
| quote | str? | exact Latin/English extract |
| confidence | enum | |

Rules of thumb
- A variant without a source is a *guess* → put it in `etymology.note`, not `variants`.
- Prefer quoting the source over paraphrasing in `attestations[].text`.
- When two P-* turn out to be the same place, keep the older id, add
  `"status": "merged-into: P-x"`, rewrite references via `scripts/kb.py rewire` (TODO).

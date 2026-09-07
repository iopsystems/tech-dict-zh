# Research refresh operations

These ledgers make periodic source discovery incremental and auditable. After initial creation, `research_runs.tsv`, `candidate_sources.tsv`, and `source_decisions.tsv` are append-only: correct an earlier fact with a later decision or superseding source record rather than rewriting history. Migrated v1.1.0 sources use the run sentinel `pre-ledger-v1.1.0`.

## Running a refresh

1. Read the last completed run and current manifest.
2. Recheck accepted snapshots and hashes, then search only the planned scope and recent interval.
3. Append every discovery to the candidate ledger before review.
4. Deduplicate mirrors under one `logical_source_id`; keep canonical and retrieval locations separate.
5. Review provenance, accessibility, translation quality, and technical value.
6. Append a decision. Promote accepted candidates into the manifest, capture a lawful snapshot, compute SHA-256, and only then extract terminology.
7. Reconcile run counts, saturation yield, and validation before marking the run complete.

Run status values: `running`, `complete`, `failed`, `interrupted`. Candidate status values: `discovered`, `pending_review`, `accepted`, `rejected`, `quarantined`, `duplicate`. Quality status values: `accepted`, `rejected`, `quarantined`. Access status values: `accessible`, `accessible_snapshot`, `challenge`, `dead`, `unknown`.

## Source precedence

Eligible evidence is `original_chinese` or substantiated `human_translated`. Original Chinese usage controls whenever it conflicts with translated wording. Human translations are fallback evidence and every such dictionary reference must end in ` (T)`; original references precede translated references. `machine_translated`, `translation_unknown`, and `originality_unknown` cannot support entries regardless of score.

## Translation-quality gate

Require an identifiable original work plus a human translator or accountable editorial/localization team. Reject or quarantine explicit machine/AI translations, unattributed apparent translations, repeated unnatural literal renderings, inconsistent central terminology, semantic errors, and fabricated distinctions. Record concrete evidence in `quality_notes`; one awkward phrase alone is not proof of machine translation.

## Quality scoring

Use the inspectable 100-point rubric:

| Dimension | Points |
| --- | ---: |
| original Chinese authorship | 25 |
| first-party technical authority | 20 |
| terminology density | 15 |
| technical depth | 15 |
| independent corroboration value | 10 |
| recency/relevance | 5 |
| stable accessibility | 5 |
| clear provenance | 5 |

Acceptance requires at least 60 points. An evidence-eligibility failure remains disqualifying at any score.

## Saturation and the 1,000-source cap

The soft target is 300–500 diverse, high-quality sources. Stop collection when the latest 50 reviewed sources yield fewer than five new terms and fewer than five meaningful variants. The hard limit is 1,000 accepted logical sources; mirrors do not increase it. At capacity, remove low-quality translations, uncertain or unattributed material, duplicates, terminology-light marketing, superseded documentation, then redundant older sources.

## WeChat handling

Canonical WeChat URLs may be staged even when direct retrieval is challenged. Never bypass a CAPTCHA or store a verification page as evidence. Prefer an official mirror, clearly attributed preserved copy, or lawful manual export as `retrieval_url`. Search snippets and article indexes are discovery evidence only. Keep a candidate pending until full content, authorship, originality, and translation method can be reviewed.

## Publishing a release

Metadata-only runs keep the current dataset version. When terms or meaningful variants change, archive the prior four root TSVs under `archived/<prior-version>/`, publish the new release at the stable root filenames, update row dates/versions, and record before/after versions in the completed run.

## Validation

Run both checks before completing a run or publishing:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_research_data.py
```

The validator checks exact schemas, IDs and foreign keys, provenance eligibility, translation labels/order, source hashes, challenge markers, the logical-source cap, and run-count reconciliation.

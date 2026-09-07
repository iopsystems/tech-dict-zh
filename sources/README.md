# Chinese observability and eBPF source corpus

This directory contains local snapshots of Chinese-language source material used to compile the terminology tables. See `source_manifest.tsv` in the repository root for URLs, project identities, retrieval dates, and selection notes.

The corpus is intentionally selective: it preserves terminology-dense documentation, blogs, reports, and white papers rather than complete source-code repositories.

## Source provenance and precedence

Beginning with dataset version `v1.1.0`, the source manifest groups material into:

- `original_chinese` / `primary`: content originally written, or maintained as parallel first-party documentation, in Chinese.
- `translated_to_chinese` / `fallback`: Chinese translations of material available in another original language.

Original Chinese usage takes precedence when the two groups disagree. Translated Chinese usage is retained when it is the only evidence or when it documents a useful contextual variant. In terminology-table `references` columns, translated sources carry a ` (T)` suffix.

The current release uses stable, unversioned filenames in the repository root; its date and version remain recorded inside each TSV. Historical releases are stored under `archived/vX.Y.Z/`.


## Research metadata

The operating procedure is in [the research README](../research/README.md). Auditable metadata is recorded in the [run ledger](../research/research_runs.tsv), [decision ledger](../research/source_decisions.tsv), and [candidate queue](../research/candidate_sources.tsv).

In `source_manifest.tsv`, `canonical_url` identifies the original publication while `retrieval_url` identifies the copy actually captured or reviewed. They may be identical. Mirrors share a `logical_source_id`; a retrieval mirror does not become a separate logical source.

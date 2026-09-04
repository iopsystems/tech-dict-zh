# Chinese observability and eBPF source corpus

This directory contains local snapshots of Chinese-language source material used to compile the terminology tables. See `source_manifest.tsv` in the repository root for URLs, project identities, retrieval dates, and selection notes.

The corpus is intentionally selective: it preserves terminology-dense documentation, blogs, reports, and white papers rather than complete source-code repositories.

## Source provenance and precedence

Beginning with dataset version `v1.1.0`, the source manifest groups material into:

- `original_chinese` / `primary`: content originally written, or maintained as parallel first-party documentation, in Chinese.
- `translated_to_chinese` / `fallback`: Chinese translations of material available in another original language.

Original Chinese usage takes precedence when the two groups disagree. Translated Chinese usage is retained when it is the only evidence or when it documents a useful contextual variant. In terminology-table `references` columns, translated sources carry a ` (T)` suffix.

The current release uses stable, unversioned filenames in the repository root; its date and version remain recorded inside each TSV. Historical releases are stored under `archived/vX.Y.Z/`.

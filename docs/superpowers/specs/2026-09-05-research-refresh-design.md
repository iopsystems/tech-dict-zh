# Research Refresh System Design

**Date:** 2026-09-05  
**Status:** Proposed for implementation  
**Current dataset:** v1.1.0

## Purpose

Create a repeatable, incremental research process that expands and refreshes the Chinese observability and eBPF terminology dictionary without rebuilding it from scratch. The process must favor terminology originating in Chinese engineering communities, identify and reject low-quality translations, retain enough provenance to audit every decision, and stop collecting when additional sources cease to improve the dictionary materially.

## Scope

The system covers:

- discovery across official websites, GitHub, Gitee, AtomGit, conference material, public WeChat accounts, and attributed mirrors;
- classification of original Chinese, human-translated, machine-translated, and uncertain material;
- source-quality review, deduplication, retention, and removal;
- incremental terminology extraction and dictionary updates;
- append-only metadata for research runs and source decisions;
- saturation measurement and a hard cap of 1,000 accepted sources;
- versioning and archival of published dictionary releases.

It does not attempt to bypass CAPTCHAs, authentication controls, robots restrictions, paywalls, or deleted-content controls. It does not treat search-result snippets or unattributed reposts as accepted terminology evidence.

## Repository Layout

The current dictionary remains available through stable root paths:

```text
popular_projects_china.tsv
source_manifest.tsv
translated_terms_zh.tsv
untranslated_terms_zh.tsv
```

Research metadata and candidate queues will use:

```text
research/
├── research_runs.tsv
├── source_decisions.tsv
├── candidate_sources.tsv
└── README.md
```

Downloaded evidence remains under `sources/`. Historical published TSV releases remain under `archived/vX.Y.Z/`.

## Source Discovery

### Discovery channels

Each research run may search:

1. Official project and business websites.
2. GitHub, Gitee, and AtomGit repositories with Chinese documentation.
3. Chinese technical conference pages, slide decks, papers, and transcripts.
4. Public WeChat accounts and canonical `mp.weixin.qq.com` article URLs.
5. Official or explicitly attributed mirrors on sites such as Tencent Cloud, InfoQ, SegmentFault, CSDN, Zhihu, or project blogs.
6. Search indexes, newsletters, and article lists used only to discover canonical or better-preserved sources.

### WeChat discovery

Direct automated retrieval of WeChat articles is not assumed to work. A WeChat source may therefore have:

- a canonical WeChat URL identifying the publication;
- a separate retrieval URL pointing to an official mirror or clearly attributed preserved copy;
- a manually exported HTML or PDF snapshot when lawful and available.

Automated CAPTCHA or verification pages must never be stored as article content. Discovery pages that contain only titles or links remain candidates until an acceptable content copy is found.

Target accounts initially include DeepFlow/云杉网络, 夜莺监控, Flashcat, HUATUO 开源技术, openEuler, 龙蜥/OpenAnolis, 滴滴技术, 阿里巴巴云原生, 阿里云开发者, 腾讯云原生, 腾讯技术工程, 百度云原生, Apache SkyWalking Chinese community, 云原生社区, and 开源社.

## Provenance Classification

Every reviewed source receives exactly one `content_origin` value:

- `original_chinese`: written in Chinese by the named author, project, company, or community; includes first-party Chinese material maintained in parallel where Chinese authorship is credible.
- `human_translated`: identifies the original work and a human translator or editorial translation process.
- `machine_translated`: explicitly machine/AI translated or contains strong, repeated machine-translation artifacts.
- `translation_unknown`: appears translated but does not identify its translator or method.
- `originality_unknown`: evidence is insufficient to determine whether the material originated in Chinese.

A repost is recorded separately as a delivery relationship and does not determine content origin. Its evidence class follows the underlying work.

## Evidence Eligibility and Precedence

Source eligibility is:

1. `original_chinese`: accepted as primary evidence when other quality checks pass.
2. `human_translated`: accepted as fallback evidence and marked `(T)` in dictionary references.
3. Verified translation of an otherwise unavailable standard: accepted as fallback evidence and marked `(T)`.
4. `machine_translated`: excluded from terminology evidence.
5. `translation_unknown`: excluded until verified.
6. `originality_unknown`: excluded until verified.

When accepted original Chinese and translated sources disagree, original Chinese usage controls the preferred dictionary counterpart. A translated rendering may remain as a contextual variant when it is meaningful and clearly labeled. When translation is the only acceptable evidence, it may support an entry, but the entry notes must make that limitation clear.

## Translation-Quality Review

Reviewers reject or quarantine sources exhibiting one or more of the following:

- explicit labels such as “机器翻译”, “AI 翻译”, or “仅供参考”;
- missing author, original URL, or publishing organization for apparently translated material;
- an unacknowledged close match to an earlier non-Chinese publication;
- repeated unnatural literal translations;
- internally inconsistent translations for central technical terms;
- obvious semantic errors, fabricated terminology, or loss of technical distinctions.

One isolated awkward phrase is not sufficient by itself to classify an entire source as machine translated. The reviewer records concrete evidence in `quality_notes`.

## Quality Scoring

Accepted-source selection considers, in descending importance:

1. Original Chinese authorship.
2. First-party technical authority.
3. Terminology density.
4. Technical depth and specificity.
5. Independent corroboration value.
6. Recency and continued relevance.
7. Stable accessibility and preservability.
8. Clear author and publication provenance.

The implementation may express this as a numeric score, but the individual dimensions must remain inspectable. A single opaque score must not replace the provenance and quality fields.

## Capacity, Saturation, and Retention

The accepted evidence corpus has a hard maximum of 1,000 logical sources and a soft target of 300–500 high-quality, diverse sources.

Collection should stop before the hard cap when the latest 50 reviewed sources yield both:

- fewer than five new dictionary terms; and
- fewer than five meaningful new translation or context variants.

Syndicated copies and mirrors of the same underlying article count as one logical source. Mirrors may remain as retrieval locations without increasing the accepted-source count.

The corpus should remain diverse across projects, businesses, communities, subject areas, and publication periods. A prolific account must not dominate solely through volume.

When the hard cap is reached, removal priority is:

1. Machine translations.
2. Unverified translations.
3. Unattributed reposts.
4. Duplicates and near-duplicates.
5. Marketing-heavy or terminology-light material.
6. Superseded documentation.
7. Older sources whose terminology is already fully represented.

Older sources remain eligible when they document historical terminology, the origin of an established rendering, or a still-used regional or contextual variant.

## Incremental Research Runs

Each run must:

1. Load the last completed run and current source manifest.
2. Recheck known accepted sources for accessibility and material changes.
3. Search for content published or discovered since the previous run.
4. Add discoveries to the candidate queue before accepting them.
5. Detect unchanged content using a content hash where a local snapshot is available.
6. Deduplicate mirrors and near-identical copies as one logical source.
7. Apply provenance, translation-quality, and evidence-eligibility review.
8. Extract terminology only from accepted evidence.
9. Compare proposed entries and variants against the current dictionaries.
10. Apply original-Chinese precedence and `(T)` reference labeling.
11. Measure marginal new-term and new-variant yield.
12. Archive the previous root TSVs only when publishing a new dataset version.
13. Record run results and every source-status decision.

A failed or interrupted run remains recorded with a non-complete status and can be resumed using its `run_id`.

## Research Run Ledger

`research/research_runs.tsv` is append-only and contains:

```text
run_id
status
started_at
completed_at
dataset_version_before
dataset_version_after
search_scope
accounts_or_projects
search_queries
platforms
candidate_count
accepted_count
updated_count
rejected_count
removed_count
new_terms
new_variants
saturation_window
saturation_new_terms
saturation_new_variants
review_method
tool_version
operator
notes
```

Run IDs use a sortable form such as `2026-09-05-wechat-discovery-01` or `2026-10-01-monthly-refresh-01`.

## Candidate Queue

`research/candidate_sources.tsv` separates discovery from accepted evidence and contains:

```text
candidate_id
first_seen_run
discovered_at
title
publisher_or_account
canonical_url
retrieval_url
platform
suspected_origin
candidate_status
notes
```

The 1,000-source cap applies only to accepted logical sources in `source_manifest.tsv`, not to this candidate queue.

## Source Manifest Extensions

The source manifest will retain its current fields and add:

```text
logical_source_id
first_seen_run
last_checked_run
first_seen_date
last_checked_date
content_published_date
content_modified_date
content_hash
canonical_url
retrieval_url
wechat_account
content_origin
translation_method
translator
original_url
quality_status
quality_score
quality_notes
access_status
supersedes_source_id
```

Exact column order will be defined in the implementation plan. Existing source IDs and dictionary references must remain stable unless a documented correction is required.

## Source Decision Ledger

`research/source_decisions.tsv` is append-only and contains:

```text
run_id
source_or_candidate_id
decision
reason_code
reason_detail
previous_status
new_status
reviewer
date
```

Decisions include acceptance, rejection, quarantine, metadata correction, supersession, restoration, and removal. This ledger prevents repeated review of known duplicates, low-quality translations, dead links, and rejected sources.

## Publication and Versioning

The latest release always uses stable root filenames. Each row continues to carry its dataset date and semantic version.

When a research run produces material dictionary changes:

1. Copy the prior root TSV release into `archived/<prior-version>/` using dated/versioned filenames.
2. Publish the new TSVs at the stable root paths.
3. Record the new version in the completed research-run row.

Runs that discover no material dictionary changes do not create a new dataset version or archive duplicate TSVs.

## Validation

Before a run is marked complete or a release is published, validation must confirm:

- UTF-8 encoding and consistent TSV field counts;
- unique run, candidate, logical-source, and source IDs;
- all dictionary references resolve to accepted manifest sources;
- every translated reference has `(T)` and no original-Chinese reference does;
- primary references precede translated fallback references;
- excluded sources do not support dictionary entries;
- all local snapshot paths exist and contain the expected content rather than a challenge page;
- content hashes use one declared algorithm consistently;
- accepted logical-source count does not exceed 1,000;
- source and decision counts reconcile with the research-run summary;
- archived and current release metadata match their directory and release versions.

## Initial Implementation Boundary

The first implementation should establish the metadata files, document the operating procedure, migrate existing manifest records without changing existing terminology decisions, and record the 2026-09-05 WeChat feasibility research as the first run. It should seed the candidate queue with the promising WeChat sources already identified, but should not accept them into the dictionary until each source passes content and provenance review.

Automated crawling, scheduled execution, and bulk ingestion are explicitly deferred. They can be added later after the manual workflow and schemas prove stable.

# Research Refresh System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish a reproducible, incremental research-refresh workflow with auditable source provenance, translation-quality controls, WeChat candidate staging, saturation tracking, and automated TSV validation.

**Architecture:** Stable root dictionaries remain the published interface. An extended source manifest holds accepted evidence, while append-only TSV ledgers under `research/` hold run summaries, candidate discoveries, and source decisions. A dependency-free Python validator enforces schemas, identifiers, evidence eligibility, translated-reference labels, source limits, local snapshot integrity, and run-count reconciliation.

**Tech Stack:** UTF-8 TSV, Python 3 standard library (`csv`, `hashlib`, `pathlib`, `re`, `unittest`), Git.

**Spec:** `docs/superpowers/specs/2026-09-05-research-refresh-design.md`

## Global Constraints

- The accepted evidence corpus has a hard maximum of 1,000 logical sources and a soft target of 300–500 high-quality, diverse sources.
- Original Chinese usage takes precedence when original and translated sources disagree.
- Accepted translated evidence is marked ` (T)` in dictionary `references` fields.
- `machine_translated`, `translation_unknown`, and `originality_unknown` sources cannot support dictionary entries.
- Direct WeChat retrieval must not bypass CAPTCHAs or other access controls, and challenge pages must not be stored as evidence.
- Search snippets and unattributed reposts are discovery inputs, not accepted evidence.
- Existing dictionary terms and source IDs remain unchanged during this initial metadata migration.
- The current root TSV release remains `v1.1.0`; metadata-only work does not create a dictionary release or archive duplicate TSVs.
- All new operational metadata files are append-only after their initial creation.
- Use SHA-256 for local snapshot content hashes.

---

## File Structure

- Create `scripts/validate_research_data.py`: dependency-free validator and CLI.
- Create `tests/test_validate_research_data.py`: unit tests for schema, provenance, references, limits, snapshots, and run reconciliation.
- Modify `source_manifest.tsv`: migrate accepted sources to the extended auditable schema.
- Create `research/research_runs.tsv`: append-only research-run ledger.
- Create `research/candidate_sources.tsv`: discoveries awaiting evidence review.
- Create `research/source_decisions.tsv`: append-only decision audit trail.
- Create `research/README.md`: operating procedure, enums, scoring rubric, saturation and publication rules.
- Modify `sources/README.md`: point readers to the research metadata and clarify canonical versus retrieval URLs.

---

### Task 1: Dependency-Free Research Data Validator

**Files:**
- Create: `scripts/validate_research_data.py`
- Create: `tests/test_validate_research_data.py`

**Interfaces:**
- Consumes: repository root containing the four stable TSVs, `research/*.tsv`, `source_manifest.tsv`, and `sources/` snapshots.
- Produces: `validate_repository(root: pathlib.Path) -> list[str]`, where an empty list means valid; CLI exits `0` on success and `1` after printing one error per line on failure.

- [ ] **Step 1: Write failing validator tests**

Create `tests/test_validate_research_data.py` using `unittest`, `csv`, `tempfile`, and `pathlib`. Include these test cases with minimal temporary TSV fixtures:

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import csv
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.validate_research_data import validate_repository


def write_tsv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


class ResearchDataValidationTests(unittest.TestCase):
    def test_valid_minimal_repository_has_no_errors(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_repository(root)
            self.assertEqual([], validate_repository(root))

    def test_rejects_unlabeled_translated_reference(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_repository(root)
            terms = root / "translated_terms_zh.tsv"
            text = terms.read_text(encoding="utf-8").replace("SRC-T (T)", "SRC-T")
            terms.write_text(text, encoding="utf-8")
            self.assertTrue(any("must end with (T)" in e for e in validate_repository(root)))

    def test_rejects_excluded_source_reference(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_repository(root)
            manifest = root / "source_manifest.tsv"
            text = manifest.read_text(encoding="utf-8").replace("human_translated", "machine_translated")
            manifest.write_text(text, encoding="utf-8")
            self.assertTrue(any("ineligible source" in e for e in validate_repository(root)))

    def test_rejects_more_than_1000_logical_sources(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_repository(root)
            # Append 1,000 distinct accepted logical sources to the one already present.
            self.append_manifest_sources(root, 1000)
            self.assertTrue(any("1,000" in e for e in validate_repository(root)))

    def test_rejects_challenge_page_snapshot(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_repository(root)
            snapshot = root / "sources" / "translated.html"
            snapshot.write_text("wappoc_appmsgcaptcha VerifyCode", encoding="utf-8")
            self.assertTrue(any("challenge page" in e for e in validate_repository(root)))

    def test_reconciles_run_and_candidate_counts(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_valid_repository(root)
            runs = root / "research" / "research_runs.tsv"
            text = runs.read_text(encoding="utf-8").replace("\t1\t0\t", "\t2\t0\t", 1)
            runs.write_text(text, encoding="utf-8")
            self.assertTrue(any("candidate_count" in e for e in validate_repository(root)))

    # make_valid_repository and append_manifest_sources write all required headers
    # exactly as defined in Tasks 2 and 3, with SRC-O as original_chinese,
    # SRC-T as human_translated, one local snapshot per source, one completed run,
    # and one queued candidate and decision assigned to that run.


if __name__ == "__main__":
    unittest.main()
```

Implement the two fixture helpers fully in the test file. Do not use repository production data as test fixtures.

- [ ] **Step 2: Run tests to verify they fail**

Run:

```bash
python3 -m unittest tests/test_validate_research_data.py -v
```

Expected: import failure because `scripts.validate_research_data` does not exist.

- [ ] **Step 3: Implement TSV loading, schemas, and validation**

Create `scripts/validate_research_data.py` with:

```python
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import re
import sys

MAX_ACCEPTED_LOGICAL_SOURCES = 1000
ELIGIBLE_ORIGINS = {"original_chinese", "human_translated"}
TRANSLATED_ORIGINS = {"human_translated"}
EXCLUDED_ORIGINS = {"machine_translated", "translation_unknown", "originality_unknown"}
RUN_STATUSES = {"running", "complete", "failed", "interrupted"}
CANDIDATE_STATUSES = {"discovered", "pending_review", "accepted", "rejected", "quarantined", "duplicate"}
QUALITY_STATUSES = {"accepted", "rejected", "quarantined"}
ACCESS_STATUSES = {"accessible", "accessible_snapshot", "challenge", "dead", "unknown"}
TRANSLATED_SUFFIX = " (T)"
CHALLENGE_MARKERS = ("wappoc_appmsgcaptcha", "VerifyCode", "环境异常", "完成验证")

MANIFEST_HEADER = [
    "source_id", "logical_source_id", "project_or_publisher", "source_type", "host",
    "language", "content_origin", "priority", "title", "url", "canonical_url",
    "retrieval_url", "local_path", "first_seen_run", "last_checked_run",
    "first_seen_date", "last_checked_date", "content_published_date",
    "content_modified_date", "content_hash", "translation_method", "translator",
    "original_url", "quality_status", "quality_score", "quality_notes",
    "access_status", "supersedes_source_id", "date", "notes", "version",
]

RUN_HEADER = [
    "run_id", "status", "started_at", "completed_at", "dataset_version_before",
    "dataset_version_after", "search_scope", "accounts_or_projects", "search_queries",
    "platforms", "candidate_count", "accepted_count", "updated_count", "rejected_count",
    "removed_count", "new_terms", "new_variants", "saturation_window",
    "saturation_new_terms", "saturation_new_variants", "review_method", "tool_version",
    "operator", "notes",
]

CANDIDATE_HEADER = [
    "candidate_id", "first_seen_run", "discovered_at", "title", "publisher_or_account",
    "canonical_url", "retrieval_url", "platform", "suspected_origin",
    "candidate_status", "notes",
]

DECISION_HEADER = [
    "run_id", "source_or_candidate_id", "decision", "reason_code", "reason_detail",
    "previous_status", "new_status", "reviewer", "date",
]
```

Implement:

- `read_tsv(path, expected_header)` with UTF-8 decoding, exact header matching, and duplicate-ID detection;
- `sha256_file(path)` returning lowercase hexadecimal SHA-256;
- `split_references(value)` splitting semicolon-separated references and stripping only the ` (T)` suffix;
- manifest enum, score (`0`–`100` integer), local-path, SHA-256, translation metadata, and logical-source-cap checks;
- dictionary reference checks against manifest eligibility and suffix rules;
- original references before translated references within each dictionary row;
- challenge-marker scanning for `.html`, `.htm`, `.md`, and `.txt` snapshots;
- candidate/run/decision foreign-key checks;
- completed-run `candidate_count` reconciliation with candidates whose `first_seen_run` equals that run;
- unique IDs for runs and candidates and unique `(run_id, source_or_candidate_id, decision)` decision tuples;
- `validate_repository(root)` accumulating all errors rather than stopping at the first;
- `main()` printing `research data validation passed` on success.

Treat `pre-ledger-v1.1.0` as the only allowed run sentinel in migrated manifest rows; it does not require a run-ledger row.

- [ ] **Step 4: Run tests to verify they pass**

Run:

```bash
python3 -m unittest tests/test_validate_research_data.py -v
```

Expected: all six tests pass.

- [ ] **Step 5: Commit validator and tests**

```bash
git add scripts/validate_research_data.py tests/test_validate_research_data.py
git commit -m "feat: validate research metadata and evidence"
```

---

### Task 2: Migrate the Accepted Source Manifest

**Files:**
- Modify: `source_manifest.tsv`
- Test: `tests/test_validate_research_data.py`

**Interfaces:**
- Consumes: the current 22-row v1.1.0 manifest and local files listed by `local_path`.
- Produces: the exact `MANIFEST_HEADER` schema consumed by the validator and later research runs.

- [ ] **Step 1: Add a failing production-manifest migration test**

Add this test:

```python
def test_repository_manifest_uses_extended_schema(self):
    root = Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    self.assertFalse([e for e in errors if "source_manifest.tsv header" in e], errors)
```

- [ ] **Step 2: Run the migration test to verify it fails**

Run:

```bash
python3 -m unittest tests.test_validate_research_data.ResearchDataValidationTests.test_repository_manifest_uses_extended_schema -v
```

Expected: failure reporting the old 13-column manifest header.

- [ ] **Step 3: Research the three existing translated-source provenance records**

For `WEB-SW-MESH`, `WEB-SW-HTTP`, and `WEB-OTEL-METRICS`, inspect the official source repositories or page history. Record:

- the non-Chinese original URL;
- the named translator when present, otherwise the accountable first-party localization team;
- translation method as `first_party_human_translation` or `community_human_translation`;
- a concise `quality_notes` explanation.

If human translation cannot be substantiated from first-party history, stop this task and report the affected dictionary references. Do not invent a translator and do not silently classify the source as original Chinese.

- [ ] **Step 4: Rewrite the manifest with the extended schema**

For all 22 current records:

- preserve `source_id`, titles, existing URLs, local paths, source order, dictionary eligibility, date `2026-09-04`, and version `v1.1.0`;
- set `logical_source_id` equal to `source_id` because no current records are mirrors of each other;
- set `first_seen_run` and `last_checked_run` to `pre-ledger-v1.1.0`;
- set `first_seen_date` to the existing row date and `last_checked_date` to `2026-09-05`;
- copy the old `url` into both `canonical_url` and `retrieval_url` unless the canonical and retrieved locations genuinely differ;
- compute `content_hash` from the local snapshot using SHA-256;
- map 19 primary sources to `original_chinese`, `quality_status=accepted`, and `priority=primary`;
- map the three verified translated sources to `human_translated`, `quality_status=accepted`, and `priority=fallback`;
- set `quality_score` using the documented rubric in Task 4, with every accepted source scoring at least `60`;
- set `access_status=accessible_snapshot`;
- leave genuinely unknown publication/modification dates empty;
- leave `supersedes_source_id` empty.

Use a one-off standard-library Python migration command or carefully edit the TSV; do not add a permanent migration script.

- [ ] **Step 5: Run manifest and dictionary validation**

Run:

```bash
python3 -m unittest tests/test_validate_research_data.py -v
python3 scripts/validate_research_data.py
```

Expected: unit tests pass. The repository validator may still report missing `research/*.tsv` files, but it must report no manifest-schema, hash, provenance, eligibility, or dictionary-reference errors.

- [ ] **Step 6: Commit the manifest migration**

```bash
git add source_manifest.tsv tests/test_validate_research_data.py
git commit -m "data: add auditable source provenance metadata"
```

---

### Task 3: Seed Research Run, Candidate, and Decision Ledgers

**Files:**
- Create: `research/research_runs.tsv`
- Create: `research/candidate_sources.tsv`
- Create: `research/source_decisions.tsv`
- Test: `tests/test_validate_research_data.py`

**Interfaces:**
- Consumes: `RUN_HEADER`, `CANDIDATE_HEADER`, and `DECISION_HEADER` from the validator; the approved WeChat feasibility findings.
- Produces: one completed run, ten pending candidates, and ten append-only queue decisions linked by `run_id`.

- [ ] **Step 1: Add a failing production-ledger test**

```python
def test_repository_research_ledgers_are_consistent(self):
    root = Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    self.assertEqual([], errors)
```

- [ ] **Step 2: Run it to verify it fails**

Run:

```bash
python3 -m unittest tests.test_validate_research_data.ResearchDataValidationTests.test_repository_research_ledgers_are_consistent -v
```

Expected: failure listing the three missing research TSVs.

- [ ] **Step 3: Create the completed feasibility-run row**

Create `research/research_runs.tsv` with `RUN_HEADER` and one row:

- `run_id`: `2026-09-05-wechat-discovery-01`
- `status`: `complete`
- timestamps: ISO 8601 with timezone; use the actual start/completion timestamps recorded during implementation
- dataset before/after: `v1.1.0` / `v1.1.0`
- scope: WeChat feasibility and reverse discovery for Chinese observability/eBPF sources
- platforms: `WeChat | Sogou Weixin | official sites | attributed mirrors | web search`
- counts: candidates `10`, accepted `0`, updated `0`, rejected `0`, removed `0`, new terms `0`, new variants `0`
- saturation fields: window `0`, new terms `0`, new variants `0` because candidates were not yet reviewed
- review method: `manual provenance and accessibility feasibility review`
- tool version: `codex`
- operator: `OpenAI Codex`
- notes: direct WeChat URLs returned verification challenges; candidates require content/provenance review before acceptance

- [ ] **Step 4: Seed ten WeChat candidates**

Create `research/candidate_sources.tsv` with these stable IDs and canonical URLs:

```text
WC-2026-0001  https://mp.weixin.qq.com/s/OdDy1sNoQNy5zUwMxxAG_A
WC-2026-0002  https://mp.weixin.qq.com/s/mOS0XBWxtNhuVJ35qg_M_Q
WC-2026-0003  https://mp.weixin.qq.com/s/0IUvaPpjsXl7zXw8E3LSSg
WC-2026-0004  https://mp.weixin.qq.com/s/nqgec7BLov0o9IycDAnk2A
WC-2026-0005  https://mp.weixin.qq.com/s/zvHQVBgU2IFUUYyzeDlokw
WC-2026-0006  https://mp.weixin.qq.com/s/4xlbWjclbSyCn91HpVRT9g
WC-2026-0007  https://mp.weixin.qq.com/s/FyPaifHGs3knCcHmjMGVqg
WC-2026-0008  https://mp.weixin.qq.com/s/lDhCoLN0mknquJcO15Fd2Q
WC-2026-0009  https://mp.weixin.qq.com/s/Gmst4_FsbXUIhuJw1BXNnQ
WC-2026-0010  https://mp.weixin.qq.com/s/z0xLlYpSdCi_k2fCxuUW9w
```

Populate the known titles, publishers/accounts, and retrieval URLs from the approved feasibility report. Set `first_seen_run=2026-09-05-wechat-discovery-01`, `discovered_at=2026-09-05`, `platform=WeChat`, `suspected_origin=original_chinese`, and `candidate_status=pending_review`. Where only an index rather than a full attributed copy exists, state that explicitly in `notes`.

- [ ] **Step 5: Record queue decisions**

Create `research/source_decisions.tsv` with one `queued_for_review` decision for each candidate:

- `run_id=2026-09-05-wechat-discovery-01`
- `reason_code=wechat_reverse_discovery`
- `previous_status` empty
- `new_status=pending_review`
- `reviewer=OpenAI Codex`
- `date=2026-09-05`
- `reason_detail` identifies the official or attributed page that exposed the canonical WeChat URL

- [ ] **Step 6: Run tests and repository validation**

```bash
python3 -m unittest tests/test_validate_research_data.py -v
python3 scripts/validate_research_data.py
```

Expected: all tests pass and CLI prints `research data validation passed`.

- [ ] **Step 7: Commit the seeded ledgers**

```bash
git add research/research_runs.tsv research/candidate_sources.tsv research/source_decisions.tsv tests/test_validate_research_data.py
git commit -m "data: seed WeChat research run and candidates"
```

---

### Task 4: Document the Manual Refresh Workflow and Quality Rubric

**Files:**
- Create: `research/README.md`
- Modify: `sources/README.md`
- Test: `tests/test_validate_research_data.py`

**Interfaces:**
- Consumes: schemas and enums implemented in Tasks 1–3 and policy from the specification.
- Produces: a human-operable checklist for future periodic runs and stable documentation links.

- [ ] **Step 1: Add documentation-presence tests**

Add a test that reads `research/README.md` and asserts it contains all of:

```python
required_sections = {
    "## Running a refresh",
    "## Source precedence",
    "## Translation-quality gate",
    "## Quality scoring",
    "## Saturation and the 1,000-source cap",
    "## WeChat handling",
    "## Publishing a release",
    "## Validation",
}
```

- [ ] **Step 2: Run the documentation test to verify it fails**

Run the new test directly and expect failure because `research/README.md` does not exist.

- [ ] **Step 3: Write the operating procedure**

Create `research/README.md` with the required sections and exact commands:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_research_data.py
```

Document:

- append-only rules for all three research ledgers;
- all enum values from the validator;
- the `pre-ledger-v1.1.0` migration sentinel;
- candidate-to-source promotion steps;
- original Chinese over translated evidence precedence;
- `(T)` reference syntax;
- machine-translation rejection signals;
- mirror deduplication by `logical_source_id`;
- CAPTCHA/challenge-page prohibition;
- saturation window of 50 reviewed sources and thresholds of fewer than five new terms and fewer than five new variants;
- hard cap of 1,000 accepted logical sources and soft target of 300–500;
- archive-on-material-release behavior.

Define the inspectable 100-point quality rubric:

```text
original Chinese authorship       25
first-party technical authority   20
terminology density                15
technical depth                    15
independent corroboration value    10
recency/relevance                    5
stable accessibility                5
clear provenance                     5
```

Require `60` points for acceptance. A source that fails an evidence-eligibility rule remains ineligible regardless of score.

- [ ] **Step 4: Update the source-corpus README**

Link `sources/README.md` to `../research/README.md`, `../research/research_runs.tsv`, `../research/source_decisions.tsv`, and `../research/candidate_sources.tsv`. Explain that `canonical_url` identifies the original publication while `retrieval_url` identifies the copy actually captured or reviewed.

- [ ] **Step 5: Run documentation and full validation tests**

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_research_data.py
git diff --check
```

Expected: all tests pass, validator reports success, and Git reports no whitespace errors.

- [ ] **Step 6: Commit documentation**

```bash
git add research/README.md sources/README.md tests/test_validate_research_data.py
git commit -m "docs: define periodic research refresh workflow"
```

---

### Task 5: Final Release-Neutral Verification

**Files:**
- Verify: all files changed by Tasks 1–4

**Interfaces:**
- Consumes: completed implementation.
- Produces: evidence that metadata infrastructure is valid and the published dictionary remains v1.1.0.

- [ ] **Step 1: Run the complete test suite**

```bash
python3 -m unittest discover -s tests -v
```

Expected: all tests pass with zero failures and zero errors.

- [ ] **Step 2: Run repository validation**

```bash
python3 scripts/validate_research_data.py
```

Expected: `research data validation passed`.

- [ ] **Step 3: Verify release neutrality and source counts**

```bash
awk -F '\t' 'NR>1 {versions[$NF]++} END {for (v in versions) print v, versions[v]}' translated_terms_zh.tsv
awk -F '\t' 'NR>1 {logical[$2]=1} END {print "accepted logical sources", length(logical)}' source_manifest.tsv
awk -F '\t' 'NR>1 {status[$10]++} END {for (s in status) print s, status[s]}' research/candidate_sources.tsv
```

Expected:

```text
v1.1.0 99
accepted logical sources 22
pending_review 10
```

- [ ] **Step 4: Inspect Git state and commit history**

```bash
git status --short
git log --oneline -6
```

Expected: clean working tree and one focused commit per completed task, plus the spec and plan commits.

- [ ] **Step 5: Push only after explicit integration approval**

Do not push during task execution. Use the branch-finishing workflow after all verification passes and the user chooses how to integrate the work.

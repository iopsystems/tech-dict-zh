#!/usr/bin/env python3
"""Validate dictionary evidence and research ledgers."""
import csv, hashlib, re, sys
from collections import Counter
from pathlib import Path

MANIFEST_HEADER="source_id logical_source_id project_or_publisher source_type host language content_origin priority title url canonical_url retrieval_url local_path first_seen_run last_checked_run first_seen_date last_checked_date content_published_date content_modified_date content_hash translation_method translator original_url quality_status quality_score quality_notes access_status supersedes_source_id date notes version".split()
RUN_HEADER="run_id status started_at completed_at dataset_version_before dataset_version_after search_scope accounts_or_projects search_queries platforms candidate_count accepted_count updated_count rejected_count removed_count new_terms new_variants saturation_window saturation_new_terms saturation_new_variants review_method tool_version operator notes".split()
CANDIDATE_HEADER="candidate_id first_seen_run discovered_at title publisher_or_account canonical_url retrieval_url platform suspected_origin candidate_status notes".split()
DECISION_HEADER="run_id source_or_candidate_id decision reason_code reason_detail previous_status new_status reviewer date".split()
ELIGIBLE={"original_chinese","human_translated"}
ORIGINS=ELIGIBLE|{"machine_translated","translation_unknown","originality_unknown"}
RUN_STATUSES={"running","complete","failed","interrupted"}
CANDIDATE_STATUSES={"discovered","pending_review","accepted","rejected","quarantined","duplicate"}
QUALITY_STATUSES={"accepted","rejected","quarantined"}
ACCESS_STATUSES={"accessible","accessible_snapshot","challenge","dead","unknown"}
CHALLENGE_MARKERS=("wappoc_appmsgcaptcha","VerifyCode","环境异常","完成验证")
RUN_SENTINELS={"pre-ledger-v1.1.0"}

def _read(root, rel, header, errors):
    path=root/rel
    if not path.is_file(): errors.append(f"{rel}: missing file"); return []
    with path.open(encoding="utf-8-sig",newline="") as f:
        reader=csv.DictReader(f,delimiter="\t")
        if reader.fieldnames != header: errors.append(f"{rel}: header mismatch; expected {header!r}")
        try:return list(reader)
        except csv.Error as exc: errors.append(f"{rel}: malformed TSV: {exc}"); return []

def _duplicates(rows,key):
    return [v for v,n in Counter(r.get(key,"") for r in rows if r.get(key,"")).items() if n>1]

def _integer(value,label,errors,minimum=0):
    try:n=int(value)
    except (TypeError,ValueError): errors.append(f"{label}: expected integer, got {value!r}"); return None
    if n<minimum: errors.append(f"{label}: must be >= {minimum}")
    return n

def _references(value):
    for raw in filter(None,(x.strip() for x in value.split(";"))):
        translated=raw.endswith(" (T)")
        yield (raw[:-4].strip() if translated else raw),translated

def validate_repository(root):
    root=Path(root); errors=[]
    manifest=_read(root,"source_manifest.tsv",MANIFEST_HEADER,errors)
    runs=_read(root,"research/research_runs.tsv",RUN_HEADER,errors)
    candidates=_read(root,"research/candidate_sources.tsv",CANDIDATE_HEADER,errors)
    decisions=_read(root,"research/source_decisions.tsv",DECISION_HEADER,errors)
    for label,rows,key in (("manifest",manifest,"source_id"),("runs",runs,"run_id"),("candidates",candidates,"candidate_id")):
        for value in _duplicates(rows,key): errors.append(f"{label}: duplicate {key} {value}")
    run_ids={r.get("run_id") for r in runs}|RUN_SENTINELS
    sources={r.get("source_id"):r for r in manifest}
    logical={r.get("logical_source_id") for r in manifest if r.get("quality_status")=="accepted" and r.get("logical_source_id")}
    if len(logical)>1000: errors.append(f"manifest: {len(logical)} accepted logical sources exceeds cap 1000")
    for i,row in enumerate(manifest,2):
        tag=f"source_manifest.tsv:{i} {row.get('source_id','')}"
        origin=row.get("content_origin")
        if not row.get("source_id"): errors.append(f"{tag}: source_id is required")
        if not row.get("logical_source_id"): errors.append(f"{tag}: logical_source_id is required")
        if origin not in ORIGINS: errors.append(f"{tag}: invalid content_origin {origin!r}")
        if row.get("quality_status") not in QUALITY_STATUSES: errors.append(f"{tag}: invalid quality_status")
        if origin not in ELIGIBLE and row.get("quality_status")=="accepted": errors.append(f"{tag}: excluded content_origin cannot be accepted")
        if row.get("access_status") not in ACCESS_STATUSES: errors.append(f"{tag}: invalid access_status")
        score=_integer(row.get("quality_score"),f"{tag} quality_score",errors)
        if score is not None and score not in range(0,101): errors.append(f"{tag}: quality_score must be 0..100")
        if row.get("quality_status")=="accepted" and score is not None and score < 60: errors.append(f"{tag}: accepted source quality_score must be at least 60")
        for field in ("first_seen_run","last_checked_run"):
            if row.get(field) not in run_ids: errors.append(f"{tag}: unknown {field} {row.get(field)!r}")
        translated=origin=="human_translated"
        if translated and not all(row.get(x) for x in ("translation_method","translator","original_url")): errors.append(f"{tag}: human translation requires method, translator, and original_url")
        if not translated and row.get("translation_method") not in ("","not_applicable"): errors.append(f"{tag}: translation_method conflicts with content_origin")
        rel=row.get("local_path",""); path=root/rel; sources_root=(root/"sources").resolve()
        try: contained=path.resolve().is_relative_to(sources_root)
        except (OSError,RuntimeError): contained=False
        if not contained or any(part.is_symlink() for part in [path,*path.parents] if part != root): errors.append(f"{tag}: local_path must remain inside sources directory without symlinks"); continue
        if not rel or not path.is_file(): errors.append(f"{tag}: missing local_path {rel!r}"); continue
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if row.get("content_hash") != digest: errors.append(f"{tag}: content_hash mismatch")
        if path.suffix.lower() in {".md",".txt",".html",".htm"}:
            text=path.read_text(encoding="utf-8",errors="replace")
            if any(marker in text for marker in CHALLENGE_MARKERS): errors.append(f"{tag}: challenge page marker in snapshot")
    for rel in ("translated_terms_zh.tsv","untranslated_terms_zh.tsv"):
        path=root/rel
        if not path.is_file(): errors.append(f"{rel}: missing file"); continue
        with path.open(encoding="utf-8-sig",newline="") as f:
            reader=csv.DictReader(f,delimiter="\t")
            refcol = "references" if reader.fieldnames and "references" in reader.fieldnames else "reference"
            if not reader.fieldnames or refcol not in reader.fieldnames: errors.append(f"{rel}: missing references column"); continue
            for line,row in enumerate(reader,2):
                seen_translated=False
                for sid,marked in _references(row.get(refcol,"")):
                    source=sources.get(sid)
                    if not source: errors.append(f"{rel}:{line}: unknown reference {sid}"); continue
                    if source.get("content_origin") not in ELIGIBLE or source.get("quality_status")!="accepted": errors.append(f"{rel}:{line}: ineligible reference {sid}")
                    should_mark=source.get("content_origin")=="human_translated"
                    if marked != should_mark: errors.append(f"{rel}:{line}: reference {sid} {'requires' if should_mark else 'must not use'} (T)")
                    if seen_translated and not should_mark: errors.append(f"{rel}:{line}: original Chinese references must precede translated references")
                    seen_translated |= should_mark
    run_by_id={r.get("run_id"):r for r in runs}
    candidate_ids={c.get("candidate_id") for c in candidates}
    source_or_candidate=set(sources)|candidate_ids
    for i,row in enumerate(runs,2):
        if row.get("status") not in RUN_STATUSES: errors.append(f"research_runs.tsv:{i}: invalid status")
        for field in ("candidate_count","accepted_count","updated_count","rejected_count","removed_count","new_terms","new_variants","saturation_window","saturation_new_terms","saturation_new_variants"):
            if row.get(field)!="": _integer(row.get(field),f"research_runs.tsv:{i} {field}",errors)
    for i,row in enumerate(candidates,2):
        if row.get("candidate_status") not in CANDIDATE_STATUSES: errors.append(f"candidate_sources.tsv:{i}: invalid candidate_status")
        if row.get("first_seen_run") not in run_by_id: errors.append(f"candidate_sources.tsv:{i}: unknown first_seen_run")
    decision_keys=[(r.get("run_id"),r.get("source_or_candidate_id"),r.get("decision")) for r in decisions]
    for key,count in Counter(decision_keys).items():
        if count>1: errors.append(f"source_decisions.tsv: duplicate decision tuple {key}")
    for i,row in enumerate(decisions,2):
        if row.get("run_id") not in run_by_id: errors.append(f"source_decisions.tsv:{i}: unknown run_id")
        if row.get("source_or_candidate_id") not in source_or_candidate: errors.append(f"source_decisions.tsv:{i}: unknown source_or_candidate_id")
    discovered=Counter(c.get("first_seen_run") for c in candidates)
    accepted=Counter(d.get("run_id") for d in decisions if d.get("new_status")=="accepted")
    rejected=Counter(d.get("run_id") for d in decisions if d.get("new_status")=="rejected")
    removed=Counter(d.get("run_id") for d in decisions if d.get("decision") in {"remove","removed","removal"} or d.get("new_status")=="removed")
    updated=Counter(d.get("run_id") for d in decisions if d.get("decision") in {"metadata_correction","supersession","restoration","update","updated"})
    for rid,row in run_by_id.items():
        if row.get("status")!="complete": continue
        for field,actual in (("candidate_count",discovered[rid]),("accepted_count",accepted[rid]),("updated_count",updated[rid]),("rejected_count",rejected[rid]),("removed_count",removed[rid])):
            expected=_integer(row.get(field),f"research_runs.tsv {rid} {field}",errors)
            if expected is not None and expected != actual: errors.append(f"research_runs.tsv {rid}: {field} {expected} != {actual} ledger rows")
    return errors

def main(argv=None):
    root=Path((argv or sys.argv)[1]) if len(argv or sys.argv)>1 else Path.cwd()
    errors=validate_repository(root)
    if errors:
        for error in errors: print(f"ERROR: {error}",file=sys.stderr)
        return 1
    print("Research data validation passed.")
    return 0
if __name__=="__main__": raise SystemExit(main())

import csv,hashlib,sys,unittest
from pathlib import Path
from tempfile import TemporaryDirectory
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.validate_research_data import validate_repository
MH="source_id logical_source_id project_or_publisher source_type host language content_origin priority title url canonical_url retrieval_url local_path first_seen_run last_checked_run first_seen_date last_checked_date content_published_date content_modified_date content_hash translation_method translator original_url quality_status quality_score quality_notes access_status supersedes_source_id date notes version".split()
RH="run_id status started_at completed_at dataset_version_before dataset_version_after search_scope accounts_or_projects search_queries platforms candidate_count accepted_count updated_count rejected_count removed_count new_terms new_variants saturation_window saturation_new_terms saturation_new_variants review_method tool_version operator notes".split()
CH="candidate_id first_seen_run discovered_at title publisher_or_account canonical_url retrieval_url platform suspected_origin candidate_status notes".split()
DH="run_id source_or_candidate_id decision reason_code reason_detail previous_status new_status reviewer date".split()
def tsv(p,h,rs):
 p.parent.mkdir(parents=True,exist_ok=True)
 with p.open("w",encoding="utf-8",newline="") as f:w=csv.DictWriter(f,fieldnames=h,delimiter="\t");w.writeheader();w.writerows(rs)
class Tests(unittest.TestCase):
 def setUp(self):
  self.t=TemporaryDirectory();self.r=Path(self.t.name);(self.r/"sources").mkdir()
  for s in ("O","T"):(self.r/"sources"/f"{s}.md").write_text("trusted",encoding="utf-8")
  self.m=[self.src("O","original_chinese"),self.src("T","human_translated")];tsv(self.r/"source_manifest.tsv",MH,self.m)
  tsv(self.r/"translated_terms_zh.tsv",["term","reference"],[{"term":"metrics","reference":"O;T (T)"}]);tsv(self.r/"untranslated_terms_zh.tsv",["term","reference"],[{"term":"eBPF","reference":"O"}])
  tsv(self.r/"research/research_runs.tsv",RH,[dict.fromkeys(RH,"")|{"run_id":"R","status":"complete","candidate_count":"1"}]);tsv(self.r/"research/candidate_sources.tsv",CH,[dict.fromkeys(CH,"")|{"candidate_id":"C","first_seen_run":"R","candidate_status":"accepted"}]);tsv(self.r/"research/source_decisions.tsv",DH,[dict.fromkeys(DH,"")|{"run_id":"R","source_or_candidate_id":"C","decision":"accept"}])
 def tearDown(self):self.t.cleanup()
 def src(self,s,o):
  p=f"sources/{s}.md";tr=o=="human_translated"
  return dict.fromkeys(MH,"")|{"source_id":s,"logical_source_id":s,"content_origin":o,"local_path":p,"first_seen_run":"R","last_checked_run":"R","content_hash":hashlib.sha256((self.r/p).read_bytes()).hexdigest(),"translation_method":"human" if tr else "not_applicable","translator":"x" if tr else "","original_url":"https://original" if tr else "","quality_status":"accepted","quality_score":"80","access_status":"accessible"}
 def err(self,x):self.assertTrue(any(x in e for e in validate_repository(self.r)),validate_repository(self.r))
 def test_valid(self):self.assertEqual([],validate_repository(self.r))
 def test_marker(self):tsv(self.r/"translated_terms_zh.tsv",["term","reference"],[{"term":"x","reference":"T"}]);self.err("(T)")
 def test_ineligible(self):self.m[0]["content_origin"]="machine_translated";tsv(self.r/"source_manifest.tsv",MH,self.m);self.err("ineligible")
 def test_cap(self):
  self.m=[self.src("O","original_chinese")|{"source_id":f"S{i}","logical_source_id":f"S{i}"} for i in range(1001)];tsv(self.r/"source_manifest.tsv",MH,self.m);self.err("1000")
 def test_challenge(self):
  p=self.r/"sources/O.md";p.write_text("wappoc_appmsgcaptcha",encoding="utf-8");self.m[0]["content_hash"]=hashlib.sha256(p.read_bytes()).hexdigest();tsv(self.r/"source_manifest.tsv",MH,self.m);self.err("challenge")
 def test_count(self):
  p=self.r/"research/research_runs.tsv";f=p.open();rs=list(csv.DictReader(f,delimiter="\t"));f.close();rs[0]["candidate_count"]="2";tsv(p,RH,rs);self.err("candidate_count")

 def test_repository_manifest_uses_extended_schema(self):
  root=Path(__file__).resolve().parents[1];errors=validate_repository(root);self.assertFalse([e for e in errors if "source_manifest.tsv" in e and "header" in e],errors)
 def test_repository_research_ledgers_are_consistent(self):
  self.assertEqual([],validate_repository(Path(__file__).resolve().parents[1]))

 def test_research_readme_has_required_sections(self):
  text=(Path(__file__).resolve().parents[1]/"research/README.md").read_text()
  for heading in ("## Running a refresh","## Source precedence","## Translation-quality gate","## Quality scoring","## Saturation and the 1,000-source cap","## WeChat handling","## Publishing a release","## Validation"): self.assertIn(heading,text)

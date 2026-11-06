import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import unittest

PATH = pathlib.Path(__file__).parents[1] / "skills/instagram-creator-reels-insights/scripts/workflow.py"
SPEC = importlib.util.spec_from_file_location("creator_workflow", PATH)
wf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wf)

POST_CONTRACT = {"creator":"creator","url":"url","timestamp":"created","type":"kind","id":"stable","id_kind":"pk","video_values":["reel","video"],"non_video_values":["image","carousel"]}
TRANSCRIPT_CONTRACT = {"url":"url","code":"code","pk":"pk","creator":"userName","text":"text","segments":"segments","error":"errMsg","segment_text":"text","post_id_kind":"pk"}
START, END = "2026-11-05T00:00:00Z", "2026-11-06T00:00:00Z"

# Synthetic contracts for offline planner tests only. These do not assert that
# the current Codex host exposes or forwards these options.
OFFLINE_HOST_CONTRACT = {"verified":True,
    "call_tool":"call-actor",
    "call_actor_fields":["actor","input","waitSecs","callOptions"],
    "call_options_fields":["maxItems","maxTotalChargeUsd"],
    "run_readback":{"verified":True,"tool":"get-actor-run-list","items_field":"items",
        "run_id_field":"id","options_field":"options","options_fields":["maxItems","maxTotalChargeUsd"]},
    "max_wait_secs":45}

def pricing(model, unit=None, minimum="0.01"):
    result = {"verified":True,"currency":"USD","source":"synthetic offline fixture",
              "checked_at":"test-only","model":model,"minimum_run_charge_usd":minimum}
    if model == "pay_per_result":
        result.update({"max_total_cost_per_result_usd":unit,"max_fixed_run_cost_usd":"0.00",
                       "all_billable_components_bounded_by_max_items":True})
    else:
        result["all_billable_components_bounded_by_max_total_charge_usd"] = True
    return result

def post(code, creator="a", created=START, url=None, stable=None):
    return {"creator":creator,"url":url or f"https://www.instagram.com/reel/{code}/",
            "created":created,"kind":"reel","stable":stable or code}

def synthetic_run(run_id, usernames, posts, results_limit, retrieval_complete=True, **extra):
    """Synthetic Profile Posts run envelope for offline tests; not Actor evidence."""
    return {"run_id":run_id,"usernames":usernames,"posts":posts,"results_limit":results_limit,
            "retrieval_complete":retrieval_complete,"run_status":"SUCCEEDED",**extra}

def select(posts, accounts, cap, contract=POST_CONTRACT, retrieval_complete=True,
           results_limit=None, usernames=None, run_id="synthetic-run", **run_extra):
    limit = results_limit if results_limit is not None else max(1,len(posts)+1)
    run = synthetic_run(run_id,usernames or accounts,posts,limit,retrieval_complete,**run_extra)
    return wf.select_posts([run],accounts,cap,START,END,contract)

class CreatorWorkflowTests(unittest.TestCase):
    def test_rolling_windows_use_exclusive_upper_bound(self):
        self.assertEqual(wf.window("2026-11-05T12:00:00+08:00", "daily"),
                         {"start_utc":"2026-11-04T04:00:00Z","end_utc_exclusive":"2026-11-05T04:00:00Z"})
        self.assertEqual(wf.window("2026-11-05T12:00:00+08:00", "weekly")["start_utc"], "2026-10-29T04:00:00Z")

    def test_settings_reject_zero_bad_precision_and_dot_path(self):
        for amount in (0, -1, float("nan"), float("inf"), "bad", "1.001"):
            with self.subTest(amount=amount), self.assertRaises(wf.ContractError):
                wf.validate_settings({"report_budget_usd":amount,"per_creator_limit":2,"accounts":["a"]})
        for account in ("https://www.instagram.com/./", "https://www.instagram.com/p/short/"):
            with self.subTest(account=account), self.assertRaises(wf.ContractError):
                wf.validate_settings({"report_budget_usd":"1.00","per_creator_limit":2,"accounts":[account]})

    def test_settings_normalize_and_dedupe_accounts(self):
        got = wf.validate_settings({"report_budget_usd":"3.25","per_creator_limit":2,
                                    "accounts":["@Creator.Name","https://www.instagram.com/other/"],"save_consent":False})
        self.assertEqual(got["accounts"], ["creator.name","other"])
        with self.assertRaises(wf.ContractError):
            wf.validate_settings({"report_budget_usd":3,"per_creator_limit":2,"accounts":["x","@X"]})

    def test_missing_profile_schema_is_interface_error_not_empty(self):
        with self.assertRaisesRegex(wf.ContractError, "interface_error"):
            wf.select_posts([synthetic_run("synthetic-run",["a"],[],1)], ["a"], 2, START, END, None)
        with self.assertRaisesRegex(wf.ContractError, "lacks a required"):
            wf.select_posts([synthetic_run("synthetic-run",["a"],[{"creator":"a"}],1)], ["a"], 2, START, END, POST_CONTRACT)

    def test_latest_per_creator_and_profile_posturl_normalization(self):
        rows = [
            post("one", created="2026-11-05T10:00:00Z", url="https://instagram.com/reels/one?utm_source=x"),
            post("two", created="2026-11-05T11:00:00Z", url="https://www.instagram.com/reel/two/"),
            post("three", created="2026-11-05T09:00:00Z"),
            post("four", creator="b", created="2026-11-05T11:00:00Z")]
        contract = dict(POST_CONTRACT, url="postUrl")
        for row in rows:
            row["postUrl"] = row.pop("url")
        got = select(rows, ["a","b"], 2, contract, False, usernames=["a","b"])
        a = [x["url"] for x in got["selected"] if x["creator"] == "a"]
        self.assertEqual(a, ["https://www.instagram.com/reel/two/","https://www.instagram.com/reel/one/"])
        self.assertEqual(got["counts"]["a"]["omitted_by_cap_observed"], 1)
        self.assertTrue(got["counts"]["a"]["additional_candidates_unknown"])
        submitted = [x for x in got["selected"] if x["row"]["creator"] == "a"][:1]
        matched = wf.reconcile_transcripts(submitted,[{"url":"https://instagram.com/reels/two/?igshid=share","text":"actual words","pk":"two"}],"SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual(matched[0]["status"], "success")

    def test_exclusive_end_and_out_of_window_rows(self):
        rows = [post("in"), post("at-end", created=END),
                post("outside", created="2026-11-06T00:00:01Z"),
                post("photo", created="2026-11-05T12:00:00Z")]
        rows[-1]["kind"] = "image"
        got = select(rows, ["a"], 5)
        self.assertEqual([x["row"]["stable"] for x in got["selected"]], ["in"])
        self.assertEqual(got["counts"]["a"]["out_of_window"], 2)
        self.assertEqual(got["counts"]["a"]["non_video"], 1)

    def test_top_level_selection_status_distinguishes_empty_partial_and_interface_error(self):
        empty = select([], ["a"], 2)
        self.assertEqual(empty["status"],"no_candidates")
        self.assertEqual(empty["coverage_status"],"complete")
        self.assertEqual(empty["counts"]["a"]["coverage_status"],"complete")
        partial = select([post("a")], ["a"], 2, retrieval_complete=False)
        self.assertEqual(partial["status"],"partial")
        malformed = [post("a"),post("b",creator="not-requested")]
        result = select(malformed,["a"],2)
        self.assertEqual(result["status"],"partial_interface_error")
        self.assertEqual(result["row_interface_error_count"],1)
        self.assertEqual(result["unresolved"][0]["status"],"interface_error")
        self.assertNotEqual(result["coverage_status"],"complete")

    def test_identity_conflicts_reduce_top_and_attributable_creator_coverage(self):
        stable_id_conflict = [post("one", stable="shared"), post("two", stable="shared")]
        by_id = select(stable_id_conflict, ["a"], 3)
        self.assertEqual(by_id["unresolved"][-1]["status"], "identity_conflict")
        self.assertTrue(by_id["unresolved"][-1]["reason"])
        self.assertEqual(by_id["identity_conflict_count"], 1)
        self.assertEqual(by_id["coverage_status"], "partial")
        self.assertEqual(by_id["counts"]["a"]["coverage_status"], "partial")

        same_url_two_authors = [post("same", creator="a"), post("same", creator="b")]
        by_author = select(same_url_two_authors, ["a", "b"], 3, usernames=["a", "b"])
        self.assertEqual(by_author["unresolved"][-1]["status"], "identity_conflict")
        self.assertTrue(by_author["unresolved"][-1]["reason"])
        self.assertNotEqual(by_author["coverage_status"], "complete")
        self.assertNotEqual(by_author["counts"]["a"]["coverage_status"], "complete")
        self.assertNotEqual(by_author["counts"]["b"]["coverage_status"], "complete")

    def test_unattributed_row_error_is_unknown_without_degrading_unrelated_author(self):
        rows = [post("ok", creator="a"), post("bad", creator="unexpected")]
        got = select(rows, ["a"], 3)
        self.assertEqual(got["status"], "partial_interface_error")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertEqual(got["counts"]["a"]["coverage_status"], "complete")
        self.assertEqual(got["unresolved"][-1]["status"], "interface_error")
        self.assertEqual(got["unattributed_issue_count"], 1)

    def test_complete_unconflicted_candidates_keep_complete_status(self):
        got = select([post("valid")], ["a"], 3)
        self.assertEqual(got["status"], "complete")
        self.assertEqual(got["coverage_status"], "complete")
        self.assertEqual(got["counts"]["a"]["coverage_status"], "complete")

    def test_requested_creator_without_discovery_run_is_unknown_not_complete(self):
        run_a = synthetic_run("synthetic-a", ["a"], [], 3)
        got = wf.select_posts([run_a], ["a", "b"], 2, START, END, POST_CONTRACT)
        self.assertEqual(got["status"], "partial_interface_error")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertEqual(got["counts"]["a"]["coverage_status"], "complete")
        self.assertFalse(got["counts"]["a"]["additional_candidates_unknown"])
        self.assertEqual(got["counts"]["b"]["coverage_status"], "unknown")
        self.assertTrue(got["counts"]["b"]["additional_candidates_unknown"])
        self.assertIsNone(got["counts"]["b"]["possible_results_limit_reached"])
        self.assertEqual(got["counts"]["b"]["run_coverage"], [])

    def test_empty_run_list_returns_stable_unknown_state_for_every_creator(self):
        got = wf.select_posts([], ["a", "b"], 2, START, END, POST_CONTRACT)
        self.assertEqual(got["status"], "partial_interface_error")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertEqual(set(got["counts"]), {"a", "b"})
        for creator in ("a", "b"):
            with self.subTest(creator=creator):
                self.assertEqual(got["counts"][creator]["coverage_status"], "unknown")
                self.assertTrue(got["counts"][creator]["additional_candidates_unknown"])
                self.assertIsNone(got["counts"][creator]["possible_results_limit_reached"])
                self.assertEqual(got["counts"][creator]["run_coverage"], [])

    def test_all_requested_creators_with_successful_empty_runs_are_complete(self):
        runs = [synthetic_run("synthetic-a", ["a"], [], 3),
                synthetic_run("synthetic-b", ["b"], [], 3)]
        got = wf.select_posts(runs, ["a", "b"], 2, START, END, POST_CONTRACT)
        self.assertEqual(got["status"], "no_candidates")
        self.assertEqual(got["coverage_status"], "complete")
        for creator in ("a", "b"):
            self.assertEqual(got["counts"][creator]["coverage_status"], "complete")
            self.assertFalse(got["counts"][creator]["additional_candidates_unknown"])
            self.assertEqual(len(got["counts"][creator]["run_coverage"]), 1)

    def test_discovery_run_status_controls_empty_result_and_failure_coverage(self):
        no_posts = synthetic_run("synthetic-empty", ["a"], [], 3, True, run_status="SUCCEEDED")
        successful_empty = wf.select_posts([no_posts], ["a"], 2, START, END, POST_CONTRACT)
        self.assertEqual(successful_empty["status"], "no_candidates")
        self.assertEqual(successful_empty["coverage_status"], "complete")

        for failed_status in ("FAILED", "ABORTED", "TIMED-OUT"):
            with self.subTest(failed_status=failed_status):
                failed = synthetic_run("synthetic-failed", ["a"], [], 3, True,
                                       run_status=failed_status, run_error="synthetic failure")
                result = wf.select_posts([failed], ["a"], 2, START, END, POST_CONTRACT)
                self.assertNotEqual(result["status"], "no_candidates")
                self.assertNotEqual(result["coverage_status"], "complete")
                self.assertEqual(result["run_failures"][0]["run_id"], "synthetic-failed")
                self.assertEqual(result["run_failures"][0]["usernames"], ["a"])
                self.assertEqual(result["run_failures"][0]["run_status"], failed_status)
                self.assertEqual(result["run_failures"][0]["error"], "synthetic failure")
                self.assertEqual(result["counts"]["a"]["coverage_status"], "partial")

    def test_missing_or_unknown_discovery_run_status_fails_closed(self):
        missing = synthetic_run("synthetic-missing", ["a"], [], 3)
        del missing["run_status"]
        unknown = synthetic_run("synthetic-unknown", ["a"], [], 3, run_status="SURPRISE")
        for run in (missing, unknown):
            result = wf.select_posts([run], ["a"], 2, START, END, POST_CONTRACT)
            self.assertNotEqual(result["status"], "no_candidates")
            self.assertEqual(result["coverage_status"], "unknown")
            self.assertTrue(result["counts"]["a"]["additional_candidates_unknown"])
            self.assertIn(result["run_coverage"][0]["coverage_status"], {"run_status_unknown"})

    def test_mixed_success_and_failed_discovery_runs_preserve_candidates_and_failures(self):
        good = synthetic_run("synthetic-good", ["a"], [post("found")], 3)
        failed = synthetic_run("synthetic-bad", ["b"], [], 3, True,
                               run_status="FAILED", run_error="synthetic failed")
        got = wf.select_posts([good, failed], ["a", "b"], 3, START, END, POST_CONTRACT)
        self.assertEqual(len(got["selected"]), 1)
        self.assertEqual(got["selected"][0]["creator"], "a")
        self.assertEqual(got["counts"]["a"]["coverage_status"], "complete")
        self.assertEqual(got["counts"]["b"]["coverage_status"], "partial")
        self.assertEqual(got["coverage_status"], "partial")
        self.assertEqual(got["run_failures"][0]["run_id"], "synthetic-bad")

    def test_results_limit_boundary_is_possible_truncation_not_a_claim(self):
        rows=[post("a")]
        got=select(rows,["a"],2,results_limit=1)
        self.assertEqual(got["status"],"partial")
        self.assertTrue(got["possible_results_limit_reached"])
        self.assertTrue(got["counts"]["a"]["additional_candidates_unknown"])
        self.assertEqual(got["counts"]["a"]["discovered_returned_in_window"],1)

    def test_results_limit_is_checked_separately_for_each_synthetic_run(self):
        runs = [synthetic_run("synthetic-run-a",["a"],[post("a")],2),
                synthetic_run("synthetic-run-b",["b"],[post("b",creator="b")],2)]
        got = wf.select_posts(runs,["a","b"],2,START,END,POST_CONTRACT)
        self.assertEqual([run["raw_returned_rows"] for run in got["run_coverage"]],[1,1])
        self.assertEqual([run["coverage_status"] for run in got["run_coverage"]],
                         ["returned_below_run_limit","returned_below_run_limit"])
        self.assertFalse(got["possible_results_limit_reached"])
        self.assertFalse(got["counts"]["a"]["additional_candidates_unknown"])
        self.assertFalse(got["counts"]["b"]["additional_candidates_unknown"])
        self.assertEqual(got["status"],"complete")

    def test_multi_username_run_with_unverified_limit_scope_is_unknown(self):
        rows = [post("a",creator="a"),post("b",creator="b")]
        run = synthetic_run("synthetic-multi-run",["a","b"],rows,2)
        got = wf.select_posts([run],["a","b"],2,START,END,POST_CONTRACT)
        self.assertEqual(got["coverage_status"],"unknown")
        self.assertEqual(got["run_coverage"][0]["coverage_status"],
                         "possible_results_limit_reached_scope_unknown")
        self.assertTrue(got["counts"]["a"]["results_limit_scope_unknown"])
        self.assertTrue(got["counts"]["b"]["results_limit_scope_unknown"])
        self.assertIsNone(got["counts"]["a"]["possible_results_limit_reached"])
        self.assertIsNone(got["counts"]["b"]["possible_results_limit_reached"])
        self.assertTrue(got["counts"]["a"]["additional_candidates_unknown"])
        self.assertTrue(got["counts"]["b"]["additional_candidates_unknown"])

        mixed = wf.select_posts([synthetic_run("synthetic-single",["a"],[rows[0]],3),run],
                                ["a","b"],2,START,END,POST_CONTRACT)
        self.assertIsNone(mixed["counts"]["a"]["possible_results_limit_reached"])
        self.assertTrue(mixed["counts"]["a"]["results_limit_per_creator_unattributed"])

    def test_raw_out_of_window_rows_still_count_toward_synthetic_run_limit(self):
        rows = [post("in",created="2026-11-05T12:00:00Z"),
                post("old",created="2026-11-04T00:00:00Z")]
        got = select(rows,["a"],2,results_limit=2)
        self.assertEqual(got["run_coverage"][0]["raw_returned_rows"],2)
        self.assertEqual(got["counts"]["a"]["discovered_returned_in_window"],1)
        self.assertTrue(got["possible_results_limit_reached"])
        self.assertEqual(got["run_coverage"][0]["coverage_status"],"possible_results_limit_reached")

    def test_missing_run_boundary_or_limit_returns_machine_readable_unknown_coverage(self):
        no_runs = wf.select_posts([], ["a"], 2, START, END, POST_CONTRACT)
        self.assertEqual(no_runs["status"],"partial_interface_error")
        self.assertEqual(no_runs["interface_errors"][0]["code"],"missing_run_boundary")
        self.assertEqual(no_runs["coverage_status"],"unknown")

        run = synthetic_run("synthetic-run",["a"],[post("a")],2)
        del run["results_limit"]
        result = wf.select_posts([run],["a"],2,START,END,POST_CONTRACT)
        self.assertEqual(result["status"],"partial_interface_error")
        self.assertEqual(result["coverage_status"],"unknown")
        self.assertEqual(result["interface_errors"][0]["code"],"invalid_or_missing_run_metadata")
        self.assertIn("results_limit",result["interface_errors"][0]["missing"][0]["missing"])
        self.assertTrue(result["counts"]["a"]["additional_candidates_unknown"])

        run = synthetic_run("synthetic-run",["a"],[post("a")],2)
        del run["run_id"]
        result = wf.select_posts([run],["a"],2,START,END,POST_CONTRACT)
        self.assertEqual(result["interface_errors"][0]["code"],"invalid_or_missing_run_metadata")
        self.assertIn("run_id",result["interface_errors"][0]["missing"][0]["missing"])

    def test_missing_run_to_creator_mapping_never_reports_complete(self):
        result = wf.select_posts([synthetic_run("synthetic-run",["a"],[post("a")],2)],
                                 ["a","b"],2,START,END,POST_CONTRACT)
        self.assertEqual(result["status"],"partial_interface_error")
        self.assertEqual(result["coverage_status"],"unknown")
        self.assertEqual(result["interface_errors"][0]["missing"][0]["usernames"],["b"])

    def test_duplicate_candidates_do_not_consume_cap_and_conflict_visible(self):
        rows = [post("same"), post("same", url="https://instagram.com/reels/same/?igshid=tracking"),
                post("same", creator="b")]
        got = select(rows, ["a","b"], 1, usernames=["a","b"])
        self.assertEqual(len(got["selected"]), 1)
        self.assertEqual(got["unresolved"][0]["status"], "duplicate_candidate")
        self.assertEqual(got["unresolved"][1]["status"], "identity_conflict")

    def test_post_with_no_transcript_row_remains_accounted(self):
        submitted = [{"url":wf.canonical_post_url("https://instagram.com/reels/a?igshid=x"),"stable_id":"pk-a","creator":"a"}]
        got = wf.reconcile_transcripts(submitted, [], "SUCCEEDED", True, POST_CONTRACT, TRANSCRIPT_CONTRACT)
        self.assertEqual(got[0]["status"], "not_returned")
        self.assertEqual(got[0]["post"]["creator"], "a")

    def test_posturl_transcript_url_variants_and_stable_id_fallback(self):
        postrow = {"url":wf.canonical_post_url("https://www.instagram.com/reel/a/"),"stable_id":"pk-a","creator":"a"}
        via_url = wf.reconcile_transcripts([postrow],[{"url":"https://instagram.com/reels/a/?utm_source=feed","text":"words","pk":"pk-a"}],"SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual(via_url[0]["status"], "success")
        via_id = wf.reconcile_transcripts([postrow],[{"url":None,"text":"words","pk":"pk-a"}],"SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual(via_id[0]["status"], "success")
        mismatch = wf.reconcile_transcripts([postrow],[{"url":"https://instagram.com/reel/a/","text":"words","pk":"wrong"}],"SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual(mismatch[0]["status"], "identity_conflict")

    def test_transcript_url_author_and_stable_id_conflicts_never_succeed(self):
        post_a={"url":"https://www.instagram.com/reel/a/","stable_id":"id-a","creator":"a"}
        post_b={"url":"https://www.instagram.com/reel/b/","stable_id":"id-b","creator":"a"}
        # URL points to B while stable ID points to A: mark both, never attribute text to A.
        url_id_conflict=wf.reconcile_transcripts([post_a,post_b],[
            {"url":post_b["url"],"pk":"id-a","userName":"a","text":"wrong mapping"}],
            "SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual({x["status"] for x in url_id_conflict if "post" in x},{"identity_conflict"})
        self.assertNotIn("success",{x["status"] for x in url_id_conflict})
        # URL and ID agree but the returned author does not.
        author_conflict=wf.reconcile_transcripts([post_a],[
            {"url":post_a["url"],"pk":"id-a","userName":"other","text":"wrong author"}],
            "SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual(author_conflict[0]["status"],"identity_conflict")
        # URL points to A but an unknown/different stable ID must not be accepted.
        id_conflict=wf.reconcile_transcripts([post_a],[
            {"url":post_a["url"],"pk":"wrong-id","userName":"a","text":"wrong id"}],
            "SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual(id_conflict[0]["status"],"identity_conflict")
        consistent=wf.reconcile_transcripts([post_a],[
            {"url":post_a["url"],"pk":"id-a","userName":"a","text":"matching words"}],
            "SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual(consistent[0]["status"],"success")

    def test_missing_rows_are_pending_when_dataset_incomplete(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        got = wf.reconcile_transcripts([postrow], [], "RUNNING", False, POST_CONTRACT, TRANSCRIPT_CONTRACT)
        self.assertEqual(got[0]["status"], "pending")

    def test_text_empty_missing_invalid_and_segments_are_distinct(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        states = []
        for row in ({"url":postrow["url"],"text":""},
                    {"url":postrow["url"]},
                    {"url":postrow["url"],"text":None},
                    {"url":postrow["url"],"segments":[{"text":"spoken"},{"text":"words"}]}):
            result = wf.reconcile_transcripts([postrow],[row],"SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)[0]
            states.append((result["status"],result.get("transcript")))
        self.assertEqual(states, [("empty",""),("schema_missing_text",None),("schema_invalid",None),("segments_only",None)])

    def test_duplicate_transcript_rows_and_unmatched_are_explicit(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        got = wf.reconcile_transcripts([postrow],[{"url":postrow["url"],"text":"one","pk":"a"},
            {"url":postrow["url"],"text":"two","pk":"a"},
            {"url":"https://www.instagram.com/reel/unknown/","text":"orphan"}],"SUCCEEDED",True,POST_CONTRACT,TRANSCRIPT_CONTRACT)
        self.assertEqual(got[0]["status"], "duplicate_transcript_rows")
        self.assertEqual(len(got[0]["rows"]), 2)
        self.assertEqual(got[1]["status"], "unmatched")

    def test_zero_budget_is_never_an_actor_option(self):
        with self.assertRaises(wf.ContractError):
            wf.plan_budget_stage({"report_budget_usd":"0.00","per_creator_limit":1,"accounts":["a"]},
                                 "discovery", [{"actor":"a/b","input":{},"wait_secs":1,
                                 "pricing":pricing("pay_per_event")}], OFFLINE_HOST_CONTRACT)

    def test_budget_is_planned_in_two_stages_and_reservations_accumulate(self):
        settings = {"report_budget_usd":"1.00","per_creator_limit":2,"accounts":["a"],"save_consent":False}
        discovery = wf.plan_budget_stage(settings,"discovery",[
            {"actor":"owner/profile","input":{"usernames":["a"],"resultsLimit":4},"wait_secs":45,
             "pricing":pricing("pay_per_result","0.10"),"billable_items_requested":4}],OFFLINE_HOST_CONTRACT)
        self.assertEqual(discovery["stage_reserved_cents"],40)
        planned = discovery["calls"][0]
        self.assertEqual(planned["tool_call"]["name"],"call-actor")
        self.assertEqual(set(planned["tool_call"]["arguments"]),{"actor","input","waitSecs","callOptions"})
        self.assertEqual(planned["tool_call"]["arguments"]["callOptions"],{"maxItems":4})
        self.assertEqual(planned["tool_call"]["arguments"]["input"]["resultsLimit"],4)
        self.assertEqual(planned["planning"]["billing_model"],"pay_per_result")
        self.assertNotIn("planning",planned["tool_call"]["arguments"])

        # Transcript batches are planned only after discovery provides the URLs.
        transcript_urls = ["https://instagram.com/reel/one/","https://instagram.com/reel/two/"]
        transcript_runs = [{"actor":"owner/transcript","input":{"bulkUrls":[url]},"wait_secs":0,
                            "pricing":pricing("pay_per_event")} for url in transcript_urls]
        transcript = wf.plan_budget_stage(settings,"transcription",transcript_runs,OFFLINE_HOST_CONTRACT,discovery["ledger"])
        self.assertEqual([c["tool_call"]["arguments"]["callOptions"] for c in transcript["calls"]],
                         [{"maxTotalChargeUsd":"0.30"},{"maxTotalChargeUsd":"0.30"}])
        self.assertEqual(transcript["reserved_cents"],100)
        self.assertEqual(sum(stage["reserved_cents"] for stage in transcript["ledger"]["stages"]),100)
        self.assertEqual(transcript["state"],"offline_plan_not_executed")

    def test_stage_budget_shortfall_fails_without_expanding_prior_reservation(self):
        settings = {"report_budget_usd":"0.05","per_creator_limit":2,"accounts":["a"]}
        discovery = wf.plan_budget_stage(settings,"discovery",[
            {"actor":"owner/profile","input":{"usernames":["a"]},"wait_secs":1,
             "pricing":pricing("pay_per_event","0.01")}],OFFLINE_HOST_CONTRACT)
        self.assertEqual(discovery["reserved_cents"],1)
        # One observed transcript candidate still cannot fit its minimum run reserve.
        transcript_runs = [{"actor":"owner/transcript","input":{"bulkUrls":["url"]},"wait_secs":1,
                            "pricing":pricing("pay_per_event",minimum="0.10")}]
        with self.assertRaisesRegex(wf.ContractError,"budget_blocked"):
            wf.plan_budget_stage(settings,"transcription",transcript_runs,OFFLINE_HOST_CONTRACT,discovery["ledger"])

    def test_missing_live_host_or_readback_contract_fails_closed(self):
        settings = {"report_budget_usd":"1.00","per_creator_limit":1,"accounts":["a"]}
        run = [{"actor":"owner/profile","input":{},"wait_secs":1,"pricing":pricing("pay_per_event")}]
        for contract in ({}, {**OFFLINE_HOST_CONTRACT,"run_readback":None},
                         {**OFFLINE_HOST_CONTRACT,"run_readback":{**OFFLINE_HOST_CONTRACT["run_readback"],"verified":False}}):
            with self.subTest(contract=contract), self.assertRaisesRegex(wf.ContractError,"budget_blocked"):
                wf.plan_budget_stage(settings,"discovery",run,contract)

    def test_run_readback_uses_only_a_verified_declared_tool_and_exact_run(self):
        # The host contract and options-bearing response below are synthetic mocks only.
        settings = {"report_budget_usd":"1.00","per_creator_limit":1,"accounts":["a"]}
        plan = wf.plan_budget_stage(settings,"discovery",[
            {"actor":"owner/profile","input":{},"wait_secs":1,"pricing":pricing("pay_per_event")}],OFFLINE_HOST_CONTRACT)
        call = plan["calls"][0]
        expected = call["tool_call"]["arguments"]["callOptions"]
        response = {"items":[{"id":"run-1","options":expected}]}
        self.assertEqual(wf.verify_run_limit(call,response,"run-1",OFFLINE_HOST_CONTRACT)["state"],"budget_readback_verified")
        self.assertTrue(wf.verify_run_limit(call,{"items":[]},"run-1",OFFLINE_HOST_CONTRACT)["stop_subsequent_runs"])
        wrong = {"items":[{"id":"run-1","options":{"maxTotalChargeUsd":"0.99"}}]}
        self.assertEqual(wf.verify_run_limit(call,wrong,"run-1",OFFLINE_HOST_CONTRACT)["state"],"budget_readback_mismatch")

    def test_waitsecs_contract_accepts_only_zero_through_45(self):
        settings = {"report_budget_usd":"1.00","per_creator_limit":1,"accounts":["a"]}
        for value in (0,45):
            run = [{"actor":"owner/profile","input":{},"wait_secs":value,"pricing":pricing("pay_per_event")}]
            self.assertEqual(wf.plan_budget_stage(settings,"discovery",run,OFFLINE_HOST_CONTRACT)["calls"][0]
                             ["tool_call"]["arguments"]["waitSecs"],value)
        for value in (-1,46):
            run = [{"actor":"owner/profile","input":{},"wait_secs":value,"pricing":pricing("pay_per_event")}]
            with self.subTest(wait_secs=value), self.assertRaisesRegex(wf.ContractError,"wait_secs"):
                wf.plan_budget_stage(settings,"discovery",run,OFFLINE_HOST_CONTRACT)

    def test_unknown_pricing_fails_closed_and_maxitems_is_distinct_from_resultslimit(self):
        run = {"actor":"owner/profile","input":{"resultsLimit":10},"wait_secs":30,
               "pricing":pricing("pay_per_result","0.01"),"billable_items_requested":2}
        plan = wf.plan_budget_stage({"report_budget_usd":"1.00","per_creator_limit":2,"accounts":["a"]},
                                   "discovery",[run],OFFLINE_HOST_CONTRACT)
        self.assertEqual(plan["calls"][0]["tool_call"]["arguments"]["input"]["resultsLimit"],10)
        self.assertEqual(plan["calls"][0]["tool_call"]["arguments"]["callOptions"],{"maxItems":2})
        run["pricing"]["verified"] = False
        with self.assertRaisesRegex(wf.ContractError,"pricing_unverified"):
            wf.plan_budget_stage({"report_budget_usd":"1.00","per_creator_limit":2,"accounts":["a"]},
                                 "discovery",[run],OFFLINE_HOST_CONTRACT)

    def test_batch_splitting_uses_verified_limit_and_remaining_budget(self):
        self.assertEqual(wf.split_batches(["a","b","c","d","e"],2),[["a","b"],["c","d"],["e"]])
        self.assertEqual(wf.remaining_budget("2.50","2.50"),0)
        with self.assertRaises(wf.ContractError):
            wf.split_batches(["a"],0)

    def test_reconcile_requires_compatible_stable_id_contracts(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        wrong = dict(TRANSCRIPT_CONTRACT, post_id_kind="code")
        with self.assertRaisesRegex(wf.ContractError, "kinds differ"):
            wf.reconcile_transcripts([postrow], [], "SUCCEEDED", True, POST_CONTRACT, wrong)
        with self.assertRaisesRegex(wf.ContractError, "Profile Posts output field contract"):
            wf.reconcile_transcripts([postrow], [], "SUCCEEDED", True, None, TRANSCRIPT_CONTRACT)
        with self.assertRaisesRegex(wf.ContractError, "stable-ID kind"):
            wf.reconcile_transcripts([postrow], [], "SUCCEEDED", True, POST_CONTRACT,
                                     dict(TRANSCRIPT_CONTRACT, post_id_kind=None))
        compatible = wf.reconcile_transcripts([postrow], [], "SUCCEEDED", True, POST_CONTRACT, TRANSCRIPT_CONTRACT)
        self.assertEqual(compatible[0]["status"], "not_returned")

    def test_media_values_are_case_insensitive_and_unknowns_are_auditable(self):
        rows = [post("upper", created="2026-11-05T13:00:00Z"),
                post("photo", created="2026-11-05T12:00:00Z"),
                post("new", created="2026-11-05T11:00:00Z")]
        rows[0]["kind"] = "REEL"
        rows[1]["kind"] = "IMAGE"
        rows[2]["kind"] = "short_video_v2"
        got = select(rows, ["a"], 5)
        self.assertEqual(got["status"], "partial_interface_error")
        self.assertEqual(len(got["selected"]), 1)
        self.assertEqual(got["counts"]["a"]["non_video"], 1)
        self.assertEqual(got["counts"]["a"]["unknown_media_type"], 1)
        self.assertFalse(got["counts"]["a"]["additional_candidates_unknown"])
        self.assertEqual([u["status"] for u in got["unresolved"]], ["non_video", "unknown_media_type"])

    def test_cli_stdin_json_executes_complete_offline_report_chain(self):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        def invoke(payload):
            proc = subprocess.run([sys.executable, str(PATH)], input=json.dumps(payload), text=True,
                                  capture_output=True, env=env, check=False)
            self.assertEqual(proc.stderr, "")
            try:
                result = json.loads(proc.stdout)
            except json.JSONDecodeError as exc:
                self.fail(f"CLI did not emit JSON: {exc}: {proc.stdout!r}")
            return proc.returncode, result

        code, settings = invoke({"operation":"settings", "settings":{"report_budget_usd":"1.20",
            "per_creator_limit":1,"accounts":["@a"],"save_consent":False}})
        self.assertEqual(code, 0)
        self.assertEqual(settings["accounts"], ["a"])
        code, bounds = invoke({"operation":"window","now":"2026-11-06T00:00:00Z","mode":"daily"})
        self.assertEqual(code, 0)
        selected_input = {"operation":"select","runs":[synthetic_run("synthetic-profile-run",["a"],
            [post("a",created="2026-11-05T23:00:00Z")],2)],
            "accounts":settings["accounts"],"per_creator_limit":settings["per_creator_limit"],
            "start":bounds["start_utc"],"end_exclusive":bounds["end_utc_exclusive"],
            "post_contract":POST_CONTRACT}
        code, selected = invoke(selected_input)
        self.assertEqual(code, 0)
        self.assertEqual(selected["status"], "complete")
        self.assertEqual(len(selected["selected"]), 1)
        code, discovery = invoke({"operation":"plan_stage","stage":"discovery","settings":settings,"runs":[
                {"actor":"owner/profile","input":{"usernames":["a"],"resultsLimit":1},"wait_secs":45,
                 "pricing":pricing("pay_per_result","0.10"),"billable_items_requested":1}],
            "host_contract":OFFLINE_HOST_CONTRACT})
        self.assertEqual(code, 0)
        self.assertEqual(len(discovery["calls"]), 1)
        self.assertEqual(set(discovery["calls"][0]["tool_call"]["arguments"]),
                         {"actor","input","waitSecs","callOptions"})
        code, transcript = invoke({"operation":"plan_stage","stage":"transcription","settings":settings,
            "ledger":discovery["ledger"],"runs":[
                {"actor":"owner/transcript","input":{"bulkUrls":[selected["selected"][0]["url"]]},"wait_secs":0,
                 "pricing":pricing("pay_per_event")}],"host_contract":OFFLINE_HOST_CONTRACT})
        self.assertEqual(code,0)
        self.assertIn("maxTotalChargeUsd",transcript["calls"][0]["tool_call"]["arguments"]["callOptions"])
        code, checked = invoke({"operation":"verify_run","planned_call":transcript["calls"][0],
            "run_id":"synthetic-run","response":{"items":[{"id":"synthetic-run",
                "options":transcript["calls"][0]["tool_call"]["arguments"]["callOptions"]}]},
            "host_contract":OFFLINE_HOST_CONTRACT})
        self.assertEqual(code,0)
        self.assertEqual(checked["state"],"budget_readback_verified")
        code, batches = invoke({"operation":"split","urls":[selected["selected"][0]["url"]],"batch_size":1})
        self.assertEqual(code, 0)
        self.assertEqual(batches["batches"], [[selected["selected"][0]["url"]]])
        code, reconciled = invoke({"operation":"reconcile","submitted":selected["selected"],
            "rows":[{"url":selected["selected"][0]["url"],"pk":"a","text":"spoken words"}],
            "run_status":"SUCCEEDED","dataset_complete":True,"post_contract":POST_CONTRACT,
            "transcript_contract":TRANSCRIPT_CONTRACT})
        self.assertEqual(code, 0)
        self.assertEqual(reconciled["results"][0]["status"], "success")

        for payload, expected in (({"operation":"unknown"}, "unknown operation"),
                                  ({"operation":"settings","settings":{"report_budget_usd":0,
                                    "per_creator_limit":1,"accounts":["a"]}}, "greater than zero")):
            code, error = invoke(payload)
            self.assertEqual(code, 2)
            self.assertIn("error", error)
            self.assertIn(expected, error["error"])

if __name__ == "__main__":
    unittest.main()

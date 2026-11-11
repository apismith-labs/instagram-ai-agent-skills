import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import unittest
from datetime import datetime, timezone

PATH = pathlib.Path(__file__).parents[1] / "skills/instagram-creator-reels-insights/scripts/workflow.py"
SPEC = importlib.util.spec_from_file_location("creator_workflow", PATH)
wf = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wf)

POST_CONTRACT = {"creator":"creator","url":"url","timestamp":"created","timestamp_unit":"unix_seconds","type":"kind","id":"stable","id_kind":"pk","video_values":["Video"],"non_video_values":[]}
TRANSCRIPT_CONTRACT = {"url":"url","code":"code","pk":"pk","creator":"userName","text":"text","segments":"segments","error":"errMsg","segment_text":"text","post_id_kind":"pk"}
START, END = "2026-11-05T00:00:00Z", "2026-11-06T00:00:00Z"

def post(code, creator="a", created=START, url=None, stable=None):
    return {"creator":creator,"url":url or f"https://www.instagram.com/reel/{code}/",
            "created":created,"kind":"Video","stable":stable or code}

def synthetic_run(run_id, usernames, posts, results_limit, retrieval_complete=True, **extra):
    """Synthetic Profile Posts run envelope for offline tests; not Actor evidence."""
    if retrieval_complete is True and "retrieval_complete_evidence" not in extra:
        extra["retrieval_complete_evidence"] = {
            "source":"synthetic_fixture", "detail":"synthetic fixture includes all declared rows"}
    return {"run_id":run_id,"usernames":usernames,"posts":posts,"results_limit":results_limit,
            "retrieval_complete":retrieval_complete,"run_status":"SUCCEEDED",**extra}

def select(posts, accounts, cap, contract=POST_CONTRACT, retrieval_complete=True,
           results_limit=None, usernames=None, run_id="synthetic-run", display_timezone="UTC", **run_extra):
    limit = results_limit if results_limit is not None else max(1,len(posts)+1)
    run = synthetic_run(run_id,usernames or accounts,posts,limit,retrieval_complete,**run_extra)
    return wf.select_posts([run],accounts,cap,START,END,contract,display_timezone)

class CreatorWorkflowTests(unittest.TestCase):
    def test_rolling_windows_use_exclusive_upper_bound(self):
        self.assertEqual(wf.window("2026-11-05T12:00:00+08:00", "daily"),
                         {"start_utc":"2026-11-04T04:00:00Z","end_utc_exclusive":"2026-11-05T04:00:00Z"})
        self.assertEqual(wf.window("2026-11-05T12:00:00+08:00", "weekly")["start_utc"], "2026-10-29T04:00:00Z")

    def test_unix_seconds_publish_time_is_converted_to_utc_and_requested_timezone(self):
        epoch = int(datetime.fromisoformat("2026-01-01T23:30:00+00:00").timestamp())
        row = post("epoch", created=epoch)
        run = synthetic_run("epoch-run", ["a"], [row], 5)
        got = wf.select_posts([run], ["a"], 5, "2026-01-01T00:00:00Z",
                              "2026-01-02T00:00:00Z", POST_CONTRACT, "Asia/Shanghai")
        selected = got["selected"][0]
        self.assertEqual(selected["published_at_utc"], "2026-01-01T23:30:00Z")
        self.assertEqual(selected["published_at_local"], "2026-01-02T07:30:00+08:00")
        self.assertEqual(selected["display_timezone"], "Asia/Shanghai")

    def test_numeric_time_without_confirmed_unit_is_preserved_as_unverified(self):
        row = post("unknown-unit", created=1_767_301_800)
        contract = {key:value for key, value in POST_CONTRACT.items() if key != "timestamp_unit"}
        got = select([row], ["a"], 5, contract=contract)
        self.assertEqual(got["selected"], [])
        issue = next(item for item in got["unresolved"] if item["status"] == "timestamp_unverified")
        self.assertEqual(issue["field"], "created")
        self.assertTrue(issue["field_present"])
        self.assertEqual(issue["value"], 1_767_301_800)

    def test_timezone_display_does_not_change_window_membership(self):
        epoch = int(datetime.fromisoformat("2026-01-01T00:30:00+00:00").timestamp())
        run = synthetic_run("timezone-run", ["a"], [post("cross-day", created=epoch)], 5)
        utc = wf.select_posts([run], ["a"], 5, "2026-01-01T00:00:00Z",
                              "2026-01-02T00:00:00Z", POST_CONTRACT, "UTC")
        shanghai = wf.select_posts([run], ["a"], 5, "2026-01-01T00:00:00Z",
                                   "2026-01-02T00:00:00Z", POST_CONTRACT, "Asia/Shanghai")
        self.assertEqual([item["url"] for item in utc["selected"]],
                         [item["url"] for item in shanghai["selected"]])
        self.assertEqual(utc["selected"][0]["published_at_utc"],
                         shanghai["selected"][0]["published_at_utc"])
        self.assertEqual(shanghai["selected"][0]["published_at_local"], "2026-01-01T08:30:00+08:00")

    def test_transcript_runtime_timestamp_is_not_used_as_post_publish_time(self):
        epoch = int(datetime.fromisoformat("2026-01-01T23:30:00+00:00").timestamp())
        selected = wf.select_posts(
            [synthetic_run("publish-run", ["a"], [post("same-post", created=epoch)], 5)],
            ["a"], 5, "2026-01-01T00:00:00Z", "2026-01-02T00:00:00Z",
            POST_CONTRACT, "Asia/Shanghai")["selected"]
        transcript = {"url":selected[0]["url"], "pk":"same-post", "userName":"a",
                      "text":"spoken words", "createTime":epoch,
                      "timestamp":"2026-11-11T05:00:00Z"}
        result = wf.reconcile_transcripts(selected, [transcript], "SUCCEEDED", True,
                                          POST_CONTRACT, TRANSCRIPT_CONTRACT)[0]
        self.assertEqual(result["post"]["published_at_local"], "2026-01-02T07:30:00+08:00")
        self.assertEqual(result["row"]["timestamp"], "2026-11-11T05:00:00Z")

    def test_settings_reject_invalid_creator_cap_and_dot_path(self):
        for amount in (0, -1, True, 1.5, "2", None):
            with self.subTest(amount=amount), self.assertRaises(wf.ContractError):
                wf.validate_settings({"per_creator_limit":amount,"accounts":["a"]})
        for account in ("https://www.instagram.com/./", "https://www.instagram.com/p/short/"):
            with self.subTest(account=account), self.assertRaises(wf.ContractError):
                wf.validate_settings({"per_creator_limit":2,"accounts":[account]})

    def test_settings_normalize_and_dedupe_accounts(self):
        got = wf.validate_settings({"per_creator_limit":2,
                                    "accounts":["@Creator.Name","https://www.instagram.com/other/"],"save_consent":False})
        self.assertEqual(got["accounts"], ["creator.name","other"])
        self.assertEqual(got["per_creator_limit"], 2)
        self.assertFalse(got["save_consent"])
        self.assertNotIn("report_budget_usd", got)
        with self.assertRaises(wf.ContractError):
            wf.validate_settings({"per_creator_limit":2,"accounts":["x","@X"]})

    def test_legacy_budget_field_is_ignored_and_never_returned_as_a_setting(self):
        got = wf.validate_settings({"report_budget_usd":"not a valid amount",
                                    "per_creator_limit":3,"accounts":["a"]})
        self.assertEqual(got, {"per_creator_limit":3,"accounts":["a"],"save_consent":False})

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
        rows[-1]["kind"] = "Image"
        got = select(rows, ["a"], 5)
        self.assertEqual([x["row"]["stable"] for x in got["selected"]], ["in"])
        self.assertEqual(got["counts"]["a"]["out_of_window"], 2)
        self.assertEqual(got["counts"]["a"]["unknown_media_type"], 1)
        self.assertEqual(got["counts"]["a"]["discovered_returned_in_window"], 2)
        self.assertEqual(got["counts"]["a"]["type_video_candidates"], 1)

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

    def test_succeeded_empty_run_without_completeness_signal_is_unknown_not_no_candidates(self):
        run = synthetic_run("synthetic-no-signal-empty", ["a"], [], 5, retrieval_complete=None)
        run.pop("retrieval_complete")
        got = wf.select_posts([run], ["a"], 3, START, END, POST_CONTRACT)
        self.assertNotEqual(got["status"], "no_candidates")
        self.assertEqual(got["status"], "partial")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertEqual(got["counts"]["a"]["coverage_status"], "unknown")
        self.assertEqual(got["counts"]["a"]["selected"], 0)
        self.assertEqual(got["run_coverage"][0]["retrieval_complete"], None)

    def test_succeeded_below_limit_without_completeness_signal_keeps_candidate_unknown(self):
        run = synthetic_run("synthetic-no-signal-rows", ["a"], [post("candidate")], 5,
                            retrieval_complete=None)
        run.pop("retrieval_complete")
        got = wf.select_posts([run], ["a"], 3, START, END, POST_CONTRACT)
        self.assertEqual(len(got["selected"]), 1)
        self.assertEqual(got["selected"][0]["row"]["stable"], "candidate")
        self.assertEqual(got["status"], "partial")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertEqual(got["counts"]["a"]["coverage_status"], "unknown")
        self.assertEqual(got["run_coverage"][0]["retrieval_complete"], None)

    def test_nonempty_evidence_source_and_detail_pass_structure_check_only(self):
        run = synthetic_run("synthetic-explicit-complete", ["a"], [post("candidate")], 5,
                            retrieval_complete=True,
                            retrieval_complete_evidence={"source":"x", "detail":"y"})
        got = wf.select_posts([run], ["a"], 3, START, END, POST_CONTRACT)
        self.assertEqual(got["status"], "complete")
        self.assertEqual(got["coverage_status"], "complete")
        self.assertEqual(got["run_coverage"][0]["retrieval_complete"], True)
        self.assertEqual(got["run_coverage"][0]["retrieval_completeness_evidence"],
                         {"source":"x", "detail":"y"})

    def test_true_without_completeness_evidence_is_downgraded_to_unknown(self):
        run = synthetic_run("synthetic-unbacked-true", ["a"], [], 5,
                            retrieval_complete=True, retrieval_complete_evidence=None)
        got = wf.select_posts([run], ["a"], 3, START, END, POST_CONTRACT)
        self.assertNotEqual(got["status"], "no_candidates")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertIsNone(got["run_coverage"][0]["retrieval_complete"])
        self.assertEqual(got["run_coverage"][0]["retrieval_completeness_evidence"]["status"],
                         "missing_or_unverifiable")

    def test_completeness_evidence_shape_requires_nonempty_source_and_detail(self):
        invalid_evidence = ["source/detail", {}, {"detail":"read all pages"},
                            {"source":"tool"}, {"source":"  ","detail":"pages read"},
                            {"source":"tool","detail":"  "}]
        for evidence in invalid_evidence:
            with self.subTest(evidence=evidence):
                run = synthetic_run("synthetic-invalid-evidence", ["a"], [], 5,
                                    retrieval_complete=True, retrieval_complete_evidence=evidence)
                got = wf.select_posts([run], ["a"], 3, START, END, POST_CONTRACT)
                self.assertEqual(got["coverage_status"], "unknown")
                self.assertNotEqual(got["status"], "no_candidates")
                self.assertIsNone(got["run_coverage"][0]["retrieval_complete"])

    def test_unknown_completeness_for_one_creator_does_not_degrade_another(self):
        unknown = synthetic_run("synthetic-a-unknown", ["a"], [post("a-row")], 5,
                                retrieval_complete=None)
        explicit = synthetic_run("synthetic-b-complete", ["b"], [post("b-row", creator="b")], 5,
                                 retrieval_complete=True,
                                 retrieval_complete_evidence={"source":"synthetic page ledger",
                                                              "detail":"all fixture pages supplied"})
        got = wf.select_posts([unknown, explicit], ["a", "b"], 2, START, END, POST_CONTRACT)
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertEqual(got["counts"]["a"]["coverage_status"], "unknown")
        self.assertEqual(got["counts"]["b"]["coverage_status"], "complete")
        self.assertEqual({row["creator"] for row in got["selected"]}, {"a", "b"})

    def test_workflow_reference_matches_tri_state_completeness_contract(self):
        reference = (PATH.parent.parent / "references/workflow.md").read_text()
        self.assertIn("retrieval_complete` is tri-state", reference)
        self.assertIn("retrieval_complete_evidence", reference)
        self.assertIn("never infer it from `SUCCEEDED`", reference)
        self.assertIn("A `reconcile` row status of `success` means only", reference)

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
        self.assertEqual(got["run_failures"], [])
        self.assertEqual(got["identity_conflict_count"], 0)
        self.assertIsInstance(got["run_failures"], list)
        self.assertIsInstance(got["identity_conflict_count"], int)
        self.assertEqual(got["unattributed_issue_count"], 0)
        self.assertIsInstance(got["unattributed_issue_count"], int)

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
        self.assertEqual(got["run_failures"], [])
        self.assertEqual(got["identity_conflict_count"], 0)
        self.assertIsInstance(got["run_failures"], list)
        self.assertIsInstance(got["identity_conflict_count"], int)
        self.assertEqual(got["unattributed_issue_count"], 0)
        self.assertIsInstance(got["unattributed_issue_count"], int)
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
                self.assertEqual(set(result["run_failures"][0]), {
                    "run_id", "usernames", "row_attributed_usernames", "run_status", "error",
                    "status_message", "coverage_status"})
                self.assertEqual(result["counts"]["a"]["coverage_status"], "partial")

    def test_missing_or_unknown_discovery_run_status_fails_closed(self):
        missing = synthetic_run("synthetic-missing", ["a"], [], 3)
        del missing["run_status"]
        unknown = synthetic_run("synthetic-unknown", ["a"], [], 3, run_status="SURPRISE")
        for run in (missing, unknown):
            result = wf.select_posts([run], ["a"], 2, START, END, POST_CONTRACT)
            self.assertNotEqual(result["status"], "no_candidates")
            self.assertEqual(result["coverage_status"], "unknown")
            self.assertEqual(result["run_failures"], [])
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

    def test_failed_discovery_run_keeps_valid_rows_transcribable_but_partial(self):
        valid = post("failed-run-valid", creator="a")
        unknown_media = post("failed-run-unknown", creator="a")
        unknown_media["kind"] = "unverified_kind"
        wrong_author = post("failed-run-wrong-author", creator="not-requested")
        failed = synthetic_run("synthetic-failed-with-rows", ["a"],
            [valid, unknown_media, wrong_author], 5, True,
            run_status="FAILED", run_error="synthetic partial failure")

        got = wf.select_posts([failed], ["a"], 3, START, END, POST_CONTRACT)

        self.assertEqual(got["status"], "partial_interface_error")
        self.assertIn(got["coverage_status"], {"partial", "unknown"})
        self.assertIn(got["counts"]["a"]["coverage_status"], {"partial", "unknown"})
        self.assertEqual(len(got["selected"]), 1)
        self.assertEqual(got["selected"][0]["row"], valid)
        self.assertEqual(got["selected"][0]["source_run_id"], "synthetic-failed-with-rows")
        self.assertEqual(got["selected"][0]["source_run_index"], 0)
        self.assertEqual({item["status"] for item in got["unresolved"]},
                         {"unknown_media_type", "interface_error"})

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
        self.assertEqual(result["run_failures"], [])
        self.assertEqual(result["identity_conflict_count"], 0)
        self.assertIsInstance(result["run_failures"], list)
        self.assertIsInstance(result["identity_conflict_count"], int)
        self.assertEqual(result["unattributed_issue_count"], 1)
        self.assertIsInstance(result["unattributed_issue_count"], int)
        self.assertIn("results_limit",result["interface_errors"][0]["missing"][0]["missing"])
        self.assertTrue(result["counts"]["a"]["additional_candidates_unknown"])
        self.assertEqual(result["unresolved"][0]["row"], run["posts"][0])
        self.assertEqual(result["unresolved"][0]["run_id"], "synthetic-run")
        self.assertEqual(result["unresolved"][0]["run_index"], 0)
        self.assertTrue(result["unresolved"][0]["reason"])
        self.assertEqual(result["unattributed_issue_count"], 1)

        run = synthetic_run("synthetic-run",["a"],[post("a")],2)
        del run["run_id"]
        result = wf.select_posts([run],["a"],2,START,END,POST_CONTRACT)
        self.assertEqual(result["interface_errors"][0]["code"],"invalid_or_missing_run_metadata")
        self.assertIn("run_id",result["interface_errors"][0]["missing"][0]["missing"])
        self.assertEqual(result["unresolved"][0]["row"], run["posts"][0])
        self.assertIsNone(result["unresolved"][0]["run_id"])
        self.assertEqual(result["unresolved"][0]["run_index"], 0)
        self.assertTrue(result["unresolved"][0]["reason"])

    def test_missing_run_to_creator_mapping_never_reports_complete(self):
        result = wf.select_posts([synthetic_run("synthetic-run",["a"],[post("a")],2)],
                                 ["a","b"],2,START,END,POST_CONTRACT)
        self.assertEqual(result["status"],"partial_interface_error")
        self.assertEqual(result["coverage_status"],"unknown")
        self.assertEqual(result["interface_errors"][0]["missing"][0]["usernames"],["b"])

    def test_missing_bundle_usernames_uses_row_contract_or_preserves_unattributable_rows(self):
        bundle = synthetic_run("synthetic-missing-usernames", ["a"],
            [post("owned", creator="a"), post("outside", creator="not-requested"),
             {"url":"https://www.instagram.com/reel/no-owner/","created":START,
              "kind":"Video","stable":"no-owner"}], 5)
        del bundle["usernames"]
        got = wf.select_posts([bundle], ["a"], 3, START, END, POST_CONTRACT)

        self.assertEqual(got["status"], "partial_interface_error")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertEqual([item["row"]["stable"] for item in got["selected"]], ["owned"])
        self.assertEqual(got["selected"][0]["creator"], "a")
        self.assertEqual(got["selected"][0]["source_run_id"], "synthetic-missing-usernames")
        self.assertEqual(got["selected"][0]["source_run_index"], 0)
        self.assertEqual(got["counts"]["a"]["coverage_status"], "unknown")
        self.assertTrue(got["counts"]["a"]["additional_candidates_unknown"])
        self.assertEqual(len(got["unresolved"]), 2)
        self.assertEqual({item["row_index"] for item in got["unresolved"]}, {1, 2})
        self.assertTrue(all(item["run_id"] == "synthetic-missing-usernames" and
                            item["run_index"] == 0 and item["reason"]
                            for item in got["unresolved"]))

    def test_fallback_run_is_included_in_only_its_row_attributed_creator_coverage(self):
        run_a = synthetic_run("r-ok", ["a"], [post("a-ok")], 5)
        run_b = synthetic_run("r-b", ["b"], [post("b-ok", creator="b")], 5)
        fallback = synthetic_run("r-fb", ["a"],
            [post("a-fb-1"), post("a-fb-2", created="2026-11-05T23:00:00Z")], 5)
        del fallback["usernames"]

        got = wf.select_posts([run_a, run_b, fallback], ["a", "b"], 5,
                              START, END, POST_CONTRACT)

        self.assertEqual(got["status"], "partial_interface_error")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertEqual(got["counts"]["a"]["coverage_status"], "unknown")
        self.assertTrue(got["counts"]["a"]["additional_candidates_unknown"])
        self.assertEqual([run["run_id"] for run in got["counts"]["a"]["run_coverage"]],
                         ["r-ok", "r-fb"])
        self.assertEqual(got["counts"]["a"]["run_coverage"][1], {
            "run_id":"r-fb", "status":"run_username_mapping_missing",
            "run_status":"SUCCEEDED", "attributed_via":"row_creator_field"})
        self.assertEqual(got["counts"]["b"]["coverage_status"], "complete")
        self.assertFalse(got["counts"]["b"]["additional_candidates_unknown"])
        self.assertEqual([run["run_id"] for run in got["counts"]["b"]["run_coverage"]], ["r-b"])
        fallback_record = next(run for run in got["run_coverage"] if run["run_id"] == "r-fb")
        self.assertEqual(fallback_record["usernames"], [])
        self.assertEqual(fallback_record["row_attributed_usernames"], ["a"])
        self.assertEqual(fallback_record["coverage_status"], "run_username_mapping_missing")
        selected_from_fallback = [item for item in got["selected"]
                                  if item["source_run_id"] == "r-fb"]
        self.assertEqual(len(selected_from_fallback), 2)
        self.assertTrue(all(item["source_run_index"] == 2 for item in selected_from_fallback))

    def test_fallback_invalid_url_does_not_create_creator_run_coverage(self):
        invalid = post("invalid-url")
        invalid["url"] = "https://example.com/not-an-instagram-post"
        fallback = synthetic_run("r-fb-invalid", ["a"], [invalid], 5)
        del fallback["usernames"]

        got = wf.select_posts([fallback], ["a"], 3, START, END, POST_CONTRACT)

        self.assertEqual(got["coverage_status"], "unknown")
        self.assertNotEqual(got["status"], "complete")
        self.assertEqual(got["selected"], [])
        self.assertEqual(got["counts"]["a"]["run_coverage"], [])
        self.assertEqual(got["counts"]["a"]["coverage_status"], "unknown")
        self.assertEqual(len(got["unresolved"]), 1)
        self.assertEqual(got["unresolved"][0]["row"], invalid)
        self.assertEqual(got["unresolved"][0]["run_id"], "r-fb-invalid")
        self.assertEqual(got["unresolved"][0]["row_index"], 0)
        self.assertIn("invalid", got["unresolved"][0]["reason"])

    def test_fallback_invalid_and_valid_rows_attribute_run_once_for_valid_candidate(self):
        invalid = post("invalid-url")
        invalid["url"] = "https://example.com/not-an-instagram-post"
        valid = post("valid-fallback")
        fallback = synthetic_run("r-fb-mixed", ["a"], [invalid, valid], 5)
        del fallback["usernames"]

        got = wf.select_posts([fallback], ["a"], 3, START, END, POST_CONTRACT)

        self.assertEqual(got["coverage_status"], "unknown")
        self.assertNotEqual(got["status"], "complete")
        self.assertEqual(len(got["selected"]), 1)
        self.assertEqual(got["selected"][0]["row"]["stable"], "valid-fallback")
        self.assertEqual(got["selected"][0]["source_run_id"], "r-fb-mixed")
        self.assertEqual(got["selected"][0]["source_run_index"], 0)
        self.assertEqual(len(got["unresolved"]), 1)
        self.assertEqual(got["unresolved"][0]["row"], invalid)
        self.assertEqual(got["unresolved"][0]["row_index"], 0)
        self.assertEqual(len(got["counts"]["a"]["run_coverage"]), 1)
        self.assertEqual(got["counts"]["a"]["run_coverage"][0]["run_id"], "r-fb-mixed")
        fallback_record = next(r for r in got["run_coverage"] if r["run_id"] == "r-fb-mixed")
        self.assertEqual(fallback_record["row_attributed_usernames"], ["a"])

    def test_failed_fallback_run_is_reported_once_with_error_and_row_author(self):
        failed = synthetic_run("r-failed-fallback", ["a"], [post("failed-row")], 5,
                               True, run_status="FAILED", run_error="synthetic failure")
        del failed["usernames"]

        got = wf.select_posts([failed], ["a"], 3, START, END, POST_CONTRACT)

        self.assertEqual(got["status"], "partial_interface_error")
        self.assertEqual(got["coverage_status"], "unknown")
        self.assertNotIn(got["status"], {"complete", "no_candidates"})
        self.assertEqual(len(got["run_failures"]), 1)
        self.assertEqual(got["run_failures"][0]["run_id"], "r-failed-fallback")
        self.assertEqual(got["run_failures"][0]["run_status"], "FAILED")
        self.assertEqual(got["run_failures"][0]["error"], "synthetic failure")
        self.assertEqual(set(got["run_failures"][0]), {
            "run_id", "usernames", "row_attributed_usernames", "run_status", "error",
            "status_message", "coverage_status"})
        self.assertEqual(got["run_failures"][0]["row_attributed_usernames"], ["a"])
        self.assertEqual(got["counts"]["a"]["coverage_status"], "unknown")
        self.assertEqual(len(got["selected"]), 1)
        self.assertEqual(got["selected"][0]["source_run_id"], "r-failed-fallback")
        self.assertEqual(got["selected"][0]["source_run_index"], 0)

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
        self.assertTrue(got[0]["reason"])

    def test_reconcile_terminal_failures_are_not_pending(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        for run_status in ("FAILED", "ABORTED", "TIMED-OUT"):
            for completeness in (False, None):
                with self.subTest(run_status=run_status, dataset_complete=completeness):
                    got = wf.reconcile_transcripts([postrow], [], run_status, completeness,
                                                  POST_CONTRACT, TRANSCRIPT_CONTRACT,
                                                  "reported terminal failure")
                    self.assertEqual(got[0]["status"], "run_failed")
                    self.assertNotEqual(got[0]["status"], "pending")
                    self.assertEqual(got[0]["run_status"], run_status)
                    self.assertIs(got[0]["dataset_complete"], completeness)
                    self.assertEqual(got[0]["reason"], "reported terminal failure")
                    self.assertEqual(got[0]["error"], "reported terminal failure")

        default_reason = wf.reconcile_transcripts([postrow], [], "FAILED", False,
                                                  POST_CONTRACT, TRANSCRIPT_CONTRACT)[0]
        self.assertEqual(default_reason["status"], "run_failed")
        self.assertIn("FAILED", default_reason["reason"])
        self.assertIsNone(default_reason["error"])

    def test_reconcile_run_error_accepts_only_text_without_dropping_matches(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        for value in ("worker stopped", None, 42, ["not", "text"], {"message":"not a string"}):
            with self.subTest(run_error=value):
                failed = wf.reconcile_transcripts([postrow], [], "FAILED", False,
                                                  POST_CONTRACT, TRANSCRIPT_CONTRACT, value)[0]
                self.assertEqual(failed["status"], "run_failed")
                self.assertIs(failed["dataset_complete"], False)
                if value == "worker stopped":
                    self.assertEqual(failed["error"], value)
                    self.assertEqual(failed["reason"], value)
                else:
                    self.assertIsNone(failed["error"])
                    self.assertEqual(failed["reason"], "Transcript Actor run ended with FAILED")

        missing = wf.reconcile_transcripts([postrow], [], "FAILED", None,
                                            POST_CONTRACT, TRANSCRIPT_CONTRACT)[0]
        self.assertIsNone(missing["error"])
        self.assertEqual(missing["reason"], "Transcript Actor run ended with FAILED")

        matched = wf.reconcile_transcripts([postrow], [
            {"url":postrow["url"],"pk":"a","userName":"a","text":"transcript"}],
            "SUCCEEDED", None, POST_CONTRACT, TRANSCRIPT_CONTRACT,
            {"unexpected":"object"})[0]
        self.assertEqual(matched["status"], "success")
        self.assertEqual(matched["transcript"], "transcript")
        self.assertIsNone(matched["dataset_complete"])

        for field, value in (("run_error", "actual host message"),
                             ("run_error", None),
                             ("run_error", {"message":"unsupported shape"}),
                             (None, None)):
            with self.subTest(cli_run_error=(field, value)):
                request = {"operation":"reconcile", "submitted":[postrow], "rows":[],
                           "run_status":"FAILED", "dataset_complete":None,
                           "post_contract":POST_CONTRACT, "transcript_contract":TRANSCRIPT_CONTRACT}
                if field is not None:
                    request[field] = value
                proc = subprocess.run([sys.executable, str(PATH)], input=json.dumps(request), text=True,
                                      capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
                self.assertEqual(proc.returncode, 0, proc.stderr)
                result = json.loads(proc.stdout)["results"][0]
                self.assertEqual(result["status"], "run_failed")
                self.assertTrue(isinstance(result["reason"], str) and result["reason"])
                self.assertTrue(result["error"] is None or isinstance(result["error"], str))

    def test_reconcile_pending_reasons_distinguish_run_and_dataset(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        for run_status in ("READY", "RUNNING", "ABORTING", "TIMING-OUT", "UNKNOWN"):
            with self.subTest(run_status=run_status):
                result = wf.reconcile_transcripts([postrow], [], run_status, None,
                                                  POST_CONTRACT, TRANSCRIPT_CONTRACT)[0]
                self.assertEqual(result["status"], "pending")
                self.assertIn("run", result["reason"].lower())
                self.assertEqual(result["run_status"], run_status)
                self.assertIsNone(result["dataset_complete"])

        for completeness, expected in ((False, "incomplete"), (None, "unknown")):
            with self.subTest(run_status="SUCCEEDED", dataset_complete=completeness):
                result = wf.reconcile_transcripts([postrow], [], "SUCCEEDED", completeness,
                                                  POST_CONTRACT, TRANSCRIPT_CONTRACT)[0]
                self.assertEqual(result["status"], "pending")
                self.assertIn(expected, result["reason"].lower())
                self.assertEqual(result["run_status"], "SUCCEEDED")
                self.assertIs(result["dataset_complete"], completeness)

        complete_empty = wf.reconcile_transcripts([postrow], [], "SUCCEEDED", True,
                                                  POST_CONTRACT, TRANSCRIPT_CONTRACT)[0]
        self.assertEqual(complete_empty["status"], "not_returned")
        self.assertIs(complete_empty["dataset_complete"], True)

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

    def test_duplicate_candidate_reason_is_independent_of_dataset_completeness(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        for completeness in (True, False, None):
            with self.subTest(dataset_complete=completeness):
                got = wf.reconcile_transcripts([postrow, dict(postrow)], [], "SUCCEEDED", completeness,
                                              POST_CONTRACT, TRANSCRIPT_CONTRACT)
                self.assertEqual(len(got), 1)
                self.assertEqual(got[0]["status"], "duplicate_candidate")
                self.assertEqual(got[0]["reason"], "Duplicate candidate in submitted list")
                self.assertIs(got[0]["dataset_complete"], completeness)

    def test_reconcile_normalizes_known_run_status_variants_like_select(self):
        postrow = {"url":"https://www.instagram.com/reel/a/","stable_id":"a","creator":"a"}
        for raw_status in ("TIMED_OUT", "timed-out", "timed_out"):
            with self.subTest(run_status=raw_status):
                result = wf.reconcile_transcripts([postrow], [], raw_status, None,
                                                  POST_CONTRACT, TRANSCRIPT_CONTRACT)[0]
                self.assertEqual(result["status"], "run_failed")
                self.assertEqual(result["run_status"], "TIMED-OUT")
                self.assertEqual(result["reason"], "Transcript Actor run ended with TIMED-OUT")

                discovery = synthetic_run("synthetic-timed-out", ["a"], [], 3, True,
                                          run_status=raw_status)
                selected = wf.select_posts([discovery], ["a"], 2, START, END, POST_CONTRACT)
                self.assertEqual(selected["run_failures"][0]["run_status"], "TIMED-OUT")

    def test_batch_splitting_uses_live_limit(self):
        self.assertEqual(wf.split_batches(["a","b","c","d","e"],2),[["a","b"],["c","d"],["e"]])
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

    def test_reconcile_match_success_does_not_claim_dataset_completeness(self):
        submitted = [{"url":"https://www.instagram.com/reel/a/", "stable_id":"a", "creator":"a"}]
        row = {"url":submitted[0]["url"], "pk":"a", "userName":"a", "text":"matched transcript"}
        for completeness in (False, None):
            with self.subTest(dataset_complete=completeness):
                got = wf.reconcile_transcripts([submitted[0]], [row], "SUCCEEDED", completeness,
                                              POST_CONTRACT, TRANSCRIPT_CONTRACT)
                self.assertEqual(got[0]["status"], "success")
                self.assertIs(got[0]["dataset_complete"], completeness)
                self.assertEqual(got[0]["run_status"], "SUCCEEDED")

    def test_reconcile_dataset_completeness_is_stable_on_duplicate_and_conflict_paths(self):
        post_a = {"url":"https://www.instagram.com/reel/a/", "stable_id":"a", "creator":"a"}
        post_b = {"url":"https://www.instagram.com/reel/b/", "stable_id":"b", "creator":"b"}
        for completeness in (False, None):
            with self.subTest(dataset_complete=completeness):
                duplicate = wf.reconcile_transcripts([post_a], [
                    {"url":post_a["url"], "pk":"a", "userName":"a", "text":"one"},
                    {"url":post_a["url"], "pk":"a", "userName":"a", "text":"two"}],
                    "SUCCEEDED", completeness, POST_CONTRACT, TRANSCRIPT_CONTRACT)
                self.assertEqual(duplicate[0]["status"], "duplicate_transcript_rows")
                self.assertIs(duplicate[0]["dataset_complete"], completeness)
                self.assertEqual(len(duplicate[0]["rows"]), 2)

                url_pk_conflict = wf.reconcile_transcripts([post_a, post_b], [
                    {"url":post_a["url"], "pk":"b", "userName":"a", "text":"conflict"}],
                    "SUCCEEDED", completeness, POST_CONTRACT, TRANSCRIPT_CONTRACT)
                conflicts = [item for item in url_pk_conflict if item.get("status") == "identity_conflict"]
                self.assertEqual(len(conflicts), 2)
                self.assertTrue(all(item["dataset_complete"] is completeness for item in conflicts))

                author_conflict = wf.reconcile_transcripts([post_a], [
                    {"url":post_a["url"], "pk":"a", "userName":"other", "text":"conflict"}],
                    "SUCCEEDED", completeness, POST_CONTRACT, TRANSCRIPT_CONTRACT)
                self.assertEqual(author_conflict[0]["status"], "identity_conflict")
                self.assertIs(author_conflict[0]["dataset_complete"], completeness)

                invalid_url_id_hit = wf.reconcile_transcripts([post_a], [
                    {"url":"https://example.com/bad", "pk":"a", "userName":"a", "text":"conflict"}],
                    "SUCCEEDED", completeness, POST_CONTRACT, TRANSCRIPT_CONTRACT)
                self.assertEqual(invalid_url_id_hit[0]["status"], "identity_conflict")
                self.assertIs(invalid_url_id_hit[0]["dataset_complete"], completeness)

        missing = wf.reconcile_transcripts([post_a], [
            {"url":post_a["url"], "pk":"a", "userName":"a", "text":"matched"}],
            "SUCCEEDED", None, POST_CONTRACT, TRANSCRIPT_CONTRACT)
        self.assertIsNone(missing[0]["dataset_complete"])

    def test_reconcile_cli_missing_dataset_complete_is_unknown(self):
        request = {"operation":"reconcile", "submitted":[{"url":"https://www.instagram.com/reel/a/",
                    "stable_id":"a", "creator":"a"}],
                   "rows":[{"url":"https://www.instagram.com/reel/a/", "pk":"a",
                            "userName":"a", "text":"matched"}],
                   "run_status":"SUCCEEDED", "post_contract":POST_CONTRACT,
                   "transcript_contract":TRANSCRIPT_CONTRACT}
        proc = subprocess.run([sys.executable, str(PATH)], input=json.dumps(request), text=True,
                              capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        output = json.loads(proc.stdout)
        self.assertEqual(output["results"][0]["status"], "success")
        self.assertIsNone(output["results"][0]["dataset_complete"])
    def test_exact_video_value_selects_and_other_media_values_remain_unknown(self):
        rows = [post("upper", created="2026-11-05T13:00:00Z"),
                post("photo", created="2026-11-05T12:00:00Z"),
                post("new", created="2026-11-05T11:00:00Z"),
                post("null-type", created="2026-11-05T10:00:00Z"),
                post("non-string-type", created="2026-11-05T09:00:00Z"),
                post("missing-type", created="2026-11-05T08:00:00Z")]
        rows[0]["kind"] = "Video"
        rows[1]["kind"] = "IMAGE"
        rows[2]["kind"] = "short_video_v2"
        rows[3]["kind"] = None
        rows[4]["kind"] = 7
        rows[4]["url"] = None
        del rows[5]["kind"]
        got = select(rows, ["a"], 5)
        self.assertEqual(got["status"], "partial")
        self.assertEqual(len(got["selected"]), 1)
        self.assertEqual(got["row_interface_error_count"], 0)
        self.assertEqual(got["counts"]["a"]["discovered_returned_in_window"], 5)
        self.assertEqual(got["counts"]["a"]["unknown_media_type"], 5)
        self.assertEqual(got["counts"]["a"]["type_video_candidates"], 1)
        self.assertFalse(got["counts"]["a"]["additional_candidates_unknown"])
        self.assertEqual([u["status"] for u in got["unresolved"]], ["unknown_media_type"] * 5)
        self.assertEqual([u["value"] for u in got["unresolved"]], ["IMAGE", "short_video_v2", None, 7, None])
        self.assertEqual([u["field_present"] for u in got["unresolved"]], [True, True, True, True, False])
        self.assertTrue(all("reason" not in u for u in got["unresolved"]))

    def test_cli_stdin_json_executes_report_chain_without_budget_operations(self):
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

        code, settings = invoke({"operation":"settings", "settings":{"report_budget_usd":"legacy and ignored",
            "per_creator_limit":1,"accounts":["@a"],"save_consent":False}})
        self.assertEqual(code, 0)
        self.assertEqual(settings, {"accounts":["a"],"per_creator_limit":1,"save_consent":False})
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
        code, batches = invoke({"operation":"split","urls":[selected["selected"][0]["url"]],"batch_size":1})
        self.assertEqual(code, 0)
        self.assertEqual(batches["batches"], [[selected["selected"][0]["url"]]])
        code, reconciled = invoke({"operation":"reconcile","submitted":selected["selected"],
            "rows":[{"url":selected["selected"][0]["url"],"pk":"a","text":"spoken words"}],
            "run_status":"SUCCEEDED","dataset_complete":True,"post_contract":POST_CONTRACT,
            "transcript_contract":TRANSCRIPT_CONTRACT})
        self.assertEqual(code, 0)
        self.assertEqual(reconciled["results"][0]["status"], "success")

        for operation in ("plan_stage", "verify_run", "remaining", "unknown"):
            code, error = invoke({"operation":operation})
            self.assertEqual(code, 2)
            self.assertEqual(error["error"], "unknown operation")

if __name__ == "__main__":
    unittest.main()

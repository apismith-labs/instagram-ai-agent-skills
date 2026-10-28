import copy
import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'skills/instagram-transcript-extractor/scripts/workflow.py'
spec = importlib.util.spec_from_file_location('workflow', SCRIPT)
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

def url(code):
    return f'https://www.instagram.com/reel/{code}/'

def evidence(total, status='SUCCEEDED', limit=20):
    return [{'run_status': status, 'pages': [{'offset': 0, 'limit': limit, 'count': total, 'total': total, 'truncated': False}]}]

def single(plan, items, observations):
    plan = copy.deepcopy(plan)
    status = observations[0].get('run_status') if observations else 'SUCCEEDED'
    plan['batches'][0].update(phase='submitted', run_id='r1', dataset_id='d1', run_status=status)
    observations = copy.deepcopy(observations)
    for ev in observations:
        ev.update(batch_id='batch-1', run_id='r1', dataset_id='d1', item_indices=list(range(len(items))))
    return w.reconcile(plan, items, observations)


class WorkflowTests(unittest.TestCase):
    def test_variants_are_deduplicated_and_originals_retained(self):
        original = [url('ABC'), 'https://instagram.com/reel/ABC', 'https://WWW.INSTAGRAM.COM/reel/ABC/?igsh=example#fragment']
        plan = w.prepare(original)
        self.assertEqual(len(plan['requests']), 1)
        self.assertEqual(plan['requests'][0]['originals'], [{'line': i+1, 'url': u} for i, u in enumerate(original)])
        self.assertEqual(w.actor_input(plan['requests']), {'enhancedcrawl': True, 'videoUrl': original[0]})
        out = single(plan, [{'url': 'https://instagram.com/reel/ABC', 'text': 'visible'}], evidence(1))
        self.assertEqual(out['results'][0]['item']['text'], 'visible')
        self.assertEqual(out['counts'], {'success': 1})

    def test_distinct_identities_and_unsupported_links(self):
        plan = w.prepare([url('ABC'), url('abc'), url('DEF'), 'https://instagram.com/p/ABC/', 'https://instagram.com/share/reel/ABC', 'https://ig.me/ABC', url('ABC')+'?unknown=1'])
        self.assertEqual(len(plan['requests']), 4)
        self.assertEqual(len(plan['invalid']), 3)
        self.assertIn('copy', plan['invalid'][0]['reason'])
        self.assertEqual(w.actor_input(plan['requests'])['enhancedcrawl'], True)
        self.assertEqual(len(w.actor_input(plan['requests'])['bulkUrls']), 4)

    def test_shuffled_partial_and_anonymous(self):
        plan = w.prepare([url('A'), url('A'), url('B'), url('C'), url('D')])
        items = [{'code':'D','text':'partial','errMsg':'warning'}, {'url':url('A'),'text':'spoken'}, {'text':'unknown'}, {'code':'B','errMsg':'failed'}]
        out = single(plan, items, evidence(4))
        self.assertEqual(out['counts'], {'success':1,'failed':1,'not_returned':1,'review':1})
        self.assertFalse(out['results'][2]['identity_review'])
        self.assertEqual(out['results'][3]['item']['text'], 'partial')
        self.assertEqual(len(out['unassigned']), 1)

    def test_conflict_does_not_hide_valid_item(self):
        plan = w.prepare([url('A'), url('B'), url('C')])
        rows = [{'url':url('A'),'text':'safe'}, {'url':url('A'),'code':'B','text':'conflict'}]
        out = single(plan, rows, evidence(2))
        self.assertEqual(out['results'][0]['status'], 'review')
        self.assertEqual(out['results'][0]['item']['text'], 'safe')
        self.assertEqual(out['results'][1]['status'], 'review')
        self.assertEqual(out['results'][2]['status'], 'not_returned')
        self.assertFalse(out['results'][2]['identity_review'])
        self.assertEqual(len(out['unassigned']), 1)

    def test_duplicate_candidates_are_visible(self):
        out = single(w.prepare([url('A')]), [{'code':'A','text':'one'}, {'code':'A','text':'two'}], evidence(2))
        self.assertEqual(out['counts'], {'review': 1})
        self.assertEqual([x['text'] for x in out['results'][0]['items']], ['one','two'])

    def test_empty_mixed_and_malformed(self):
        plan = w.prepare([url('A'),url('B'),url('C'),url('D')])
        out = single(plan, [{'code':'A','text':' '}, {'code':'B','text':12}, {'code':'C','text':'ok'}, {'code':'D','text':'yes','errMsg':'warning'}], evidence(4))
        self.assertEqual(out['counts'], {'empty':1,'review':2,'success':1})

    def test_segments_preserve_transcript(self):
        plan = w.prepare([url('A')])
        for seg in (None, 'bad', [{'start':2,'end':1,'text':'x'}], [{'start':True,'end':3,'text':'x'}], [{'start':2,'end':3,'text':'x'}, {'start':1,'end':4,'text':'x'}]):
            with self.subTest(seg=seg):
                out = single(plan, [{'code':'A','text':'valid','segments':seg}], evidence(1))['results'][0]
                self.assertEqual(out['status'], 'success')
                self.assertEqual(out['item']['text'], 'valid')
                self.assertEqual(out['safe_segments'], [])
                self.assertIn(out['timestamps'], ('invalid','unavailable'))
        valid = [{'start':0.2,'end':1.0,'text':'hello'}]
        self.assertEqual(single(plan, [{'code':'A','text':'valid','segments':valid}], evidence(1))['results'][0]['safe_segments'], valid)

    def test_completeness_guards(self):
        plan = w.prepare([url('A'),url('B')])
        rows = [{'code':'A','text':'ok'}]
        cases = [evidence(1,'RUNNING'), [{'run_status':'SUCCEEDED','pages':[{'offset':0,'limit':1,'count':1,'total':2,'truncated':False}]}],
                 [{'run_status':'SUCCEEDED','pages':[{'offset':0,'limit':1,'count':1,'total':1,'truncated':False},{'offset':1,'limit':1,'count':0,'total':2,'truncated':False}]}], [],
                 [{'run_status':'SUCCEEDED','pages':[{'offset':0,'limit':10,'count':1,'truncated':False}]}]]
        for ev in cases:
            with self.subTest(evidence=ev): self.assertEqual(single(plan, rows, ev)['results'][1]['status'], 'pending')
        self.assertEqual(single(plan, rows, evidence(1))['results'][1]['status'], 'not_returned')
        self.assertEqual(single(plan, [], evidence(0))['counts'], {'not_returned':2})
        marker = [{'run_status':'FAILED','pages':[{'offset':0,'limit':10,'count':1,'truncated':False}],'end_of_data':True,'end_evidence':'tool documented terminal marker'}]
        self.assertTrue(single(plan, rows, marker)['complete'])

    def test_multipage(self):
        ev = [{'run_status':'SUCCEEDED','pages':[{'offset':0,'limit':1,'count':1,'total':2,'truncated':False},{'offset':1,'limit':1,'count':1,'total':2,'truncated':False}]}]
        plan = w.prepare([url('A'),url('B'),url('C')])
        self.assertEqual(single(plan, [{'code':'A','text':'a'}, {'code':'B','text':'b'}], ev)['counts'], {'success':2,'not_returned':1})
        ev[0]['pages'][1]['offset'] = 0
        self.assertFalse(single(plan, [{'code':'A'}, {'code':'B'}], ev)['complete'])

    def test_terminal_status_and_partial_results(self):
        plan = w.prepare([url('A'), url('B')])
        for run_status in ('SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'):
            with self.subTest(run_status=run_status):
                missing = 'not_returned' if run_status == 'SUCCEEDED' else 'run_failed'
                empty = single(plan, [], evidence(0, run_status))
                self.assertEqual(empty['counts'], {missing: 2})
                self.assertEqual(empty['batches'][0]['run_status'], run_status)
                partial = single(plan, [{'code': 'A', 'text': 'sample'}], evidence(1, run_status))
                self.assertEqual(partial['counts'], {'success': 1, missing: 1})
                self.assertEqual(partial['results'][0]['item']['text'], 'sample')
                self.assertEqual(partial['results'][0]['run_status'], run_status)
                self.assertEqual(sum(partial['counts'].values()), 2)

    def test_unregistered_and_incomplete_runs_remain_pending(self):
        plan = w.prepare([url('A')])
        self.assertEqual(w.reconcile(plan, [], [])['counts'], {'pending': 1})
        plan['batches'][0].update(phase='submitted', run_id='r1', run_status='SUCCEEDED')
        ev = evidence(0)
        ev[0].update(batch_id='batch-1', run_id='r1', dataset_id='d1', item_indices=[])
        self.assertEqual(w.reconcile(plan, [], ev)['counts'], {'pending': 1})
        plan['batches'][0]['dataset_id'] = 'd1'
        ev[0]['pages'][0]['total'] = 1
        self.assertEqual(w.reconcile(plan, [], ev)['counts'], {'pending': 1})
        # A run wholly absent from plan and evidence is unknowable to the helper.

    def test_batch_coverage_and_identity(self):
        plan = w.prepare([url('A'), url('A'), url('B'), url('C'), url('D')])
        plan['batches'] = [
            {'batch_id':'b1','request_indices':[0,1], 'phase':'submitted','run_id':'r1','dataset_id':'d1','run_status':'SUCCEEDED'},
            {'batch_id':'b2','request_indices':[2,3], 'phase':'submitted','run_id':'r2','dataset_id':'d2','run_status':'SUCCEEDED'}]
        rows = [{'code':'A','text':'a'}, {'code':'C','text':'c'}]
        e1 = {'batch_id':'b1','run_id':'r1','dataset_id':'d1','run_status':'SUCCEEDED','item_indices':[0], 'pages':[{'offset':0,'limit':10,'count':1,'total':1,'truncated':False}]}
        e2 = {'batch_id':'b2','run_id':'r2','dataset_id':'d2','run_status':'SUCCEEDED','item_indices':[1], 'pages':[{'offset':0,'limit':10,'count':1,'total':1,'truncated':False}]}
        result = w.reconcile(plan, rows, [e1,e2])
        self.assertEqual(result['counts'], {'success':2,'not_returned':2})
        self.assertEqual(result['results'][0]['lines'], [1,2])
        self.assertEqual(w.reconcile(plan, rows[:1], [e1])['counts'], {'success':1,'not_returned':1,'pending':2})
        # Two observations for the same run cannot cover two distinct batches.
        for key in ('run_id','dataset_id'):
            bad = copy.deepcopy(e2); bad[key] = e1[key]
            out = w.reconcile(plan, rows, [e1,bad])
            self.assertFalse(out['complete'])
            self.assertEqual(out['results'][2]['status'], 'pending')
        for key in ('run_id','dataset_id'):
            bad = copy.deepcopy(e2); bad[key] = 'wrong'
            out = w.reconcile(plan, rows, [e1,bad])
            self.assertEqual(out['results'][1]['status'], 'not_returned')
            self.assertEqual(out['results'][3]['status'], 'pending')
        incomplete = copy.deepcopy(e2); incomplete['pages'][0]['total'] = 2
        out = w.reconcile(plan, rows, [e1,incomplete])
        self.assertEqual(out['counts'], {'success':2,'not_returned':1,'pending':1})
        self.assertTrue(out['results'][2]['provisional'])
        self.assertFalse(out['results'][1]['provisional'])
        out = w.reconcile(plan, rows, [e1,e2,copy.deepcopy(e2)])
        self.assertEqual(out['results'][3]['status'], 'pending')
        p = copy.deepcopy(plan); del p['batches'][1]['run_id']
        self.assertEqual(w.reconcile(p, rows, [e1,e2])['results'][3]['status'], 'pending')
        for phase in ('new', 'submission_unknown'):
            p = copy.deepcopy(plan); p['batches'][1]['phase'] = phase
            out = w.reconcile(p, rows, [e1,e2])
            self.assertEqual(out['results'][3]['status'], 'pending')
            self.assertFalse(out['batches'][1]['complete'])
        p = copy.deepcopy(plan); p['batches'][1]['run_status'] = 'RUNNING'
        run = copy.deepcopy(e2); run['run_status'] = 'RUNNING'
        self.assertEqual(w.reconcile(p, rows, [e1,run])['results'][3]['status'], 'pending')
        # Reusing the same item index for two batches is also not evidence of coverage.
        bad = copy.deepcopy(e2); bad['item_indices'] = [0]
        self.assertEqual(w.reconcile(plan, rows, [e1,bad])['counts'], {'pending':4})

    def test_batch_plan_must_cover_exactly_once(self):
        plan = w.prepare([url('A'),url('B')])
        for groups in ([[0]], [[0,0,1]], [[0,1],[1]]):
            p = copy.deepcopy(plan)
            p['batches'] = [{'batch_id':str(i),'request_indices':g,'phase':'new'} for i,g in enumerate(groups)]
            with self.subTest(groups=groups), self.assertRaises(w.ContractError):
                w.reconcile(p, [], [])

    def test_non_string_url_reports_row(self):
        with self.assertRaisesRegex(w.ContractError, 'line 2'):
            w.prepare([url('A'), None])

    def test_recovery_policy(self):
        self.assertEqual([w.next_action(s) for s in [{'phase':'new'}, {'phase':'running','run_id':'r1'}, {'phase':'submission_unknown'}, {'phase':'unknown_unresolved'}, {'phase':'terminal','dataset_id':'d1'}, {'phase':'read_incomplete','dataset_id':'d1'}, {'phase':'complete'}]], ['start','get_same_run','find_existing_run','report_unknown','read_dataset','retry_read','report'])

    def test_cli_errors_and_contract(self):
        plan = w.prepare([url('A')])
        cases = [('{', 'invalid_json'), ('{}','unsupported_operation'), (json.dumps({'operation':'bad','secret':'dont-echo'}),'unsupported_operation'), (json.dumps({'operation':'prepare'}),'missing_field')]
        for value in ({'items':[]}, {'data':{'items':[]}}, '[]', None):
            cases.append((json.dumps({'operation':'reconcile','plan':plan,'items':value,'evidence':[]}), 'invalid_items'))
        cases.append((json.dumps({'operation':'reconcile','plan':plan,'items':[]}), 'missing_field'))
        for data, error in cases:
            with self.subTest(error=error, data=data):
                p = subprocess.run([sys.executable, str(SCRIPT)], input=data, text=True, capture_output=True)
                self.assertEqual(p.returncode, 2)
                self.assertEqual(json.loads(p.stderr)['error']['type'], error)
                self.assertNotIn('dont-echo', p.stderr)
                self.assertEqual(p.stdout, '')
        plan['batches'][0].update(phase='submitted',run_id='r1',dataset_id='d1',run_status='SUCCEEDED')
        ev = evidence(0); ev[0].update(batch_id='batch-1',run_id='r1',dataset_id='d1',item_indices=[])
        ok = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps({'operation':'reconcile','plan':plan,'items':[],'evidence':ev}), text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(ok.stdout)['counts'], {'not_returned':1})

if __name__ == '__main__': unittest.main()

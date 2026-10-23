import copy
import json
from pathlib import Path
import unittest
from analyzer import analyze, TOP

class AnalyzerTests(unittest.TestCase):
    def setUp(self):
        self.program = json.loads(Path(__file__).with_name('refund.json').read_text())

    def test_different_branch_values_merge_to_unknown(self):
        result = analyze(self.program)
        self.assertEqual(result['in_states']['cost']['count'], TOP)
        self.assertEqual(result['reports'][0]['status'], 'unknown-may-be-zero')

    def test_equal_values_merge_to_constant_and_safe_denominator(self):
        self.program['nodes']['repeat']['value'] = 1
        result = analyze(self.program)
        self.assertEqual(result['in_states']['cost']['count'], 1)
        self.assertEqual(result['in_states']['done']['average'], 100)
        self.assertEqual(result['reports'], [])

    def test_zero_denominator_is_retained_as_candidate(self):
        self.program['nodes']['first']['value'] = 0
        result = analyze(self.program)
        self.assertEqual(result['reports'][0]['abstract_value'], 0)

    def test_unreachable_node_is_not_reported(self):
        self.program['nodes']['dead'] = {'op':'assert_nonzero', 'src':'unused', 'next':'done'}
        result = analyze(self.program)
        self.assertIsNone(result['in_states']['dead'])
        self.assertFalse(any(r['node'] == 'dead' for r in result['reports']))

    def test_loop_loses_constant_and_converges(self):
        p = {'entry':'init', 'nodes':{
            'init':{'op':'const','dst':'x','value':0,'next':'one'},
            'one':{'op':'const','dst':'one','value':1,'next':'loop'},
            'loop':{'op':'add','dst':'x','a':'x','b':'one','next':'loop'}}}
        result = analyze(p)
        self.assertEqual(result['in_states']['loop']['x'], TOP)
        self.assertLess(result['worklist_steps'], 10)

    def test_missing_target_and_unknown_instruction_rejected(self):
        p = copy.deepcopy(self.program)
        p['nodes']['cost']['next'] = 'missing'
        with self.assertRaises(ValueError): analyze(p)
        self.program['nodes']['cost']['op'] = 'call'
        with self.assertRaises(ValueError): analyze(self.program)

    def test_malformed_fields_are_rejected_with_value_error(self):
        for key, value in [("entry", []), ("op", []), ("target", [])]:
            p = copy.deepcopy(self.program)
            if key == "entry": p["entry"] = value
            elif key == "op": p["nodes"]["paid"]["op"] = value
            else: p["nodes"]["paid"]["next"] = value
            with self.assertRaises(ValueError): analyze(p)

    def test_constant_branch_is_deliberately_not_pruned(self):
        self.program['nodes']['choice'] = {'op':'const','dst':'retry','value':1,'next':'fork'}
        self.assertEqual(analyze(self.program)['in_states']['cost']['count'], TOP)

if __name__ == '__main__': unittest.main()

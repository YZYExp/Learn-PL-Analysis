import unittest
from extension_checks import analysis_key, counterexample, explore_refunds, finite_cegis, invalidated

class ExtensionChecks(unittest.TestCase):
    def test_crash_retry_duplicates_without_atomic_remote_dedup(self):
        states, trace = explore_refunds(False)
        self.assertIsNotNone(trace)
        self.assertIn('crash before local acknowledgement', trace)
        self.assertTrue(any(s.effects == 2 for s in states))

    def test_same_key_dedup_preserves_effect_bound_in_finite_model(self):
        states, trace = explore_refunds(True)
        self.assertIsNone(trace)
        self.assertTrue(any(s.local == 'refunded' and s.effects == 1 for s in states))
        self.assertTrue(all(s.effects <= 1 for s in states))

    def test_diamond_invalidation_includes_all_consumers_not_unrelated(self):
        graph = {'model': [], 'a': ['model'], 'b': ['model'], 'report': ['a', 'b'], 'other': []}
        self.assertEqual(invalidated(graph, ['model']), {'model', 'a', 'b', 'report'})

    def test_cyclic_dependency_closure_terminates(self):
        graph = {'a': ['b'], 'b': ['a'], 'c': ['b'], 'other': []}
        self.assertEqual(invalidated(graph, {'a'}), {'a', 'b', 'c'})

    def test_cache_identity_includes_model_and_configuration(self):
        k = analysis_key('source', 'integer-v1', 'gateway-v1', {'flag': False})
        self.assertNotEqual(k, analysis_key('source', 'integer-v1', 'gateway-v2', {'flag': False}))
        self.assertNotEqual(k, analysis_key('source', 'integer-v1', 'gateway-v1', {'flag': True}))

    def test_invalidation_rejects_missing_dependency(self):
        with self.assertRaises(ValueError): invalidated({'a': ['absent']}, {'a'})

    def test_small_test_suite_does_not_establish_specification(self):
        self.assertIsNone(counterexample('always-zero', [(0, 0)]))
        self.assertEqual(counterexample('always-zero', [(1, 1)]), (1, 1, 0, 1))

    def test_finite_search_refines_examples_until_clamp(self):
        chosen, history = finite_cegis()
        self.assertEqual(chosen, 'clamp')
        self.assertGreater(len(history), 1)
        self.assertTrue(all(item['counterexample'] is not None for item in history[:-1]))
        self.assertIsNone(history[-1]['counterexample'])

if __name__ == '__main__': unittest.main()

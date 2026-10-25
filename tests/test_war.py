"""Jalankan: python -m unittest discover -s tests -v (networkx, matplotlib)."""
import contextlib
import io
import json
from pathlib import Path
import unittest

import matplotlib
matplotlib.use('Agg')


class WarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nb = json.loads((Path(__file__).resolve().parents[1] / 'ILP.ipynb').read_text())
        cls.env = {'__name__': 'ilp_test'}
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in cls.nb['cells']:
                if cell['cell_type'] == 'code':
                    exec(''.join(cell['source']), cls.env)

    def schedule(self, items):
        return [[i.name for i in batch] for batch in self.env['war_schedule'](items)]

    def test_direction_and_register(self):
        a, b = self.env['war_instructions']
        self.assertEqual(self.env['check_war'](a, b), 'R2')
        self.assertIsNone(self.env['check_war'](b, a))

    def test_pair(self):
        self.assertEqual(self.schedule(self.env['war_instructions']), [['I1'], ['I2']])
        self.assertEqual((self.env['seq_war'], self.env['ilp_war']), (2, 2))

    def test_extended(self):
        self.assertEqual(self.schedule(self.env['war_extended_instructions']),
                         [['I1', 'I4'], ['I2', 'I5'], ['I3']])
        self.assertEqual((self.env['seq_war_extended'], self.env['ilp_war_extended']), (5, 3))

    def test_raw_regression(self):
        self.assertEqual((self.env['seq_raw'], self.env['ilp_raw']), (5, 4))
        self.assertEqual(len(self.env['war_schedule'](self.env['raw_instructions'])), 4)

    def test_empty_single_and_independent(self):
        I = self.env['Instruction']
        self.assertEqual(self.schedule([]), [])
        a = I('A', 'R1', ['R2'])
        b = I('B', 'R3', ['R4'])
        self.assertEqual(self.schedule([a]), [['A']])
        self.assertEqual(self.schedule([a, b]), [['A', 'B']])

    def test_delayed_reader_blocks_writer(self):
        I = self.env['Instruction']
        items = [I('A', 'R1', ['R8']), I('B', 'R2', ['R1', 'R3']),
                 I('C', 'R3', ['R9'])]
        self.assertEqual(self.schedule(items), [['A'], ['B'], ['C']])

    def test_duplicate_names_and_input_unchanged(self):
        I = self.env['Instruction']
        items = [I('X', 'R1', ['R2']), I('X', 'R2', ['R3'])]
        before = [(i.name, i.destination, i.sources[:]) for i in items]
        self.assertEqual(self.schedule(items), [['X'], ['X']])
        self.assertEqual(before, [(i.name, i.destination, i.sources) for i in items])

    def test_graph_edge(self):
        graph = self.env['war_graph']
        self.assertEqual(list(graph.edges), [(0, 1)])
        self.assertEqual(graph[0][1]['label'], 'WAR (R2)')

    def test_existing_functions_not_replaced(self):
        env = {'__name__': 'baseline'}
        with contextlib.redirect_stdout(io.StringIO()):
            for cell in self.nb['cells']:
                if cell['metadata'].get('id') == 'war-notes':
                    break
                if cell['cell_type'] == 'code':
                    exec(''.join(cell['source']), env)
            names = ['Instruction', 'has_dependency', 'parallel_execution',
                     'sequential_execution', 'check_raw', 'run_raw_analysis']
            old = {name: env[name] for name in names}
            for cell in self.nb['cells'][-2:]:
                exec(''.join(cell['source']), env)
        for name in names:
            self.assertIs(env[name], old[name])


if __name__ == '__main__':
    unittest.main()

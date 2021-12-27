import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class TestGraphAlgo(unittest.TestCase):
    def test_load(self):
        g_algo = GraphAlgo()
        file = "../data/diamond.json" #in this graph the number of vertices
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph()),"Graph: |V|=4 , |E|=4")
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 1 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 1}")



if __name__=='__main__':
    unittest.main()



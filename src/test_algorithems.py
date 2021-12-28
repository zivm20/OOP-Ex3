import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class TestGraphAlgo(unittest.TestCase):
    def test_load(self):
        g_algo = GraphAlgo()
        file = "../data/diamond.json"
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph()),"Graph: |V|=4 , |E|=4")
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 1 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 1}")
    
    #also tests diGraph implementations
    def test_save(self):
        g_algo = GraphAlgo()
        file = "../data/diamond.json"
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph()),"Graph: |V|=4 , |E|=4")
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 1 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 1}")
        g_algo.save_to_json("../data/diamond_edit.json")

        file = "../data/diamond_edit.json"
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph()),"Graph: |V|=4 , |E|=4")
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 1 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 1}")
        #test that we save the updated graph and not the old graph
        #test add node
        g_algo.get_graph().add_node(7,(5,4,0))
        g_algo.save_to_json("../data/diamond_edit.json")
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph()),"Graph: |V|=5 , |E|=4")
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 1 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 1, 7: 7: |edges out| 0 |edges in| 0}")
        #test add_edge
        g_algo.get_graph().add_edge(1,7,3)
        g_algo.save_to_json("../data/diamond_edit.json")
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph()),"Graph: |V|=5 , |E|=5")
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 2 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 1, 7: 7: |edges out| 0 |edges in| 1}")
        #test remove edge
        g_algo.get_graph().remove_edge(1,7)
        g_algo.save_to_json("../data/diamond_edit.json")
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 1 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 1, 7: 7: |edges out| 0 |edges in| 0}")
        #test remove node on a node without edges
        g_algo.get_graph().remove_node(7)
        g_algo.save_to_json("../data/diamond_edit.json")
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 1, 1: 1: |edges out| 1 |edges in| 1, 2: 2: |edges out| 1 |edges in| 1, 4: 4: |edges out| 1 |edges in| 1}")
        #test remove node on a node with edges
        g_algo.get_graph().remove_node(4)
        g_algo.save_to_json("../data/diamond_edit.json")
        g_algo.load_from_json(file)
        self.assertEqual(str(g_algo.get_graph()),"Graph: |V|=3 , |E|=2")
        self.assertEqual(str(g_algo.get_graph().get_all_v()),r"{0: 0: |edges out| 1 |edges in| 0, 1: 1: |edges out| 1 |edges in| 1, 2: 2: |edges out| 0 |edges in| 1}")

        #add a node that exists
        self.assertEqual(g_algo.get_graph().add_node(1),False)
        self.assertEqual(g_algo.get_graph().add_node(7),True)
        #remove when 1 node doesn't exist
        self.assertEqual(g_algo.get_graph().remove_edge(1,5),False)
        #remove when both nodes don't exist
        self.assertEqual(g_algo.get_graph().remove_edge(8,5),False)
        #remove when both nodes exists but an edge doesn't
        self.assertEqual(g_algo.get_graph().remove_edge(1,7),False)
        #remove a node that doesn't exist
        self.assertEqual(g_algo.get_graph().remove_node(4),False)
        







    def test_center(self):
        g_algo = GraphAlgo()
        file = "../data/diamond.json"
        g_algo.load_from_json(file)
        idx,dist = g_algo.centerPoint()
        self.assertEqual(idx,0)
        self.assertEqual(dist,15.0)
        g_algo = GraphAlgo()

        file = "../data/not_connected1.json"
        g_algo.load_from_json(file)
        out = g_algo.centerPoint()
        self.assertEqual(out,None)
        g_algo = GraphAlgo()

        file = "../data/not_connected2.json"
        g_algo.load_from_json(file)
        out = g_algo.centerPoint()
        self.assertEqual(out,None)
        g_algo = GraphAlgo()

        file = "../data/2-5-4faster.json"
        g_algo.load_from_json(file)
        out = g_algo.centerPoint()
        self.assertEqual(out[0],2)
        self.assertEqual(out[1],30.284271247461902)
        g_algo = GraphAlgo()

        file = "../data/2-5-4faster_notConnected.json"
        g_algo.load_from_json(file)
        out = g_algo.centerPoint()
        self.assertEqual(out,None)
        


    def test_TSP(self):
        g_algo = GraphAlgo()
        file = "../data/2-5-4faster.json"
        g_algo.load_from_json(file)
        out = g_algo.TSP([5,0,4])
        self.assertEqual(out,([5, 4, 0], 15.142135623730951))

        out = g_algo.TSP([2,3,4,1])
        self.assertEqual(out,([3, 0, 1, 2, 5, 4], 36.1152231423072))

        file = "../data/2-5-4faster_notConnected.json"
        g_algo.load_from_json(file)
        out = g_algo.TSP([2,3,4,1])
        self.assertEqual(out,([3, 0, 1, 2, 5, 4], 36.1152231423072))
        



    def test_ShortestPath(self):
        g_algo = GraphAlgo()
        file = "../data/2-5-4faster_notConnected.json"
        g_algo.load_from_json(file)
        len_2_5_4 = g_algo.get_graph().all_out_edges_of_node(2)[5]+g_algo.get_graph().all_out_edges_of_node(5)[4] 
        self.assertEqual( g_algo.shortest_path(2,4), (len_2_5_4,[2,5,4]))
        self.assertEqual(g_algo.shortest_path(2,7),(float('inf'),[]))
        

if __name__=='__main__':
    unittest.main()



from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from typing import List
class GraphAlgo(GraphAlgoInterface):
    def __init__(self,g:GraphInterface = None):
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph
    def load_from_json(self,json_path:str) -> bool:
        pass
    def save_to_json(self, file_name: str) -> bool:
        pass
    def shortest_path(self, id1: int, id2: int) -> tuple[float, List[int]]:
        for k,v in self.graph.get_all_v().items():
           v.setDistance(float('inf'))
           v.setColor("white")

        self.graph.get_all_v()[id1].setDistance(0)
        unVisited = []
        self.add_next_nodes(unVisited,id1)

        while len(unVisited) > 0:
            
            current = unVisited[0]
            unVisited = unVisited[1:]
            if self.graph.get_all_v()[current].getColor() != "white":
                unVisited = unVisited[1:]
                continue
            self.graph.get_all_v()[current].setColor("black")
            self.add_next_nodes(unVisited,current)
        
        shortestPath = [id2]
        self.generate_shortest_path(shortestPath,id2)
        shortestPath = shortestPath[::-1]
        return self.graph.get_all_v()[id2].getDistance(), shortestPath

    def generate_shortest_path(self,path:List[int],target:int) -> None:
        if(self.graph.get_all_v()[target].getPrev() != None):
            path.append(self.graph.get_all_v()[target].getPrev() )
            self.generate_shortest_path(path,self.graph.get_all_v()[target].getPrev())
        return

    def add_next_nodes(self,lst:List[dict], node_id:int)->None:
        for k,v in self.graph.all_out_edges_of_node(node_id).items():
            if self.graph.get_all_v()[k].getColor() == "white":
                if self.graph.get_all_v()[k].getDistance() > self.graph.get_all_v()[node_id].getDistance()+v:
                    self.graph.get_all_v()[k].setDistance(self.graph.get_all_v()[node_id].getDistance()+v)
                    self.graph.get_all_v()[k].setPrev(node_id)                
                idx = 0
                while idx<len(lst) and self.graph.get_all_v()[lst[idx]].getDistance() < self.graph.get_all_v()[k].getDistance():
                    idx+=1
                lst.insert(idx,k)
        
            


    def TSP(self, node_lst: List[int]) -> tuple[List[int], float]:
        best_lst = []
        best_length = float('inf')
        for i in range(len(node_lst)):
            temp = [n for n in node_lst]
            temp = temp[0:i] + temp[i+1:-1]
            path,path_len = self.TSP_recursive(i,temp)
            if(path_len<best_length):
                best_lst = path
                best_length = temp
        return best_lst
    def TSP_recursive(self,idx:int,node_lst: List[int]) -> tuple[List[int], float]:
        pass


    def centerPoint(self) -> tuple[int, float]:
        if False==self.isConnected():
            return None
        distanceMat = self.all_pairs_shortest_path()
        distances = [max(nodes) for nodes in  distanceMat]
        return distances.index(min(distances)), min(distances) 
    def isConnected(self) -> bool:
        pass
    def all_pairs_shortest_path(self) -> List[List[float]]:
        pass


    def plot_graph(self) -> None:
        pass
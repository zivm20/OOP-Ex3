from DiGraph import DiGraph
from GraphAlgo import GraphAlgo
import os
import time
import pandas as pd
import random

def check():
    
    create_benchmark( [50,100,500,800])
    benchmark()



def create_benchmark(graphs):
    
    graphs_folder = "../benchmark/graphs/"
    files = [ graphs_folder + f for f in os.listdir( graphs_folder[:-1])]
    params = []
    for f in files:
        os.remove(f)
    done = 0
    for graph_size in graphs:
        g = DiGraph()
        edges = []
        for n in range(graph_size):
            g.add_node(n)
            for _ in range(random.randint(5,15)):
                dest = random.randint(0,graph_size-1)
                if dest != n:
                    edges.append( [n,dest] )
        for edge in edges:
            g.add_edge(edge[0],edge[1],random.uniform(0.5,88))
        g_algo = GraphAlgo(g)
        name = str(graph_size) 
        trueName = name
       
        num = 2
        while trueName + ".json" in os.listdir( graphs_folder[:-1]):
            trueName = name + "("+str(num)+")"
            num+=1


        name = graphs_folder+trueName+".json"
        g_algo.save_to_json(name)
        #make 1 tests for shortest path
        test_path = [random.sample(range(0,graph_size),2)]

        #make 1 tests for tsp
        test_TSP = [random.sample(range(0,graph_size),random.randint(3,5)) for i in range(1)]

        path_str = ""
        for path in test_path:
            path_str = path_str+"("
            for node in path:
                path_str += str(node)+","
            path_str = path_str[:-1]+") "
        path_str = path_str[:-1]
        tsp_str = ""
        for path in test_TSP:
            tsp_str = tsp_str+"("
            for node in path:
                tsp_str += str(node)+","
            tsp_str = tsp_str[:-1]+") "
        tsp_str = tsp_str[:-1]
        temp = trueName+".json" + " / " + path_str + " / " + tsp_str
        params.append(temp)
        done+=1
        print("done",done,"out of",len(graphs))
        print()

    with open("../benchmark/params.txt", 'w') as f:
        for line in params:
            f.write(line+"\n")

    return params

def benchmark():
    #graphs_folder = "../benchmark/graphs"
    #graphs = {f:graphs_folder+"/" + f for f in  os.listdir( graphs_folder )}
    data = get_results()
    pd.DataFrame(data=data).to_csv("../benchmark/python_out.csv",index=False)



def get_results():
    lines = []
    with open('../benchmark/params.txt',"r") as f:
        lines = f.readlines()
    #structure:
    #json / (node1,node2) (node1,node2) (node1 node2)... / (node1,node2,....) (node1,node2,...)
    done = 0
    data = data = {"json_file":[], "node_size":[], "avg_edges_per_node":[], "time_load":[], "shortest_path":[] , "TSP":[] , "center_point":[]}
    for line in lines:
        out = ""
        items = line.strip().split(" / ")
        g = "../benchmark/graphs/"+items[0]
        out= out + items[0] + ", "
        g_algo = GraphAlgo()
        start = time.time()
        g_algo.load_from_json(g)
        end = time.time()
        print("loaded "+items[0])
        v_size = g_algo.get_graph().v_size()
        data["json_file"].append(items[0])
        data["node_size"].append(v_size)
        data["avg_edges_per_node"].append(g_algo.get_graph().e_size()*2/v_size)
        data["time_load"].append(end-start)
        out= out + str(v_size) + ", " + str(g_algo.get_graph().e_size()*2/v_size) + ", " + str(end-start) + ", "
        
        sp_params = items[1].split(" ")
        sum = 0
        for s in sp_params:
            nodes = [int(node) for node in s[1:-1].split(",")]
            start = time.time()
            g_algo.shortest_path(nodes[0],nodes[1])
            end = time.time()
            sum+=end-start
        out = out + str(sum/len(sp_params)) +", "
        print("done shortest_path for "+items[0])
        data["shortest_path"].append(sum/len(sp_params))

        sum=0
        sp_params = items[2].split(" ")
        for s in sp_params:
            nodes = [int(node) for node in s[1:-1].split(",")]
            start = time.time()
            g_algo.TSP(nodes)
            end = time.time()
            sum+=end-start
        out = out + str(sum/len(sp_params)) +", "
        print("done TSP for "+items[0])
        data["TSP"].append(sum/len(sp_params))


        start = time.time()
        g_algo.centerPoint()
        end = time.time()
        out = out + str(end-start)
        
        print("done center_point for "+items[0])
        data["center_point"].append(end-start)
        print(out)

        done+=1
        print("done",done,"out of",len(lines))
        
        print()
    return data



if __name__ == '__main__':
    check()

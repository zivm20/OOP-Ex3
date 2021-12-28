import sys
from GraphAlgo import GraphAlgo

def main(file):
    g_algo = GraphAlgo()
    
    g_algo.load_from_json("../data/"+file)
    
    g_algo.plot_graph()




if __name__ == "__main__":
   main(sys.argv[1])





















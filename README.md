## About the program


### Node

Holds all the information about a single node in the graph, this includes
* parents - map such that each key is the id of a node and each value is the weight of the edge (key,this Id)
* children - map such that each key is the id of a node and each value is the weight of the edge (this Id,key)
* color - used for dfs
* distance - used for finding the shortest path
* prev - previus node in some path, used for recovering the shortest path
* pos - the x,y,z values of the node on the display

### DiGraph

DiGraph has 2 field, mc and nodes, mc represents the amount of times we have changed the graph and nodes is a map such that it's keys are each node's id, and it's values are a Node object

### Graph Algo

Object that allows us to apply certain algorithms on our graph,  

* shortest_path(src,dest) - uses Dijkstra's algorithm to find the shortest path from node src to node dest and returns the path found and it's length
* TSP(node_list) - tries to find the minimum distance from each node n from node_list to the subgroup of node_list without node, we continue to do this recursivly for each subgroup untill we find the optimal path: https://www.youtube.com/watch?v=XaXsJJh-Q5Y
* centerPoint() - first we use Kosaraju’s DFS based algorithm to check if the graph is connected since if it's not, we cant determine the center point, then we use the floyd-warshall algorithm to find the shortest paths between all pairs, all that is left to do is to find the maximum path length for each node in our matrix, and find the node that has the lowest value of maximum path length






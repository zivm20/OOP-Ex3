class Node:
    def __init__(self,node_id: int, pos: tuple = None):
        self.parents = {}
        self.children = {}
        self.id = node_id
        self.pos = pos

    def getParents(self) -> dict:
        return self.parents
    def addParent(self,node_id: int,weight:float):
        self.parents[node_id]=weight
    
    def getChildren(self) -> dict:
        return self.children
    def addChild(self,node_id: int,weight:float):
        self.children[node_id]=weight

    def getId(self):
        return self.id
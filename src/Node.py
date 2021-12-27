import random
class Node:
    def __init__(self,node_id: int, pos: tuple = None):
        self.parents = {}
        self.children = {}
        self.id = node_id
        self.color = "white"
        self.distance = float('inf')
        self.prev = None
        if pos==None:
            pos =tuple([random.randrange(-9,10) for _ in range(3)])
        self.pos=pos


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


    def getColor(self) -> str:
        return self.color
    def setColor(self,c:str):
        self.color = c
    
    def getDistance(self) -> float:
        return self.distance
    def setDistance(self,d:float):
        self.distance = d

    def getPrev(self) -> int:
        return self.prev
    def setPrev(self,n:int):
        self.prev = n

    def getPos(self) -> tuple:
        return self.pos
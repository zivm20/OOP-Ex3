import pygame as pg
from pygame.locals import *
from Game_interface import Game
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
from GraphAlgo import GraphAlgo
import math

class Node_Sprite(pg.sprite.Sprite):
    def __init__(self,id,xy,radius):
        pg.sprite.Sprite.__init__(self)
        self.id=id
        self.original_img = pg.Surface((radius/2,radius/2), pg.SRCALPHA)
        pg.draw.circle(self.original_img, (255,0,0), (radius, radius), radius)

        self.selected = pg.Surface((radius/2,radius/2), pg.SRCALPHA)
        pg.draw.circle(self.selected, (255,0,0), (radius, radius), radius)
        pg.draw.circle(self.selected, (0,0,0), (radius, radius), radius,4)

        self.marked = pg.Surface((radius/2,radius/2), pg.SRCALPHA)
        pg.draw.circle(self.marked, (0,255,0), (radius, radius), radius)
        self.image = self.original_img
        self.rect = self.image.get_rect(center = xy)
    
    def isClicked(self,mx,my):
        return self.rect.collidepoint((mx,my))
    
    def update(self,selected_nodes,marked_nodes):
        if self.id in selected_nodes:
            self.image = self.selected
        elif self.id in marked_nodes:
            self.image = self.marked
        else:
            self.image = self.original_img

    def getId(self):
        return self.id




class Graph_plot(Game):
    def __init__(self,width:int=320, height:int=240,setupArgs=None):
        super().__init__(width,height,setupArgs)


    def setup(self,graph_alg:GraphAlgoInterface=None):
        self.radius = 2
        
        if graph_alg == None:
            graph_alg = GraphAlgo()
        self.graph_alg = graph_alg
        
        #nodes in selection
        self.selected_nodes = []
        #nodes/path marked that was retrieved from the algorithem
        self.marked_nodes = []
        self.marked_path = []
        #length of the path that was retrieved from the algorithem
        self.path_length = None
        
        #current algorithem being displayed
        self.current_algorithem = ""
        self.algorithem_done = True

        #node sprites
        node_pos = {k:v.getPos()[:-1]  for k,v in self.graph_alg.get_graph().get_all_v().items()}
        self.node_sprites = pg.sprite.Group([Node_Sprite(k,v,self.radius) for k,v in node_pos.items()])



        
    def eventHandler(self) -> bool:
        for event in pg.event.get():
            if event.type == pg.KEYUP:
                if self.handleKeyUp(pg.key.name(event.key)):
                    return True
            elif event.type == pg.MOUSEBUTTONUP:
                if self.algorithem_done == False and (self.current_algorithem == "TSP" or self.current_algorithem == "shortest_path"):
                    flg = False
                    for sprite in self.node_sprites:
                        if sprite.isClicked(event.pos[0],event.pos[1]):
                            flg = True
                            if sprite.getId() in self.selected_nodes:
                                self.selected_nodes.remove(sprite.getId())
                            else:
                                self.selected_nodes.append(sprite.getId())

                        if self.current_algorithem == "shortest_path" and len(self.selected_nodes)>1:
                            self.marked_nodes, self.path_length = self.graph_alg.TSP(self.selected_nodes)
                            for i in range(len(self.marked_nodes)-1):
                                self.marked_path.append( [self.marked_nodes[i],self.marked_nodes[i+1]])
                            self.selected_nodes = []
                            self.algorithem_done = True
                            return True
                    return flg
        return False



    def handleKeyUp(self,k) -> bool:
        alg_triggered=""
        if k == "t":
            alg_triggered = "TSP"
        elif k == "p":
            alg_triggered = "shortest_path"
        elif k == "c":
            alg_triggered = "center_point"
        elif k == "r":
            alg_triggered = "reset"

        if alg_triggered != "":
            #not preforming any algorithems and selected "center_point" algorithem
            if self.algorithem_done == True and alg_triggered == "center_point":
                self.marked_nodes = []
                self.marked_path = []
                self.selected_nodes = []
                self.path_length = None
                self.current_algorithem = alg_triggered
                temp, self.path_length = self.graph_alg.centerPoint()
                self.marked_nodes.append(temp)
                return True
            
            #not preforming any algorithems, reset marked nodes and selection
            elif self.algorithem_done == True or alg_triggered == "reset":
                flg = len(self.marked_nodes)>1 or len(self.marked_path)>1 or len(self.selected_nodes)>1
                self.marked_nodes = []
                self.marked_path = []
                self.selected_nodes = []
                self.path_length = None
                self.current_algorithem = alg_triggered
                if alg_triggered == "shortest_path" or alg_triggered == "TSP":
                    self.algorithem_done = False
                return flg
            
            #stop selection for TSP algorithem
            elif self.algorithem_done == False and self.current_algorithem == "TSP" and alg_triggered == "TSP":
                self.marked_nodes, self.path_length = self.graph_alg.TSP(self.selected_nodes)
                for i in range(len(self.marked_nodes)-1):
                    self.marked_path.append( [self.marked_nodes[i],self.marked_nodes[i+1]]  )
                self.selected_nodes = []
                self.algorithem_done = True
                return True
            
            #reset selection for shortest path if clicked again before selection ended
            elif self.algorithem_done == False and self.current_algorithem == "shortest_path" and alg_triggered == "shortest_path":
                flg = len(self.marked_nodes)>1 or len(self.marked_path)>1 or len(self.selected_nodes)>1
                
                self.marked_nodes = []
                self.marked_path = []
                self.selected_nodes = []
                self.path_length = None
                return flg
        return False

    def update(self):
        self.clock.tick(60)
        self.screen.fill(255,255,255)
        self.node_sprites.update(self.selected_nodes,self.marked_nodes)
        self.node_sprites.draw(self.screen)
        for srcId in self.graph_alg.get_graph().get_all_v():
            for destId,w in self.graph_alg.get_graph().all_out_edges_of_node(srcId).items():
                c = (0,0,0)
                if [srcId,destId] in self.marked_path:
                    c = (0,255,0)
                self.drawArrow(self.graph_alg.get_graph().get_all_v().get(srcId).getPos()[:-1], self.graph_alg.get_graph().get_all_v().get(destId).getPos()[:-1], c)
        pg.display.flip()


    def drawArrow(self,src,dest,color):
        pg.draw.line(self.screen,color,src,dest,2)
        rotation = math.degrees(math.atan2(src[1]-dest[1], dest[0]-src[0]))+90
        pg.draw.polygon(self.screen, (255, 0, 0), ((dest[0]+20*math.sin(math.radians(rotation)), dest[1]+20*math.cos(math.radians(rotation))), (dest[0]+20*math.sin(math.radians(rotation-120)), dest[1]+20*math.cos(math.radians(rotation-120))), (dest[0]+20*math.sin(math.radians(rotation+120)), dest[1]+20*math.cos(math.radians(rotation+120)))))




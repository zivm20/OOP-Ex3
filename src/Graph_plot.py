import pygame as pg
from pygame.locals import *
from Game_interface import Game
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface

import math

class Node_Sprite(pg.sprite.Sprite):
    def __init__(self,id,xy,width,height):
        pg.sprite.Sprite.__init__(self)
        self.id=id
        

        self.original_img = pg.Surface((width,height), pg.SRCALPHA)
        pg.draw.ellipse(self.original_img, (255,0,0), self.original_img.get_rect())

        self.selected = pg.Surface((width,height), pg.SRCALPHA)
        pg.draw.ellipse(self.selected, (255,0,0), self.selected.get_rect())
        pg.draw.ellipse(self.selected, (0,0,0), self.selected.get_rect(), 4)

        self.marked = pg.Surface((width,height), pg.SRCALPHA)
        pg.draw.ellipse(self.marked, (0,255,0), self.marked.get_rect())
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
    def __init__(self,width:int=900, height:int=900,setupArgs=None):
        super().__init__(width,height,setupArgs)


    def setup(self,graph_alg:GraphAlgoInterface=None):
        
        
        if graph_alg == None:
            graph_alg = GraphAlgoInterface()
        self.graph_alg = graph_alg

        self.maxX = max([v.getPos()[0] for k,v in self.graph_alg.get_graph().get_all_v().items()]) 
        self.minX = min([v.getPos()[0] for k,v in self.graph_alg.get_graph().get_all_v().items()])
        self.maxY = max([v.getPos()[1] for k,v in self.graph_alg.get_graph().get_all_v().items()])
        self.minY = min([v.getPos()[1] for k,v in self.graph_alg.get_graph().get_all_v().items()])

        self.scaleX = (self.width*0.8)/(self.maxX-self.minX)
        self.scaleY = (self.height*0.8)/(self.maxY-self.minY)

        self.radius = 100
        newDim = (self.radius,self.radius)
        
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
        self.node_pos = {k:self.remap(v.getPos()[:-1])  for k,v in self.graph_alg.get_graph().get_all_v().items()}
        self.node_sprites = pg.sprite.Group([Node_Sprite(k,v,newDim[0],newDim[1]) for k,v in self.node_pos.items()])
        for i in self.node_pos:
            print( self.graph_alg.get_graph().get_all_v()[i].getPos()[:-1],"->",self.node_pos[i])

        self.font = pg.font.Font(pg.font.get_default_font(), 36)
        



        
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
                            print(self.path_length)
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
                print(self.path_length)
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
                    self.marked_path.append([self.marked_nodes[i],self.marked_nodes[i+1]])
                self.selected_nodes = []
                self.algorithem_done = True
                print(self.path_length)
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
        self.screen.fill((255,255,255))
        
        self.node_sprites.update(self.selected_nodes,self.marked_nodes)
        self.node_sprites.draw(self.screen)
        for srcId in self.graph_alg.get_graph().get_all_v():
            
            text_surface = self.font.render(srcId, antialias=True, color=(0, 0, 0))
            
            text_rect = text_surface.get_rect()
            text_rect.center(self.node_pos[srcId])
            self.screen.blit(text_surface, text_rect)

            for destId,w in self.graph_alg.get_graph().all_out_edges_of_node(srcId).items():
                c = (0,0,0)
                edge_occupied = False
                if [srcId,destId] in self.marked_path:
                    c = (0,255,0)
                if srcId in self.graph_alg.get_graph().all_out_edges_of_node(destId) and [destId,srcId] in self.marked_path and ([srcId,destId] in self.marked_path)==False:
                    continue
                else:
                    self.drawArrowBody(self.graph_alg.get_graph().get_all_v().get(srcId).getPos()[:-1], self.graph_alg.get_graph().get_all_v().get(destId).getPos()[:-1], c)
        for srcId in self.graph_alg.get_graph().get_all_v():
            for destId,w in self.graph_alg.get_graph().all_out_edges_of_node(srcId).items():
                c = (0,0,0)
                if [srcId,destId] in self.marked_path:
                    c = (0,255,0)
                self.drawArrowHead(self.graph_alg.get_graph().get_all_v().get(srcId).getPos()[:-1], self.graph_alg.get_graph().get_all_v().get(destId).getPos()[:-1], c)

        pg.display.flip()


    def drawArrowBody(self,src_raw,dest_raw,color):
        src = self.remap(src_raw)
        dest = self.remap(dest_raw)
        
        rotation = math.degrees(math.atan2(src[1]-dest[1], dest[0]-src[0]))+90
        dest = dest[0]-(20+self.radius/2)*math.sin(math.radians(rotation)), dest[1]-(20+self.radius/2)*math.cos(math.radians(rotation))
        src = src[0]+(self.radius/2)*math.sin(math.radians(rotation)), src[1]+(self.radius/2)*math.cos(math.radians(rotation))
        pg.draw.line(self.screen,color,src,dest,2)
        
            
    def drawArrowHead(self,src_raw,dest_raw,color):
        src = self.remap(src_raw)
        dest = self.remap(dest_raw)
        

        rotation = math.degrees(math.atan2(src[1]-dest[1], dest[0]-src[0]))+90
        dest = dest[0]-(20+self.radius/2)*math.sin(math.radians(rotation)), dest[1]-(20+self.radius/2)*math.cos(math.radians(rotation))
        src = src[0]+(self.radius/2)*math.sin(math.radians(rotation)), src[1]+(self.radius/2)*math.cos(math.radians(rotation))
        
        
        pg.draw.polygon(self.screen, color, ((dest[0]+20*math.sin(math.radians(rotation)), dest[1]+20*math.cos(math.radians(rotation))), (dest[0]+20*math.sin(math.radians(rotation-90)), dest[1]+20*math.cos(math.radians(rotation-90))), (dest[0]+20*math.sin(math.radians(rotation+90)), dest[1]+20*math.cos(math.radians(rotation+90)))))



    def remap(self,point):
        x = (point[0] - self.minX)*self.scaleX + self.width*0.1
        
        y = (point[1] - self.minY)*self.scaleY + self.height*0.1
        return x,y






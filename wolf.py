import pygame
import utils
import settings
import random
from threading import Timer

class Wolf(pygame.sprite.Sprite):
    def __init__(self,x,y,window,Land,player):
        pygame.sprite.Sprite.__init__(self)
        self.frames = {
        "down" : pygame.image.load("Images/Wolf/1.png").convert_alpha(),
        "right" : pygame.image.load("Images/Wolf/2.png").convert_alpha(),
        "left" : pygame.image.load("Images/Wolf/3.png").convert_alpha(),
        "up" : pygame.image.load("Images/Wolf/4.png").convert_alpha(),
        }
        self.image = self.frames["down"]
        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = self.y*16 - window.x
        self.rect.y = self.x*16 - window.y
        self.Land = Land
        self.player = player
        self.keep_moving = True
        self.move()

    def set_image(self,x1,y1,x2,y2):
        if x1 < x2:
            self.image = self.frames["left"]
        elif x1 > x2:
            self.image = self.frames["right"]
        elif y1 < y2:
            self.image = self.frames["down"]
        elif y1 > y2:
            self.image = self.frames["up"]

    def position(self,window):
        self.rect.x = window.x + self.x*16
        self.rect.y = window.y + self.y*16

    def move(self):
        ox = self.x
        oy = self.y
        dirs = [(1,0),(-1,0),(0,1),(0,-1),(0,0),(0,0),(0,0)]
        if utils.distance(self.x,self.y,self.player.x,self.player.y) < settings.wolf_distance:
            path = self.astar(self.x,self.y,self.player.x,self.player.y)
            if path:
                try:
                    self.x = path[-2][0]
                    self.y = path[-2][1]
                except IndexError:
                    pass
        else:
            neighbors = []
            for direction in dirs:
                if (self.x+direction[0],self.y+direction[1]) in self.Land:
                    neighbors.append((direction[0],direction[1]))
            neighbor = random.choice(neighbors)
            self.x += neighbor[0]
            self.y += neighbor[1]
        self.set_image(ox,oy,self.x,self.y)
        if self.keep_moving:
            self.t = Timer(0.2,self.move).start()

    def astar(self,x1,y1,x2,y2):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        # The set of nodes already evaluated.
        closed_set = []
        # The set of currently discovered nodes still to be evaluated.
        # Initially, only the start node is known.
        open_set = [(x1,y1)]
        # For each node, which node it can most efficiently be reached from.
        # If a node can be reached from many nodes, cameFrom will eventually contain the
        # most efficient previous step.
        came_from = {}

        # For each node, the cost of getting from the start node to that node.
        g_score = {}
        # The cost of going from start to start is zero.
        g_score[(x1,y1)] = 0
        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. That value is partly known, partly heuristic.
        f_score = {}
        # For the first node, that value is completely heuristic.
        f_score[(x1,y1)] = utils.distance(x1,y1,x2,y2)
        depth = 0
        while open_set and depth < settings.wolf_astar_depth:
            current = min(open_set,key=f_score.get)
            if current == (x2,y2):
                total_path = [current]
                while current in came_from.keys():
                    current = came_from[current]
                    total_path.append(current)
                return total_path

            open_set.remove(current)
            closed_set.append(current)
            neighbors = []
            for direction in dirs:
                if (current[0]+direction[0],current[1]+direction[1]) in self.Land:
                    neighbors.append((current[0]+direction[0],current[1]+direction[1]))
            for neighbor in neighbors:
                if neighbor in closed_set:
                    continue		# Ignore the neighbor which is already evaluated.
                # The distance from start to a neighbor
                tentative_g_score = g_score[current] + 1
                if neighbor not in open_set:	# Discover a new node
                    open_set.append(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue		# This is not a better path.

                # This path is the best until now. Record it!
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + utils.distance(neighbor[0],neighbor[1], x2,y2)
                depth += 1
        return None

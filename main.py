#Copyright (c) 2016 Copyright Andre van Tonder All Rights Reserved.
import os
import sys
import random
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
from player import *
from message import *
from gold import *
from wolf import *
from chest import *
from gui import *
import utils
import settings
import datetime

class Game(object):
    """
    Object that controls the game
    """
    def __init__(self,window):
        self.player = Player(40,16,window)
        self.characters = pygame.sprite.Group()
        self.characters.add(self.player)
        self.messages = pygame.sprite.Group()
        self.gold_pieces = pygame.sprite.Group()
        self.wolves = pygame.sprite.Group()
        self.chests = pygame.sprite.Group()
        self.animated_gold = pygame.sprite.Group()
        self.gold = 0
        self.all_gold = 0
        self.gold_taken = {}
        self.chest_pos = {}
        self.window = window
        self.change_map("Maps/1.tmx",self.player.x,self.player.y)

    def update(self):
        """
        Update the game
        """
        for g in self.animated_gold:
            g.move()
        self.messages.empty()
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        for direction in dirs:
            if (self.player.x+direction[0],self.player.y+direction[1]) in self.map.Signs:
                sign = self.map.Signs[(self.player.x+direction[0],self.player.y+direction[1])]
                self.draw_message(sign.properties["Message"],sign.x,sign.y)
            if (self.player.x+direction[0],self.player.y+direction[1]) in self.chest_pos:
                chest = self.chest_pos[(self.player.x+direction[0],self.player.y+direction[1])]
                if chest.map == self.map_file:
                    self.draw_message("Contains: {0} Gold. E>Give Q>Take".format(str(chest.gold)),chest.rect.x,chest.rect.y)
        gold_pieces = pygame.sprite.spritecollide(self.player,self.gold_pieces, True)
        for gold in gold_pieces:
            self.gold += gold.worth
            self.gold_taken[self.map_file].append((gold.x,gold.y))
            self.animated_gold.add(AnimatedGold(gold))
        for w in self.wolves:
            if w.x == self.player.x and w.y == self.player.y:
                self.gold = 0
        self.all_gold = self.gold
        for chest in self.chests:
            self.all_gold += chest.gold

    def down(self):
        screen = pygame.display.get_surface()
        if (self.player.x,self.player.y+1) in self.map.Land:
            if screen.get_height() - abs(self.player.rect.y - self.window.y) > 4*16:
                self.player.down()
            elif abs(self.window.y)+screen.get_height()+8 <= self.map.Map.height*16:
                self.window.y -= 16
                self.player.down()
            else:
                self.player.down()
        elif (self.player.x,self.player.y+1) in self.map.Doors.keys():
            obj = self.map.Doors[(self.player.x,self.player.y+1)]
            self.player.down()
            self.change_map(obj.properties["Connected"],obj.properties["GoX"],obj.properties["GoY"])

    def right(self):
        screen = pygame.display.get_surface()
        if (self.player.x+1,self.player.y) in self.map.Land:
            if screen.get_width() - abs(self.player.rect.x - self.window.x) > 4*16:
                self.player.right()
            elif abs(self.window.x)+screen.get_width()+16 <= self.map.Map.width*16:
                self.window.x -= 16
                self.player.right()
            else:
                self.player.right()
        elif (self.player.x+1,self.player.y) in self.map.Doors.keys():
            obj = self.map.Doors[(self.player.x+1,self.player.y)]
            self.map = Map(obj.properties["Connected"])
            self.player.right()
            self.change_map(obj.properties["Connected"],obj.properties["GoX"],obj.properties["GoY"])

    def left(self):
        screen = pygame.display.get_surface()
        if (self.player.x-1,self.player.y) in self.map.Land:
            if self.player.rect.x > 4*16:
                self.player.left()
            elif self.window.x != 0:
                self.window.x += 16
                self.player.left()
            else:
                self.player.left()
        elif (self.player.x-1,self.player.y) in self.map.Doors.keys():
            obj = self.map.Doors[(self.player.x-1,self.player.y)]
            self.player.left()
            self.change_map(obj.properties["Connected"],obj.properties["GoX"],obj.properties["GoY"])

    def up(self):
        screen = pygame.display.get_surface()
        if (self.player.x,self.player.y-1) in self.map.Land:
            if self.player.rect.y > 4*16:
                self.player.up()
            elif self.window.y != 0:
                self.window.y += 16
                self.player.up()
            else:
                self.player.up()
        elif (self.player.x,self.player.y-1) in self.map.Doors.keys():
            obj = self.map.Doors[(self.player.x,self.player.y-1)]
            self.player.up()
            self.change_map(obj.properties["Connected"],obj.properties["GoX"],obj.properties["GoY"])

    def take(self):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        for direction in dirs:
            if (self.player.x+direction[0],self.player.y+direction[1]) in self.chest_pos:
                chest = self.chest_pos[(self.player.x+direction[0],self.player.y+direction[1])]
                if chest.map == self.map_file:
                    self.gold += chest.take(chest.gold)

    def give(self):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        for direction in dirs:
            if (self.player.x+direction[0],self.player.y+direction[1]) in self.chest_pos:
                chest = self.chest_pos[(self.player.x+direction[0],self.player.y+direction[1])]
                if chest.map == self.map_file:
                    chest.give(self.gold)
                    self.gold = 0

    def draw_message(self,message,x,y):
        message = Message(x,y,message,self.window)
        self.messages.add(message)

    def change_map(self,map_file,x,y):
        for w in self.wolves:
            w.keep_moving = False
        self.wolves.empty()

        self.map_file = map_file
        x = int(x)
        y = int(y)
        self.map = Map(map_file)
        self.player.x = x
        self.player.y = y
        self.window.center(x*16,y*16,self.map.Map.width*16,self.map.Map.height*16)
        if self.map_file not in self.gold_taken.keys():
            self.gold_taken[self.map_file] = []
        self.gold_pieces.empty()
        for pos,obj in self.map.Gold.items():
            if (pos[0],pos[1]) not in self.gold_taken[self.map_file]:
                self.gold_pieces.add(Gold(pos[0],pos[1],self.window,obj.image,obj.properties["Worth"]))
        for pos,image in self.map.Chests.items():
            if (pos[0],pos[1]) not in self.chest_pos:
                chest = Chest(pos[0],pos[1],self.window,image,self.map_file)
                self.chests.add(chest)
                self.chest_pos[pos[0],pos[1]] = chest
        if self.map.Map.width > 30:
            for i in range(random.randint(settings.min_wolves,settings.max_wolves)):
                pos = random.choice(self.map.Land)
                self.wolves.add(Wolf(pos[0],pos[1],self.window,self.map.Land,self.player))

    def end(self):
        for w in self.wolves:
            w.keep_moving = False

class Window(object):
    def __init__(self):
        self.x = 0
        self.y = 0
    def center(self,x,y,m_width,m_height):
        """
        Center the window on a certain coordinate
        without showing any non-map
        """
        screen = pygame.display.get_surface()
        cx = -(x-screen.get_width()/2)
        cy = -(y-screen.get_height()/2)
        if x-screen.get_width()/2 < 0:
            self.x = cx + (x-screen.get_width()/2)
        elif x+screen.get_width()/2 > m_width:
            self.x = cx+(x-m_width+screen.get_width()/2)
        else:
            self.x = cx
        if y-screen.get_height()/2 < 0:
            self.y = cy + (y-screen.get_height()/2)
        elif y+screen.get_height()/2 > m_height:
            self.y = cy+(y-m_height+screen.get_height()/2)
        else:
            self.y = cy

class Map(object):
    """
    An object that stores the .tmx files information
    """
    def __init__(self,map_file):
        self.make_map(map_file)

    def make_map(self,map_file):
        """
        Get the map from the .tmx file
        """
        self.Land = []
        self.Doors = {}
        self.Signs = {}
        self.Chests = {}
        self.Gold= {}
        self.Map = load_pygame(map_file)
        self.image = pygame.Surface([self.Map.width*16,self.Map.height*16]).convert()
        self.overlay = pygame.Surface([self.Map.width*16,self.Map.height*16], pygame.SRCALPHA, 32).convert_alpha()
        layer = self.get_layer("Land")
        if layer:
            for x, y, image in layer.tiles():
                self.Land.append((x,y))
                self.image.blit(image,(x*16,y*16))
        layer = self.get_layer("Sea")
        if layer:
            for x, y, image in layer.tiles():
                self.image.blit(image,(x*16,y*16))
        layer = self.get_layer("Ground Overlay")
        if layer:
            for x, y, image in layer.tiles():
                self.image.blit(image,(x*16,y*16))
        layer = self.get_layer("Objects")
        if layer:
            for x, y, image in layer.tiles():
                self.image.blit(image,(x*16,y*16))
                self.Land.remove((x,y))
        layer = self.get_layer("Signs")
        if layer:
            for obj in layer:
                self.image.blit(obj.image,(obj.x,obj.y))
                self.Signs[(int(obj.x/16),int(obj.y/16))] = obj
                try:
                    self.Land.remove((int(obj.x/16),int(obj.y/16)))
                except ValueError:
                    print(obj.x,obj.y)
        layer = self.get_layer("Chests")
        if layer:
            for x, y, image in layer.tiles():
                self.Chests[(x,y)] = image
                self.Land.remove((x,y))
        layer = self.get_layer("Gold")
        if layer:
            for obj in layer:
                self.Gold[(int(obj.x/16),int(obj.y/16))] = obj
        layer = self.get_layer("Open Doors")
        if layer:
            for obj in layer:
                self.image.blit(obj.image,(obj.x,obj.y))
                self.Doors[(int(obj.x/16),int(obj.y/16))] = obj
        layer = self.get_layer("Doors/Windows/Roofs")
        if layer:
            for x, y, image in layer.tiles():
                self.overlay.blit(image,(x*16,y*16))
        layer = self.get_layer("Roof Overlay")
        if layer:
            for x, y, image in layer.tiles():
                self.overlay.blit(image,(x*16,y*16))

    def get_layer(self,name):
        """
        Get the layer form the map if it exists
        """
        try:
            return self.Map.get_layer_by_name(name)
        except ValueError:
            return None

class App(object):
    """
    This is the main class for our application.
    It manages our event and game loops.
    """
    def __init__(self):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and set our starting color to black.
        """
        self.screen = pygame.display.get_surface() # Get reference to the display.
        self.clock = pygame.time.Clock() # Create a clock to restrict framerate.
        self.fps = 60 # Define your max framerate.
        self.done = False # A flag to tell our game when to quit.
        self.keys = pygame.key.get_pressed() # All the keys currently held.
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.sprites = pygame.sprite.Group()
        self.top_sprites = pygame.sprite.Group()
        if pygame.mixer:
            pygame.mixer.music.load("Sounds/1.mp3")
            pygame.mixer.music.play(-1)
        self.window = Window()
        self.game = Game(self.window)

    def get_sprites(self):
        """
        Get the sprites from the game class
        """
        self.sprites.empty()
        self.top_sprites.empty()
        for c in self.game.characters:
            c.position(self.window)
        for m in self.game.messages:
            m.position(self.window)
        for g in self.game.gold_pieces:
            g.position(self.window)
        for w in self.game.wolves:
            w.position(self.window)
        for c in self.game.chests:
            if c.map == self.game.map_file:
                c.position(self.window)
                self.sprites.add(c)
        self.sprites.add(self.game.animated_gold)
        self.sprites.add(self.game.characters)
        self.sprites.add(self.game.gold_pieces)
        self.sprites.add(self.game.wolves)
        self.top_sprites.add(self.game.messages)

    def check_keybindings(self):
        """
        Check for keyboard presses
        """
        if (self.keys[pygame.K_RALT] or self.keys[pygame.K_LALT]) and self.keys[pygame.K_s]:
            pygame.image.save(self.screen,"Screenshot1.png")
        elif self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]:
            self.game.right()
        elif self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]:
            self.game.left()
        elif self.keys[pygame.K_DOWN] or self.keys[pygame.K_s]:
            self.game.down()
        elif self.keys[pygame.K_UP] or self.keys[pygame.K_w]:
            self.game.up()
        elif self.keys[pygame.K_e]:
            self.game.give()
        elif self.keys[pygame.K_q]:
            self.game.take()

    def event_loop(self):
        """
        Our event loop; called once every frame.  Only things relevant to
        processing specific events should be here.  It should not
        contain any drawing/rendering code.
        """
        pygame.event.pump()
        for event in pygame.event.get():  # Check each event in the event queue.
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                # If the user presses escape or closes the window we're done.
                self.game.end()
                self.done = True
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                # Update keys when a key is pressed or released.
                self.keys = pygame.key.get_pressed()
                self.check_keybindings()
            elif event.type in (pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP):
                self.mouse_buttons = pygame.mouse.get_pressed()
    def main_loop(self):
        """
        Our game loop. It calls the event loop; updates the display;
        restricts the framerate; and loops.
        """
        while not self.done:
            self.event_loop() # Run the event loop every frame.
            self.game.update()
            self.get_sprites()
            self.screen.fill([0,0,0])
            self.screen.blit(self.game.map.image,(self.window.x,self.window.y))
            self.sprites.draw(self.screen)
            self.screen.blit(self.game.map.overlay,(self.window.x,self.window.y))
            self.top_sprites.draw(self.screen)
            gold = utils.draw_font("Gold: " +
            str(self.game.gold),24,settings.FONT)
            self.screen.blit(gold,(self.screen.get_width()-gold.get_width(),self.screen.get_height()-gold.get_height()))
            all_gold = utils.draw_font("All Gold: " +
            str(self.game.all_gold),24,settings.FONT)
            self.screen.blit(all_gold,(self.screen.get_width()-all_gold.get_width(),self.screen.get_height()-all_gold.get_height()-gold.get_height()-4))
            pygame.display.update() # Make updates to screen every frame.
            self.clock.tick(self.fps) # Restrict framerate of program.
            print("fps:", self.clock.get_fps())

    def quit(self):
        self.done = True

class MainMenu(object):
    """
    This is the main class for our application.
    It manages our event and game loops.
    """
    def __init__(self):
        """
        Get a reference to the screen (created in main); define necessary
        attributes; and set our starting color to black.
        """
        self.screen = pygame.display.get_surface() # Get reference to the display.
        self.clock = pygame.time.Clock() # Create a clock to restrict framerate.
        self.fps = 60 # Define your max framerate.
        self.done = False # A flag to tell our game when to quit.
        self.keys = pygame.key.get_pressed() # All the keys currently held.
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.sprites = pygame.sprite.Group()
        self.make_gui()

    def make_gui(self):
        self.actions = {}
        self.buttons = pygame.sprite.Group()
        b1 = Button("Start",self.screen.get_width()/2,10)
        b1.rect.x -= b1.rect.width/2
        b2 = Button("Quit",self.screen.get_width()/2,b1.rect.bottom+10)
        b2.rect.x -= b2.rect.width/2
        self.buttons.add(b1,b2)
        self.actions[b1] = [self.quit]
        self.actions[b2] = [quit]
        self.sprites.add(self.buttons)

    def check_keybindings(self):
        """
        Check for keyboard presses
        """
        if (self.keys[pygame.K_RALT] or self.keys[pygame.K_LALT]) and self.keys[pygame.K_s]:
            pygame.image.save(self.screen,"Screenshot1.png")

    def check_buttons(self):
        for button in self.buttons:
            if button.rect.collidepoint(pygame.mouse.get_pos()) and self.mouse_buttons[0] == 1:
                self.actions[button][0](*self.actions[button][1:])

    def event_loop(self):
        """
        Our event loop; called once every frame.  Only things relevant to
        processing specific events should be here.  It should not
        contain any drawing/rendering code.
        """
        pygame.event.pump()
        for event in pygame.event.get():  # Check each event in the event queue.
            if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                # If the user presses escape or closes the window we're done.
                pygame.quit()
                quit()
            elif self.keys[pygame.K_RETURN]:
                self.done = True
            elif event.type in (pygame.KEYUP, pygame.KEYDOWN):
                # Update keys when a key is pressed or released.
                self.keys = pygame.key.get_pressed()
                self.check_keybindings()
            elif event.type in (pygame.MOUSEBUTTONDOWN,pygame.MOUSEBUTTONUP):
                self.mouse_buttons = pygame.mouse.get_pressed()
                self.check_buttons()

    def main_loop(self):
        """
        Our game loop. It calls the event loop; updates the display;
        restricts the framerate; and loops.
        """
        while not self.done:
            self.event_loop() # Run the event loop every frame.
            self.screen.fill(settings.MENU_BACKGROUND)
            image = pygame.image.load("Images/Wolf/3.png")
            image = pygame.transform.scale(image,[320,320])
            self.screen.blit(image,(0,0))
            image = pygame.image.load("Images/Bob/1.png")
            image = pygame.transform.scale(image,[320,320])
            self.screen.blit(image,(image.get_width()+10,0))
            self.sprites.draw(self.screen)
            pygame.display.update() # Make updates to screen every frame.
            self.clock.tick(self.fps) # Restrict framerate of program.
            print("fps:", self.clock.get_fps())

    def quit(self):
        self.done = True

def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    pygame.init() # Initialize Pygame.
    pygame.display.set_caption("Life of Robert") # Set the caption for the window.
    infoObject = pygame.display.Info()
    pygame.display.set_mode((infoObject.current_w, infoObject.current_h),pygame.FULLSCREEN) # Prepare the screen.
    pygame.display.set_icon(pygame.transform.scale(pygame.image.load(settings.ICON),(64,64)))
    pygame.key.set_repeat(100,100)
    MainMenu().main_loop()
    App().main_loop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

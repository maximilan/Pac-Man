from random import randint
from math import sqrt
class Character:
    def __init__(self,design,canvas):
        self.design = design
        self.canvas = canvas
        self.richtung = None
    def beweg(self,x,y):
        for i in range(len(self.design)):
            self.canvas.move(self.design[i], x, y)
    def steuer(self, richtung):
        if richtung == "Up":
            self.beweg(0, -10)
        elif richtung == "Down":
            self.beweg(0, 10)
        elif richtung == "Left":
            self.beweg(-10, 0)
        elif richtung == "Right":
            self.beweg(10, 0)
    def return_current_tile(self):
        return self.current_tile
    def get_middle(self):
        pos = self.canvas.coords(self.design[0])
        x = (pos[0] + pos[2])/2
        y = (pos[1] + pos[3])/3
        return x, y


#####################################################################    
class Enemy(Character):
    def __init__(self,design,canvas,current_tile):
        self.design = design
        self.canvas = canvas
        self.current_tile = current_tile
        self.direction = "Down"

    def get_anti_direction(self, direction):
        if direction == "Up":
            return "Down"
        if direction == "Down":
            return "Up"
        if direction == "Left":
            return "Right"
        if direction == "Right":
            return "Left"

    def check_kill(self, target):
        if self.distanz(target) < 30:
            return True
        else:
            return False
    def move(self, target):
        playcoords = target.return_coords()
        selfcoords = self.current_tile.get_coords()
        x = selfcoords[0]-playcoords[0]
        y = selfcoords[1]-playcoords[1]
        if abs(x) > abs(y):
            if x < 0:
                ziel = "Right"
            else:
                ziel = "Left"
            if y < 0:
                otherziel = "Down"
            else:
                otherziel = "Up"
        else:
            if y < 0:
                ziel = "Down"
            else:
                ziel = "Up"
            if x < 0:
                otherziel = "Right"
            else:
                otherziel = "Left"
        newDir = False
        directions = self.current_tile.get_directions()
        if ziel != self.get_anti_direction(self.direction) and ziel in directions:
            self.current_tile = self.current_tile.switch(ziel)
            self.steuer(ziel)
            self.direction = ziel
        elif otherziel != self.get_anti_direction(self.direction) and otherziel in directions:
            self.current_tile = self.current_tile.switch(otherziel)
            self.steuer(otherziel)
            self.direction = otherziel
        elif len(directions) == 1:
            posib = randint(0, len(directions)-1)
            self.current_tile = self.current_tile.switch(directions[posib])
            self.steuer(directions[posib])
            self.direction = directions[posib]
        else:
            while newDir != True:
                posib = randint(0, len(directions)-1)
                if directions[posib] != self.get_anti_direction(self.direction):
                     self.current_tile = self.current_tile.switch(directions[posib])
                     self.steuer(directions[posib])
                     self.direction = directions[posib]
                     newDir = True

    def delete(self):
        for i in range(len(self.design)):
            self.canvas.delete(self.design[i])
    def distanz(self, target):
        x1, y1 = self.get_middle()
        x2, y2 = target.get_middle()
        return sqrt((x2 -x1)**2 + (y2 -y1)**2)


#############################################################################################    
class Player(Character):
    def __init__(self,design, canvas, current_tile):
        super().__init__(design, canvas)
        self.richtung = None
        self.current_tile = current_tile
        self.yellow1 = list()
        self.yellow2 = list()
        self.eat = "Close"
        self.yellow1status = "black"
        self.yellow2status = "black"

    def set_eat(self):
        if self.yellow1status == "yellow":
            for i in range(len(self.yellow1)):
                self.canvas.itemconfig(self.yellow1[i], fill = 'yellow',outline = 'yellow')
        else:
            for i in range(len(self.yellow1)):
                self.canvas.itemconfig(self.yellow1[i], fill = 'black',outline = 'black')
        if self.yellow2status == "yellow":
            for i in range(len(self.yellow2)):
                self.canvas.itemconfig(self.yellow2[i], fill = 'yellow',outline = 'yellow')
        else:
            for i in range(len(self.yellow2)):
                self.canvas.itemconfig(self.yellow2[i], fill = 'black', outline = 'black')
    def set_richtung(self, richtung):
        self.richtung = richtung
        if self.richtung in ["Left", "Right", "Up", "Down"]:
            x, y, x2, y2 = self.canvas.coords(self.design[0])
            for i in range(len(self.design)-1, -1, -1):
                self.canvas.delete(self.design[i])
                del self.design[i]
            del self.yellow1[:]
            del self.yellow2[:]
            id1 = self.canvas.create_oval(x, y, x+45, y+45, fill='yellow')
            if self.richtung == "Up":
                id2 = self.canvas.create_polygon(x+20, y+25, x+13, y, x+27,y, fill='black')
                id3 = self.canvas.create_oval(x+11.5,y+22,x+14.5, y+25, fill='black')
                id4 = self.canvas.create_polygon(x+20, y+25, x+13, y+3, x+16, y+3, fill = 'black')
                id5 = self.canvas.create_polygon(x+20, y+25, x+27, y+3, x+24, y+3, fill = 'black')
            elif self.richtung == "Right":
                id2 = self.canvas.create_polygon(x+20, y+25, x+45, y+17, x+45, y+32, fill='black')
                id3 = self.canvas.create_oval(x+32, y+10, x+35, y+13, fill='black')
                id4 = self.canvas.create_polygon(x+20, y+25, x+42, y+17, x+42, y+20, fill = 'black')
                id5 = self.canvas.create_polygon(x+20, y+25, x+42, y+32, x+42, y+29, fill = 'black')
            elif self.richtung == "Down":
                id2 = self.canvas.create_polygon(x+20, y+20, x+13, y+45, x+27, y+45, fill='black')
                id3 = self.canvas.create_oval(x+32, y+30, x+35, y+33, fill='black')
                id4 = self.canvas.create_polygon(x+20, y+20, x+13, y+42, x+16, y+42, fill = 'black')
                id5 = self.canvas.create_polygon(x+20, y+20, x+27, y+42, x+24, y+42, fill = 'black')
            elif self.richtung == "Left":
                id2 = self.canvas.create_polygon(x+23, y+25, x, y+17, x, y+32, fill='black')
                id3 = self.canvas.create_oval(x+11.5,y+10,x+14.5, y+13, fill='black')
                id4 = self.canvas.create_polygon(x+23, y+25, x+3, y+17, x+3, y+20, fill = 'black')
                id5 = self.canvas.create_polygon(x+23, y+25, x+3, y+32, x+3, y+29, fill = 'black')
            self.design.append(id1)
            self.design.append(id2)
            self.design.append(id3)
            self.design.append(id4)
            self.design.append(id5)
            self.yellow1.append(id4)
            self.yellow1.append(id5)
            self.yellow2.append(id2)
            self.set_eat()
            
    def move(self):
        if self.eat == "Close":
            if self.yellow1status == "black":
                self.yellow1status = "yellow"
            else:
                self.yellow2status = "yellow"
                self.eat = "Open"
        elif self.eat == "Open":
            if self.yellow2status == "yellow":
                self.yellow2status = "black"
            else:
                self.yellow1status = "black"
                self.eat = "Close"
        re = self.current_tile.check_point()
        if re == 1:
            self.set_eat()
        else:
            self.yellow1status = "black"
            self.yellow2status = "black"
            self.eat = "Close"
            self.set_eat()
        directions = self.current_tile.get_directions()
        if self.richtung in directions:
            self.steuer(self.richtung)
            self.current_tile = self.current_tile.switch(self.richtung)
        return re
    def return_coords(self):
        return self.current_tile.get_coords()
    def return_yellow(self):
        self.yellow1status = "black"
        self.yellow2status = "black"
        self.eat = "Close"
        self.set_eat()
        return self.design[0]

#####################################################################################
class Tile():
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        canvas.create_rectangle(x, y, x+50, y+50, fill='grey80')

######################################################################################        
class Path():
    def __init__(self,canvas,x,y):
        self.canvas = canvas
        self.design = self.canvas.create_rectangle(x, y, x+10, y+10, fill='black')
        self.coordinate = [x,y]
        self.function = None
        self.directions = []
        self.neighbor_tiles = {}
        self.point = True
        self.pointdesign = self.canvas.create_oval(x+4, y+4, x+6, y+6, fill='yellow')
    def get_coordinate(self):
        return self.coordinate
    def link_tile(self, direction, tile):
        self.neighbor_tiles[direction] = tile
    def get_function(self, coordinates, tileslist):
        self.neighbor_tiles = {}
        del self.directions[:]
        if self.change_coords(10, 0) in coordinates:
            self.directions.append("Right")
            for i in range(len(coordinates)):
                if coordinates[i] == self.change_coords(10, 0):
                    self.link_tile("Right", tileslist[i])
        if self.change_coords(-10, 0) in coordinates:
            self.directions.append("Left")
            for i in range(len(coordinates)):
                if coordinates[i] == self.change_coords(-10, 0):
                    self.link_tile("Left", tileslist[i])
        if self.change_coords(0, 10) in coordinates:
            self.directions.append("Down")
            for i in range(len(coordinates)):
                if coordinates[i] == self.change_coords(0, 10):
                    self.link_tile("Down", tileslist[i])
        if self.change_coords(0, -10) in coordinates:
            self.directions.append("Up")
            for i in range(len(coordinates)):
                if coordinates[i] == self.change_coords(0, -10):
                    self.link_tile("Up", tileslist[i])

        if len(self.directions) == 1:
            self.function = "gasse"
            self.canvas.delete(self.design)
            self.canvas.delete(self.pointdesign)
            return 1
        else:
            return 2
        
    def change_coords(self, z, a):
        tupel = self.get_coordinate()
        return [tupel[0]+z, tupel[1]+a]
    def return_function(self):
        return self.function
    def get_directions(self):
        return self.directions
    def switch(self, direction):
        return self.neighbor_tiles[direction]
    def get_coords(self):
        return self.coordinate
    def check_point(self):
        if self.point == True:
            self.canvas.delete(self.pointdesign)
            self.point = False
            return 1
        else:
            return 0
    def set_no_point(self):
        self.canvas.delete(self.pointdesign)
        self.point = False

    

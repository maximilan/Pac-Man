from pac_data import Enemy, Player, Tile, Path
from pac_settings import Setting
from tkinter import *
import tkinter as tk
from time import sleep
from random import randint
coordinates = list()
tiles = list()
coord_tiles = list()
oldtiles = list()
vorenemy = list()
newplayer = list()
playeryellowdesign = list()
pointlist = list()
lists = (coordinates, tiles, coord_tiles, oldtiles, vorenemy, newplayer, playeryellowdesign, pointlist)
global pac_man
global points
global leben
global current_setting
global old_setting
global minuspoint
global oldpoints
global level
global enemycounter
enemycounter = 0
level = 1
oldpoints = 0
minuspoint = 6
current_setting = 0
leben = 3
points = 0
pac_man = 0
enemy = list()
WIDTH = 1000
HEIGHT = 1000
game = True
###############Geistdesign#####################
multi = [3,4,5,11,12,13,14,15,19,20,21,22,23,24,25,28,31,34,37,40,43,46,47,48,49,50,51,52,55,56,57,58,59,60,61,64,65,66,67,68,69,70,73,74,75,76,77,78,79,82,83,84,85,86,87,88,91,93,95,97]
weiß = [29,30,32,33,38,41]
##############################################

def new_setting():
    global window
    global c
    global level
    global current_setting
    global enemycounter
    enemycounter = 0
    for i in range(len(lists)):
        del lists[i][:]
    c.delete("all")
    current_setting = Setting(c,level)
    setting(current_setting.return_setting())


    
def tile(x, y, z):
    global enemy
    global minuspoint
    y1 = y
    for i in range(4):
        if y1 == y+20:
            y1 += 10
        id0 = Path(c, x+20, y1)
        tupel = id0.get_coordinate()
        coordinates.append(tupel)
        tiles.append(id0)
        pointlist.append(id0)
        if z == "spawn":
            id0.set_no_point()
        y1+= 10
    x1 = x
    for i in range(5):
        id1 = Path(c, x1, y+20)
        if z == "spawn":
            id1.set_no_point()
        if x1 == x+20:
            if z == "spawn":
                vorenemy.append(x1)
                vorenemy.append(y+20)
                vorenemy.append(id1)  ##################Daten fürs Geisterfeld, die für jede Initialisierung eines Geistes benötigt werden
            elif z == "player":
                newplayer.append(x1)
                newplayer.append(y+20)
                newplayer.append(id1)  #######Daten für Spieler
                
        x1 += 10
        tupel = id1.get_coordinate()
        coordinates.append(tupel)
        tiles.append(id1)
        pointlist.append(id1)
    if z == "spawn":
        c.create_rectangle(x, y, x+50, y+50, fill = 'grey25')
def row(liste, y):
    global spawntile
    global WIDTH
    x = WIDTH/2-len(liste)*25
    for i in range(len(liste)):
        if liste[i] == 1:
            id1 = tile(x, y,"nospawn")
        elif liste[i] == 2:
            spawntile = tile(x, y, "spawn")
        elif liste[i] == 3:
            playertile = tile(x, y, "player")
        else:
            id1 = Tile(c, x, y)
        x += 50
def setting(liste):
    global HEIGHT
    y = HEIGHT/2-len(liste)*25
    for i in range(len(liste)):
        row(liste[i], y)
        y += 50

def makeenemy():
    global c
    tupel = []
    deltupel = []
    x = vorenemy[0]-20
    y = vorenemy[1]-20
    x1 = x
    y1 = y
    for i in range(0,12):
        x1 = x
        for q in range(0,9):
            id1 = c.create_rectangle(x1, y1, x1+40/9, y1+50/11, fill='white', outline = 'black')
            tupel.append(id1)
            deltupel.append(id1)
            x1 += 40/9
        y1 += 40/11
    rand = randint(1, 4)
    print(len(tupel))
    if rand == 1:
        color = "red"
    if rand == 2:
        color = "blue"
    if rand == 3:
        color = "green"
    if rand == 4:
        color = "purple"
    for i in range(len(multi)):
        c.itemconfig(tupel[multi[i]], fill=color, outline =color)
        deltupel.remove(tupel[multi[i]])
    for i in range(len(weiß)):
        c.itemconfig(tupel[weiß[i]], fill='white', outline ='white')
        deltupel.remove(tupel[weiß[i]])
    for i in range(len(tupel)-1, -1, -1):
        if tupel[i] in deltupel:
            c.delete(tupel[i])
            del tupel[i]
    id1 = c.create_rectangle(vorenemy[0], vorenemy[1], vorenemy[0]+10, vorenemy[1] +10, fill=color,outline = color)
    tupel.append(id1)
    id2 = Enemy(tupel, c, vorenemy[2])
    enemy.append(id2)


    


def player():
    global pac_man
    x = newplayer[0]-15
    y = newplayer[1]-15
    tupel = []
    id1 = c.create_oval(x, y, x+45, y+45, fill='yellow')
    tupel.append(id1)
    playeryellowdesign.append(id1)
    id2 = c.create_polygon(x+20, y+25, x+45, y+17, x+45, y+32, fill='black')
    id3 = c.create_oval(x+32, y+10, x+35, y+13, fill='black')
    tupel.append(id2)
    tupel.append(id3)
    
    pac_man = Player(tupel, c, newplayer[2])


def death():
    player = pac_man.return_yellow()
    for q in range(1,4):
        c.itemconfig(player, fill='black')
        window.update()
        sleep(0.5)
        c.itemconfig(player,fill = 'yellow')
        window.update()
        sleep(0.5)

def enemykillmove():
    global kill
    global leben
    global c
    global pac_man
    for i in range(len(enemy)-1, -1, -1):
            if randint(1, 5) > 1:
                enemy[i].move(pac_man)
            if enemy[i].check_kill(pac_man) == True:
                kill = True
    if kill == True:
        leben += -1
        death()
        for i in range(len(enemy)):
            enemy[i].delete()
        del enemy[:]
        kill = False
        
def new():
    ask.destroy()
def stop():
    global game
    game = False
    ask.destroy()
    
def textfunc():
    global points
    global level
    global leben
    c.itemconfig(leveltext, text=str(level))
    c.itemconfig(pointtext, text=str(points))
    c.itemconfig(lebentext, text = str(leben))
while True:
    enemycounter = 0
    level = 1
    oldpoints = 0
    minuspoint = 6
    current_setting = 0
    leben = 3
    points = 0
    pac_man = 0
    ###################Startbildschirm#######################################
    ask = tk.Tk()
    ask.title = 'Pac Man'
    c = Canvas(ask, height = 250, width = 600, bg = 'black')
    c.pack()
    c.create_oval(275, 30, 320, 75, fill = 'yellow')
    c.create_polygon(295, 55, 320, 47, 320, 62, fill='black')
    c.create_oval(307, 40, 310, 43, fill='black')
    B = tk.Button(ask, text="Neues Spiel", command = new)
    B.pack(side=LEFT)
    D = tk.Button(ask, text="Spiel beenden", command=stop)
    D.pack(side=RIGHT)
    c.create_text(325, 100, text='Pac Man', font=('Lato Black', 60), fill = 'white')
    c.create_text(325, 180, text='A production of HERFARTH Enterprises', font=('Lato Black', 10), fill='white')
    c.create_text(325, 220, text='All rights reserved', font = ('Lato Black', 10), fill='white')
    ask.update()
    ask.mainloop()
    ##########################################################################
    if game != True:
        break
    window = tk.Tk()
    window.title = 'Pac Man'
    c = Canvas(window, width = WIDTH+200, height = HEIGHT, bg='black')          ###################Initialisierung Fenster, Canvas, Tiles etc.
    c.pack()
    current_setting = Setting(c,level)
    setting(current_setting.return_setting())


    while level <= current_setting.return_maxlevel():
        minuspoint = 3
        leben = 3
        def movement(event): ####Bewegungsfunktion wird definiert
            pac_man.set_richtung(str(event.keysym))
        c.bind_all('<Key>', movement)
        window.update()
        c.create_text(WIDTH+30, 300, text='Level', fill='white', font = ('Bitstream Vera Sans', 30))
        leveltext = c.create_text(WIDTH+30, 350, text='', fill='white', font = ('Bitstream Vera Sans', 30))
        c.create_text(WIDTH+30, 500, text='Points', fill='white', font = ('Bitstream Vera Sans', 30))
        pointtext = c.create_text(WIDTH+30, 550, text='', fill='white', font = ('Bitstream Vera Sans', 30))
        c.create_text(WIDTH+30, 700, text='Life', fill='white', font = ('Bitstream Vera Sans', 30))
        lebentext = c.create_text(WIDTH+30, 750, text='', fill='white', font = ('Bitstream Vera Sans', 30))
        kill = False

        player() #######Player wird initialisiert

        for q in range(3):              #######Initialisierung der Tiles, Löschen der Sackgassen
            for i in range(len(tiles)-1, -1, -1):
                function = tiles[i].get_function(coordinates,tiles)
                if function == 1:
                    oldtiles.append(tiles[i])
                    minuspoint += 1
            for i in range(len(oldtiles)):
                coordinates.remove(oldtiles[i].get_coords())
                tiles.remove(oldtiles[i])
            del oldtiles[:]


        for i in range(len(enemy)-1, -1, -1):
            del enemy[i]
        makeenemy()    
        while points < len(pointlist)-minuspoint+oldpoints and leben > 0: ###########Spielschleife
            sleep(0.1)
            textfunc()
            enemykillmove()
            points += pac_man.move()
            print(current_setting.return_ghostnumber())
            if enemycounter == 150 and len(enemy) < current_setting.return_ghostnumber():
               makeenemy()
               enemycounter = 0
            else:
                enemycounter += 1
            window.update()##Ende

        if leben > 0 and level ==  current_setting.return_maxlevel():
            for i in range(4):
                c.configure(background ="white")
                sleep(0.9)
                window.update()
                c.configure(background = "black")
                sleep(0.9)
                window.update()
            break
        if leben > 0:
            for i in range(4):
                c.configure(background ="white")
                sleep(0.9)
                window.update()
                c.configure(background = "black")
                sleep(0.9)
                window.update()
            level += 1
            new_setting()
            oldpoints += points
        else:
            break

    if leben == 0:    
        c.create_text(500, 500, text='Game Over', font = ('Bitstream Vera Sans', 60), fill = 'white')
    else:
        c.create_text(500, 500, text='Sieg', font = ('Bitstream Vera Sans', 60), fill = 'white')
    window.update()
    sleep(3)
    window.destroy()

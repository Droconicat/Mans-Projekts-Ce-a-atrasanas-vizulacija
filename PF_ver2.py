from tkinter import PhotoImage
import tkinter as tk
from time import sleep
from math import sqrt

#   -   -   -   -   -   -   Rūtiņa klase

class Node:
    def __init__(self, button, x, y, Type):
        self.Button = button
        self.x = x
        self.y = y
        self.Type = Type
        self.Parent = 0
        self.Cost = 0

#   -   -   -   -   -   Logs
App_Window = tk.Tk()
App_Window.title("Ceļu Atrašanu / Path Finding")
App_Window.geometry("800x800")
App_Window.resizable(False, False)

#   -   -   -   -   -   Frames

TopFrame = tk.Frame(App_Window, bg = "grey50", width=800, height=100)
TopFrame.place(relx = 0, rely = 0, anchor = "nw")

GridFrame = tk.Frame(App_Window, bg = "white", width=800, height=700)
GridFrame.place(relx = 0, rely = 0.125, anchor = "nw")

#   -   -   -   -   -   Poga, opcijas, tekts, un rūtiņa bilde

Button_SPF = tk.Button(TopFrame, text = "Meklēt!", bg = "orange", fg="white", width=6, height=2, relief=tk.RAISED, font=("Arial", 20, "bold"))
Button_SPF.place(in_ = TopFrame, rely = 0.5 ,anchor = "w")

Opcijas = tk.Listbox(TopFrame, width=20, height=2, font = "Helvetica")
Opcijas.place(in_ = TopFrame, relx = 0.48, rely = 0.5 ,anchor = "ne")
Opcijas.insert(1, "A*")
Opcijas.insert(2, "Dijkstras")
Opcijas.insert(3, "Greedy Best First Search")

Algo_Text = tk.Label(TopFrame, text = "Izvēlētā algoritms:", bg="grey50", fg="white", width=25, height=2)
Algo_Text.place(in_ = TopFrame, relx = 0.48, rely = 0.5 ,anchor = "se")

InfoText = tk.Label(TopFrame, width=50, height=6, relief="ridge", font=("Arial", 9), 
text = """* Zaļš ir sākum punkts. Sarkans ir gala punkts.
* Melns ir bloķēts
Nospied uz rūtiņu lai nomainītu to uz bloķētu vai
nebloķētu. Nospied uz krāsaino rūtiņu un tad uz
citu rūtiņu lai nomainītu vietā!
""")
InfoText.place(in_ = TopFrame, relx = 1, rely = 0.5 ,anchor = "e")

#Img = PhotoImage(fie="")

#Grid_Deco = tk.Label(GridFrame)
#Grid_Deco.pack()


#   -   -   -   -   -   -   -   -   VĒRTĪBAS

Grid = []
Working = False
Sel_Alg = 0
MSG_node = 0
color = ["white","black","green", "red"]
Start = 0
Goal = 0

#   -   -   -   -   -   -   -   -   ALGORITMI

def Get_Least_Cost(Open):
    
    Max = 99999
    Temp = []

    for i in range(len(Open)):
        node = Open[i]
        if node.Cost < Max:
            Max = node.Cost
            Temp.append(node)

    return Temp[len(Temp)-1]

def Dist(node1, node2):
    return sqrt(((node2.x-node1.x)**2) + ((node2.y-node1.y)**2))

def Get_Neighbors(node):
    neighbors = []
    
    for X in range(-1, 2):
        for Y in range(-1, 2):
            if abs(X)+abs(Y) == 0 or node.x+X < 0 or node.y+Y < 0 or len(Grid)-1 < node.x+X or len(Grid[0])-1 < node.y+Y:
                continue
            
            NODE = Grid[node.x+X][node.y+Y]
            
            neighbors.append(NODE)
            
    return neighbors


def Greedy_Best_First_Search():
    global Grid
    global Start
    global Goal
    global sleep
    
    Finished_Path = []
    Closed = []
    Open = []
    Current_Node = Start
    Open.append(Current_Node)
            
    while len(Open) != 0:
        Open.remove(Current_Node)
        Current_Node.Cost = Dist(Current_Node, Goal)
        Closed.append(Current_Node)
        
        Current_Node.Button.configure(bg="blue")
        
        if Current_Node == Goal:
            return Closed
        
        Neighbors = Get_Neighbors(Current_Node)
        
        for node in Neighbors:
            if node in Closed or node.Type == 1:
                continue
            
            node.Cost = Dist(node, Goal)
            node.Parent = Current_Node
            
            if not node in Open:
                
                node.Button.configure(bg="cyan")
                Open.append(node)
            
        Current_Node = Get_Least_Cost(Open)
        sleep(0.1)
    return []

#   -   -   -   -   -   Normālās funkcijas

def Get_Sel_Algorithm():
    try:
        A = Opcijas.curselection()[0]
    except:
        return -1
    else:
        return Opcijas.curselection()[0]
    

def Grid_Button_Pressed(x, y):
    global Working
    global Grid
    global MSG_node
    global Start
    global Goal
    
    if Working:
        return 0
    
    node = Grid[x][y]
    
    if MSG_node != 0:
        TYPE = node.Type
        
        node.Type = MSG_node.Type
        MSG_node.Type = TYPE
        
        node.Button.configure(bg = color[node.Type])
        if node.Type == 2:
            Start = node
        elif node.Type == 3:
            Goal = node
        
        MSG_node.Button.configure(bg = color[MSG_node.Type])
        
        MSG_node = 0
        return 0
    
    if node.Type == 0:
        node.Type = 1
        node.Button.configure(bg="black")
    elif node.Type == 1:   
        node.Type = 0
        node.Button.configure(bg="white")
    elif node.Type == 2 or node.Type == 3:
        MSG_node = node
    
    
def Start_Button_Pressed():    
    global Working
    
    if not Working:
        Working = True
        Path = Greedy_Best_First_Search()
        sleep(0.5)
        
        
    
    #else:
        
        
    
#   -   -   -   Config    
    
Button_SPF.configure(command = lambda: Start_Button_Pressed())    

    
#   -   -   -   -   -   -   -   -   -   -   -   Rūtiņa
#   - Rāmja izmērs ir x=800 un y=700 
#   - Šis bus dalīts ar 25
#   -  Type: 0 = empty , 1 = blocked , 2 = Start , 3 = Goal

for X in range(0, 32):
    Grid.append([])
    for Y in range(0, 28):
        New_Button = tk.Button(GridFrame, text="", width=1, height=1
        , bg="white", command = lambda arg1=X, arg2=Y: Grid_Button_Pressed(arg1, arg2))
        New_Button.place(in_ = GridFrame, relx = (1/800)*25*X, rely = (1/700)*25*Y,anchor = "nw")
        TYPE = 0
        if X == 31 and Y == 0:
            TYPE = 3
            New_Button.configure(bg = "red")
        elif X == 0 and Y == 27:
            TYPE = 2
            New_Button.configure(bg = "green")
        
        Grid[X].append(Node(New_Button, X, Y, TYPE))
        
        if TYPE == 2:
            Start = Grid[X][Y]
        if  TYPE == 3:
            Goal = Grid[X][Y]
            
#   -   -   -   -   -   MainLoop

App_Window.mainloop()
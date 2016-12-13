from tkinter import *


class myAwesomeClass():
    def __init__(self, master):
        v = IntVar()
        v.set(3)

        leftFrame = Frame(master)
        leftFrame.pack(side=LEFT)

        rightFrame = Frame(master)
        rightFrame.pack(side=RIGHT)

        lUpFrame = Frame(leftFrame)
        lUpFrame.pack(side=TOP)

        lDownFrame = Frame(leftFrame)
        lDownFrame.pack(side=BOTTOM)

        rUpFrame = Frame(rightFrame)
        rUpFrame.pack(side=TOP)

        rDownFrame = Frame(rightFrame)
        rDownFrame.pack(side=BOTTOM)

        self.printButton = Button(lUpFrame, text="Save", command=self.printMessage)
        self.printButton.pack(side=LEFT)

        self.quitButton = Button(lDownFrame, text="QUIT", command=lDownFrame.quit)
        self.quitButton.pack(side=BOTTOM)

        #The right top image
        self.photoT = PhotoImage(file="resources/chimera.png")
        
        self.canvasU= Canvas(rUpFrame, bg="white", width=610, height=152)
        
        self.canvasU.grid(row = 0, column = 0)
        self.canvasU.create_image(306,77, image=self.photoT)
        
        self.canvasU.bind("<Key>", self.key)
        self.canvasU.bind("<Button-1>", self.callback)
        self.canvasU.pack()

        #The right down image
        self.photoD = PhotoImage(file="resources/aRing.png")
        self.photoEx = PhotoImage(file="resources/randDraw.png")
        
        self.canvasD = Canvas(rDownFrame, bg="white", width=409, height=369)
        
        self.canvasD.grid(row = 0, column = 0)
        self.canvasD.create_image(204,185, image=self.photoD)

        self.canvasD.create_image(204,185, image=self.photoEx)
        # self.canvas.delete(self.photoD)
        self.canvasD.delete(self.photoEx)

        # self.canvasD.delete("all")
        self.coord = 10, 50, 240, 210
        self.arc = self.canvasD.create_arc(self.coord, start=0, extent=150, fill="blue", stipple="gray12")

        #polygon
        self.poly = self.canvasD.create_polygon(10, 50, 15, 35, 80, 120, 100, 234)

        self.canvasD.delete(self.poly)

        self.canvasD.create_rectangle(20, 50, 300, 100, outline="black", fill="red", width=2, stipple="gray50")

        self.canvasD.bind("<Key>", self.key)
        self.canvasD.bind("<Button-1>", self.callback)
        self.canvasD.pack()

        # self.canvasD.delete(self.arc)

    def callback(self, event):
        print("clicked at", event.x, event.y)

    def key(self, event):
        print("pressed", repr(event.char))

    def printMessage(self):
        print("Saving to the xml configuration file")
    


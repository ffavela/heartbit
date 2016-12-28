from tkinter import *
from shapely.geometry import Polygon,MultiPoint,Point
import random
from math import pi,sin,cos

class myAwesomeClass():
    def __init__(self, master):

        master.wm_title("Heartbit")
        self.sideList=[16,24,32,40,40,48,48,48,48]
        self.myRandInt=0
        self.myPoint=(0,0)

        self.poly4DrawList=[]
        self.polyDrawnL=[]
        self.explodedPoints=[]
        self.shapelyPolyList=[]
        self.W=411
        self.H=371
        self.center=[int(self.W/2),int(self.H/2)]
        self.BigR=int(min(self.W,self.H)/2)

        # master.iconbitmap(r"heart.png")

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
        # self.photoD = PhotoImage(file="resources/aRing.png")
        # self.photoEx = PhotoImage(file="resources/randDraw.png")
        
        self.canvasD = Canvas(rDownFrame, bg="white", width=self.W, height=self.H)

        # self.canvasD.bind("<Enter>", partial(color_config, text, "red"))
        
        self.canvasD.grid(row = 0, column = 0)
        # self.canvasD.create_image(204,185, image=self.photoD)

        # self.canvasD.create_image(204,185, image=self.photoEx)
        # self.canvas.delete(self.photoD)
        # self.canvasD.delete(self.photoEx)

        # self.canvasD.delete("all")
        # self.coord = 10, 50, 240, 210
        # self.arc = self.canvasD.create_arc(self.coord, start=0, extent=150, fill="blue", stipple="gray12")

        #polygon
        # self.poly = self.canvasD.create_polygon(10, 50, 15, 35, 80, 120, 100, 234)


        # self.polyPoints=[(338,167),(405,160),(383,276),(321,246)]
        # self.convexPolyPoints=list(MultiPoint(self.polyPoints).convex_hull.exterior.coords)
        # self.shapelyPoly=Polygon(self.convexPolyPoints)

        # self.pointStuff=[338,167,405,160,383,276,321,246]
        #exploding the list
        # self.pointStuff=[item for t in self.polyPoints for item in t]

        # self.poly = self.canvasD.create_polygon(self.pointStuff,fill="green",stipple="gray50")

        #The new functions
        self.initRing()

        # self.canvasD.delete(self.poly)

        # self.canvasD.create_rectangle(20, 50, 300, 100, outline="black", fill="red", width=2, stipple="gray50")

        self.canvasD.bind("<Key>", self.key)
        self.canvasD.bind("<Button-1>", self.callbackD)
        self.canvasD.pack()

        # self.canvasD.delete(self.arc)

    def callbackD(self, event):
        print("Lower canvas")
        print("clicked at", event.x, event.y)
        self.myPoint=Point(event.x, event.y)
        # if self.shapelyPoly.contains(self.myPoint):
        #     print("Point inside the polygon!!")
        self.checkEventInPolyList(event.x, event.y)
        self.genRandInt()
        # print("getPolySides(%d) = %d" % (self.myRandInt, self.getPolySides(self.myRandInt)))


    def callback(self, event):
        print("Upper canvas")
        print("clicked at", event.x, event.y)
        self.genRandInt()
        self.canvasD.delete("all")
        self.initRing()
        # print("getPolySides(%d) = %d" % (self.myRandInt, self.getPolySides(self.myRandInt)))

    def key(self, event):
        print("pressed", repr(event.char))

    def printMessage(self):
        print("Saving to the xml configuration file")

    def getPolySides(self,ringNum):
        print("ringNum = %d" % ringNum )
        if ringNum >= 1 and ringNum <= len(self.sideList) and isinstance(ringNum, int):
            return self.sideList[ringNum-1]
        return 0

    def genRandInt(self):
        self.myRandInt=random.randint(1,12)

    def createVertex4Poly(self,R,dR,N):
        ang=-pi/2
        dAng=2*pi/N
        # dR*=-1 #Making it negative
        localVertexList=[]
        for i in range(N):
            vPoints=[[],[],[],[]]
            vPoints[0]=[R*cos(ang),R*sin(ang)]
            vPoints[1]=[(R+dR)*cos(ang),(R+dR)*sin(ang)]
            vPoints[2]=[(R+dR)*cos(ang+dAng),(R+dR)*sin(ang+dAng)]
            vPoints[3]=[R*cos(ang+dAng),R*sin(ang+dAng)]
            ang+=dAng

            localVertexList.append(vPoints)
        return localVertexList

    def reCenterPolyCoords(self,vList):
        newList=[]
        for e in vList:
            newE=[[p[0]+self.center[0], p[1]+self.center[1]] for p in e]
            newList.append(newE)

        return newList

    def makePolyDrawList(self,vList):
        #the vertex list has to be already created and recentered
        self.poly4DrawList=[]
        for e in vList:
            self.explodedPoints=[item for t in e for item in t]
            self.poly4DrawList.append(self.explodedPoints)

    def makeShapelyPolyList(self,myVList):
        self.shapelyPolyList=[]
        for poly in myVList:
            convexPolyPoints=list(MultiPoint(poly).convex_hull.exterior.coords)
            shapelyPolygon=Polygon(convexPolyPoints)
            self.shapelyPolyList.append(shapelyPolygon)

    def drawPolygons(self):
        for poly in self.poly4DrawList:
            self.polyDrawnL.append(self.canvasD.create_polygon(poly,fill="blue",stipple="gray50", outline="#f12", width=2))

    def initRing(self):
        print("Inside initRing")
        # self.createVertex4Poly()
        # vLVList=self.createVertex4Poly()
        vLVList=self.createMultiRings(2)
        # vLVList=self.createVertex4Poly(135,50,random.randint(3,48))

        myVList=self.reCenterPolyCoords(vLVList[0])
        self.makePolyDrawList(myVList)
        self.makeShapelyPolyList(myVList)
        self.drawPolygons()



    def checkEventInPolyList(self,xVal,yVal):
        self.myPoint=Point(xVal, yVal)
        for poly in self.shapelyPolyList:
            if poly.contains(self.myPoint):
                print("Point inside poly list!!")
                theIndex=self.shapelyPolyList.index(poly)
                print("The index is %d" % theIndex)
                break

    def createMultiRings(self,rN):
        multiRingList=[[] for e in range(rN)]
        R=self.BigR
        dR=-50
        N=random.randint(3,48)

        for i in range(rN):
            multiRingList[i]=self.createVertex4Poly(R,dR,N)
            R+=dR

        return multiRingList

    # def color_config(self, widget, color, event):
    #     widget.configure(foreground=color)


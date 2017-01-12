from tkinter import *
from shapely.geometry import Polygon,MultiPoint,Point
import random
from math import pi,sin,cos

class myAwesomeClass():
    def __init__(self, master):

        master.wm_title("Heartbit")
        self.sideList=[16,24,32,40,40,48,48,48,48,60,60]
        self.listIndex=0
        self.myRandInt=0
        self.myPoint=(0,0)

        self.W=800
        self.H=750
        self.center=[int(self.W/2),int(self.H/2)]
        self.BigR=int(min(self.W,self.H)/2)

        self.UW=610
        self.UH=152

        self.vList=[]
        self.myVList=[]
        self.shapelyPolyList=[]
        self.poly4DrawList=[]
        self.polyDrawnL=[]
        self.shapelyPolyList=[]
        self.masterList=[]
        self.onOffList=[]

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

        self.canvasU= Canvas(rUpFrame, bg="white", width=self.UW, height=self.UH)

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

        self.masterList=self.fillAllRings()
        #The new functions
        self.initRing(0)

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
        indexList=self.checkEventInPolyList(event.x, event.y)
        print("Index list is: ",indexList)
        print("b4 if len(self.poly4DrawList)",len(self.poly4DrawList))
        if indexList != []:
            self.redrawRing(indexList)
        # self.genRandInt()
        # print("getPolySides(%d) = %d" % (self.myRandInt, self.getPolySides(self.myRandInt)))


    def callback(self, event):
        print("Upper canvas")
        x=event.x
        y=event.y
        print("clicked at", x, y)
        region=self.ringRegion(x,y)
        self.listIndex=region
        print("region = ", region)

        # self.genRandInt()
        self.initRing(region)
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

    # def genRandInt(self):
    #     self.myRandInt=random.randint(1,12)

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
        newList=[[] for e in vList]
        for i in range(len(vList)):
            for e in vList[i]:
                newE=[[p[0]+self.center[0], p[1]+self.center[1]] for p in e]
                newList[i].append(newE)

        return newList

    def getOnOffList(self,aList):
        onOffList=[[True for e in t] for t in aList]
        return onOffList

    def makePolyDrawList(self,vList):
        #the vertex list has to be already created and recentered
        p4DList=[[] for e in vList]
        for i in range(len(vList)):
            for e in vList[i]:
                expPoints=[item for t in e for item in t]
                p4DList[i].append(expPoints)

        return p4DList

    def ringRegion(self,x,y):
        divNum=11
        deltaPos=self.UW/divNum
        for i in range(divNum+1):
            if x < i*deltaPos:
                return 10-(i-1)


    def makeShapelyPolyList(self,myVList):
        myShapelyPolyList=[[] for e in myVList]
        for i in range(len(myVList)):
            for poly in myVList[i]:
                convexPolyPoints=list(MultiPoint(poly).convex_hull.exterior.coords)
                shapelyPolygon=Polygon(convexPolyPoints)
                myShapelyPolyList[i].append(shapelyPolygon)
        return myShapelyPolyList

    def drawPolygons(self, poly4DrawList, indexStuff=[]):
        def getColor(i,polyIndex,indexStuff=[]):
            color="green"
            if i%2 == 0:
                color="blue"
            # print(i,polyIndex)
            if self.onOffList != [] and self.onOffList[i][polyIndex] == False:
                color="red"

            if indexStuff != []:
                if indexStuff[0] == i and polyIndex == indexStuff[1]:
                    if self.onOffList[i][polyIndex] == True:
                        self.onOffList[i][polyIndex] = False
                        color="red"
                    else:
                        self.onOffList[i][polyIndex] = True
                        color="green"
                        if i%2 == 0:
                            color="blue"
            return color

        polyDrawnL=[[] for e in poly4DrawList]
        print("len(poly4DrawList) = ", len(poly4DrawList))

        for i in range(len(poly4DrawList)):
            for poly in poly4DrawList[i]:
                polyIndex=poly4DrawList[i].index(poly)
                color=getColor(i,polyIndex,indexStuff)

                polyDrawnL[i].append(self.canvasD.create_polygon(poly,fill=color,stipple="gray50", outline="#f12", width=2))

        print("onOffList")
        print(self.onOffList)

        return polyDrawnL

    def fillAllRings(self):
        sideList=self.sideList
        masterList=[[] for t in sideList]
        for e,i in zip(sideList,range(len(sideList))):
            self.listIndex=i#This is for the createMultiRings part
            vLVList=self.createMultiRings(2)
            myVList=self.reCenterPolyCoords(vLVList)
            shapelyPolyList=self.makeShapelyPolyList(myVList)
            poly4DrawList=self.makePolyDrawList(myVList)
            onOffList=self.getOnOffList(myVList)

            #populating the masterList with the polygon data
            masterList[i].append(myVList)#Centered polygon list
            masterList[i].append(shapelyPolyList)#Shapely polygons
            masterList[i].append(poly4DrawList)#Polygons 4 drawing
            masterList[i].append(onOffList)#Detector status

            print("len(onOffList)",len(onOffList))

        return masterList

    def initRing(self,ringNum=0):
        print("Inside initRing")
        self.canvasD.delete("all")

        self.myVList=self.masterList[ringNum][0]
        self.shapelyPolyList=self.masterList[ringNum][1]

        self.poly4DrawList=self.masterList[ringNum][2]

        self.onOffList=self.masterList[ringNum][3]
        print("initRing, self.onOffList = ",self.onOffList)

        self.polyDrawnL=self.drawPolygons(self.poly4DrawList)


    def redrawRing(self, indexList):
        self.canvasD.delete("all")
        self.polyDrawnL=self.drawPolygons(self.poly4DrawList, indexList)

    def checkEventInPolyList(self,xVal,yVal):
        #Add an argument to shapelyPolyList and adapt it
        self.myPoint=Point(xVal, yVal)
        # for poly in self.shapelyPolyList:
        for ring in self.shapelyPolyList:
            for poly in ring:
                if poly.contains(self.myPoint):
                    print("Point inside poly list!!")
                    theRIndex=self.shapelyPolyList.index(ring)
                    print("The ring index is %d" % theRIndex)

                    theIndex=self.shapelyPolyList[theRIndex].index(poly)
                    print("The index is %d" % theIndex)
                    return [theRIndex, theIndex]
        return []

    def createMultiRings(self,rN):
        multiRingList=[[] for e in range(rN)]
        R=self.BigR
        dR=-50
        # N=random.randint(3,48)
        N=self.sideList[self.listIndex]

        for i in range(rN):
            multiRingList[i]=self.createVertex4Poly(R,dR,N)
            R+=dR

        return multiRingList

    # def color_config(self, widget, color, event):
    #     widget.configure(foreground=color)

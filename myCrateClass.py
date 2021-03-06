import sys
#Checking python version (either 2 or 3)
if sys.version_info[0] == 2:
    from Tkinter import *
    import tkFont as font
else:#python 3 case
    from tkinter import *
    import tkinter.font as font

from shapely.geometry import Polygon,MultiPoint,Point
import random
from math import pi,sin,cos

from xmlParser import *

class myCrateClass():
    def __init__(self, master):

        master.wm_title("Heartbit CRATE")
        # self.debugVar=False
        # self.boolEnum=True
        # self.sideList=[16,24,32,40,40,48,48,48,48,32,32]
        # self.secList=[79,158,219,271,322,376,426,480,533,580,611]
        # self.listIndex=0
        # self.myRandInt=0
        # self.myPoint=(0,0)
        self.coboW=50
        self.coboH=173
        self.shift=[15,85]

        self.asadConW=5
        self.asadConH=48

        self.shapelyCoboPolyD={}


        myAsadCoordsList=self.getAsadCon(5,2)

        print(myAsadCoordsList)

        self.myAsadConShapelyPoly=self.getShapelyPolyFromList(myAsadCoordsList)

        self.W=900
        self.H=750
        self.center=[int(self.W/2),int(self.H/2)]
        self.BigR=int(min(self.W,self.H)/2)

        self.UW=780
        self.UH=323

        # self.vList=[]
        # self.myVList=[]
        # self.shapelyPolyList=[]
        # self.poly4DrawList=[]
        # self.polyDrawnL=[]
        # # self.shapelyPolyList=[] #Twice?!
        # self.masterList=[]
        # self.onOffList=[]

        # self.dIntList=[]
        # self.pidList=[]
        # # master.iconbitmap(r"heart.png")

        # # self.doc=getXmlDoc('configure-cobomutant.xcfg')
        # self.doc=getXmlDoc('resources/modifiedXml2.xml')

        # self.var=self.doc['Setup']['@id'] # == u'Conditions'

        # self.dummyVar=""

        # v = IntVar()
        # v.set(3)
        # self.coboPoly=self.createShapelyCoboPoly()

        self.cobosIDXs=[0,1,2,3,4,5,6,7,10,11]
        self.shapelyCoboPolyD=self.getShapelyCoboPolyD()
        self.asadsConDCoords=self.getAsadsConDCoords()

        self.asadsPolyListDForAllCobos=\
        self.getAsadsPolyListDForAllCobos(self.asadsConDCoords)

        leftFrame = Frame(master)
        leftFrame.pack(side=LEFT)

        rightFrame = Frame(master)
        rightFrame.pack(side=RIGHT)

        lUpFrame = Frame(leftFrame)
        lUpFrame.pack(side=TOP)

        lUptFrame = Frame(lUpFrame)
        lUptFrame.pack(side=TOP)

        lUplFrame = Frame(lUpFrame)
        lUplFrame.pack(side=LEFT)

        lUprFrame = Frame(lUpFrame)
        lUprFrame.pack(side=RIGHT)

        lDownFrame = Frame(leftFrame)
        lDownFrame.pack(side=BOTTOM)

        rUpFrame = Frame(rightFrame)
        rUpFrame.pack(side=TOP)

        rDownFrame = Frame(rightFrame)
        rDownFrame.pack(side=BOTTOM)

        rDownLFrame = Frame(rDownFrame)
        rDownLFrame.pack(side=LEFT)

        rDownRFrame = Frame(rDownFrame)
        rDownRFrame.pack(side=RIGHT)

        # self.printButton = Button(lUpFrame, text="Save", command=self.printMessage)
        # self.printButton.pack(side=LEFT)

        optHeaders=Label(lUptFrame,text='Options Menu', anchor="n", width=12)
        optHeaders.pack(side=TOP)

        ################Options part BEGIN
        #################################################

        # font.nametofont('TkDefaultFont').configure(size=5)
        # MyFont = font.Font(weight='bold')
        optSel=Label(lUplFrame,text='select', anchor="n", width=12)
        optSel.pack(side=LEFT)

        optionList = ('zero', 'one', 'two','three')
        self.v = StringVar()
        self.v.set(optionList[0])
        self.om = OptionMenu(lUprFrame, self.v, *optionList)
        # self.om.config( height = 3, width = 1 )
        # self.om.config(width=1)
        self.om.pack(side=BOTTOM)


        ################Options part END #################################

        self.quitButton = Button(lDownFrame, text="QUIT", command=lDownFrame.quit, height = 3, width=3)
        # self.quitButton.config(width=1)
        self.quitButton.pack(side=BOTTOM)

        # #The top image
        self.photoC = PhotoImage(file="resources/crate.png")

        self.canvasU= Canvas(rUpFrame, bg="white", width=self.UW, height=self.UH)

        self.canvasU.grid(row = 0, column = 0)
        self.canvasU.create_image(360,170, image=self.photoC)

        self.canvas_id= self.canvasU.create_text(200,10,anchor="nw")


        self.canvasU.itemconfig(self.canvas_id,text="Crate and COBOs")

        self.drawnPol=self.drawPolygons([[myAsadCoordsList]])


        # #The left down image left
        self.photoA = PhotoImage(file="resources/asad.png")

        self.canvasDL= Canvas(rDownLFrame, bg="white", width=35, height=320)

        self.canvasDL.grid(row = 0, column = 0)
        self.canvasDL.create_image(18,160, image=self.photoA)

        self.canvas_id= self.canvasDL.create_text(2,5,anchor="nw")
        self.canvasDL.itemconfig(self.canvas_id,text="ASAD")

        # #The left down image right
        self.photoAGET = PhotoImage(file="resources/aget.png")

        self.canvasDR= Canvas(rDownRFrame, bg="white", width=750, height=320)

        self.canvasDR.grid(row = 0, column = 0)
        self.canvasDR.create_image(380,160, image=self.photoAGET)

        self.canvas_id= self.canvasDR.create_text(20,16,anchor="nw")
        self.canvasDR.itemconfig(self.canvas_id,text="AGET")

        # # canvas_id = canvas.create_text(10, 10, anchor="nw")

        self.canvasU.bind("<Key>", self.key)
        self.canvasU.bind("<Button-1>", self.callbackCRATE)
        self.canvasU.pack()


        self.canvasDL.bind("<Key>", self.key)
        self.canvasDL.bind("<Button-1>", self.callbackASAD)
        self.canvasDL.pack()

        self.canvasDR.bind("<Key>", self.key)
        self.canvasDR.bind("<Button-1>", self.callbackAGET)
        self.canvasDR.pack()

        # self.canvasD = Canvas(rDownFrame, bg="white", width=self.W, height=self.H)

        # self.canvasD.grid(row = 0, column = 0)

        # self.masterList=self.fillAllRings()

        # self.masterList=self.fillAllCOBOPolys()
        # #The new functions
        # self.initRing(0)

        # self.dIntList=self.detect2Num(self.masterList)
        # self.pidList=self.detect2Pid(self.masterList)
        # # self.printRtest(self.dIntList,self.pidList)

        # self.readXmlState()
        # #Redrawing zone 1 so it gets the xml state
        # self.drawZone1()

        # self.dummyVar=getOptVal(self.doc,1,3,1,5, "isActive")

        # self.canvasD.bind("<Key>", self.key)
        # self.canvasD.bind("<Button-1>", self.callbackD)
        # self.canvasD.pack()

        # # self.canvasD.delete(self.arc)

        drawnTestPolygonCobosD=self.getDrawnShapelyPolygonD(self.shapelyCoboPolyD)
        print("drawnTestPolygonCobosD[2] = ",drawnTestPolygonCobosD[2])
        self.canvasU.itemconfig(drawnTestPolygonCobosD[2],fill="red")

        myDrawnPolyInDWithLists=self.getDrawnShapelyPolygonDOfL(self.asadsPolyListDForAllCobos)

    def callbackD(self, event):
        self.myPoint=Point(event.x, event.y)
        indexList=self.checkEventInPolyList(event.x, event.y)
        if indexList != []:
            print("zoneIndex = ", self.listIndex)
            print("indexList = ", indexList)
            localOnOffL=self.masterList[self.listIndex][3]
            onOffVal=localOnOffL[indexList[0]][indexList[1]]
            print("ondOffVal = ", onOffVal)
            self.redrawRing(indexList)
            self.writeRegionInfo(self.listIndex)
            self.writeDetectInfo(self.listIndex,indexList)

    def callbackCRATE(self, event):
        print("CRATE canvas")
        x=event.x
        y=event.y
        myPoint=Point(x,y)
        # coboPoly=self.coboPoly

        myAsadConShapelyPoly=self.myAsadConShapelyPoly
        shapelyCoboPolyD=self.shapelyCoboPolyD

        for coboKey in shapelyCoboPolyD:
            shapelyCoboPoly=shapelyCoboPolyD[coboKey]
            if shapelyCoboPoly.contains(myPoint):
                print("Inside the COBO {}!!".format(coboKey))
                # Fetching the corresponding list for the asadsD

                asadsConPolyL=self.asadsPolyListDForAllCobos[coboKey]
                for asadsConL in asadsConPolyL:
                    # print(asadsConL)
                    if asadsConL.contains(myPoint):
                        print("###############################")
                        print("Inside the asad polygon!!!")
                        print("###############################")

                break

        print(x,y)

    def callbackASAD(self, event):
        x=event.x
        y=event.y
        print("ASAD canvas")
        print(x,y)

    def callbackAGET(self, event):
        x=event.x
        y=event.y
        print("AGET canvas")
        print(x,y)


    def callback(self, event):
        x=event.x
        y=event.y
        region=self.ringRegion(x,y)
        self.listIndex=region
        self.initRing(self.listIndex)

    def key(self, event):
        print("pressed", repr(event.char))

    def printMessage(self):
        print("Saving to the xml configuration file")
        print("printing the write2Dict test")
        self.write2Dict()

        #Unparsing the dictionary
        print("\nunparsing the dictionary into an xml string\n")
        myXmlString=xmltodict.unparse(self.doc, pretty=True)
        # print(myXmlString)

        #Writing to file
        outFileName="resources/modifiedXml2.xml"
        print("\nWriting to %s \n" % outFileName)

        with open(outFileName, "w") as text_file:
            text_file.write(myXmlString)


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
        secList=self.secList
        for e,i in zip(secList,range(len(secList))):
            if x < e:
                return 9-(i-1)
        return 0 #If all fails send the tiny ring

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
        # print("len(poly4DrawList) = ", len(poly4DrawList))

        for i in range(len(poly4DrawList)):
            for poly in poly4DrawList[i]:
                polyIndex=poly4DrawList[i].index(poly)
                color="green"
                # color=getColor(i,polyIndex,indexStuff)
                myPol=self.canvasU.create_polygon(poly,\
                                                  fill=color,\
                                                  stipple="gray50",\
                                                  outline="#f12",\
                                                  width=2)
                polyDrawnL[i].append(myPol)

        # Print("onOffList")
        # print(self.onOffList)

        return polyDrawnL

    def getDrawnShapelyPolygon(self, myShapelyPolygon,color="cyan"):
        polyCoords=self.getCoordsFromShapelyPoly(myShapelyPolygon)
        # color="#000080"
        myPol=self.canvasU.create_polygon(polyCoords,\
                                          fill=color,\
                                          stipple="gray50",\
                                          outline="#f12",\
                                          width=2)
        return myPol

    #For the simple boxes of the COBOs, for example
    def getDrawnShapelyPolygonD(self, myShapelyPolygonD):
        drawnTestPolygonD={}
        for e in myShapelyPolygonD:
            myPol=self.getDrawnShapelyPolygon(myShapelyPolygonD[e])
            drawnTestPolygonD[e]=myPol

        return drawnTestPolygonD

    #For the asad list part, for example
    def getDrawnShapelyPolygonL(self, myShapelyPolygonL):
        drawnTestPolygonL=[]
        for e in myShapelyPolygonL:
            myVar=e
            polyCoords=self.getCoordsFromShapelyPoly(myVar)
            color="green"
            myPol=self.canvasU.create_polygon(polyCoords,\
                                              fill=color,\
                                              stipple="gray50",\
                                              outline="#f12",\
                                              width=2)
            drawnTestPolygonL.append(myPol)

        return drawnTestPolygonL


    #For the asad dictionary with lists part, for example
    def getDrawnShapelyPolygonDOfL(self,myShapelyPolygonDOfL):
        drawnTestPolygonDOfL={}
        for coboKey in myShapelyPolygonDOfL:
            myShapelyPolygonL=myShapelyPolygonDOfL[coboKey]
            myDrawnTestPolygonL=self.getDrawnShapelyPolygonL(myShapelyPolygonL)
            drawnTestPolygonDOfL[coboKey]=myDrawnTestPolygonL

        return drawnTestPolygonDOfL

    def fillAllRings(self):
        sideList=self.sideList
        masterList=[[] for t in sideList]
        for e,i in zip(sideList,range(len(sideList))):
            self.listIndex=i#This is for the createMultiRings part
            if self.listIndex == 9:
                vLVList=self.createMultiRings(8)
            elif self.listIndex == 10:
                vLVList=self.createMultiRings(9)
            else:
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

            # print("len(onOffList)",len(onOffList))

        return masterList

    def fillAllCOBOPolys(self):
        masterList=[None]
        # myVList=self.reCenterPolyCoords(vLVList)
        myVList=self.createPolySets()
        shapelyPolyList=self.makeShapelyPolyList(myVList)
        poly4DrawList=self.makePolyDrawList(myVList)
        onOffList=self.getOnOffList(myVList)

        #populating the masterList with the polygon data
        masterList[0].append(myVList)#Centered polygon list
        masterList[0].append(shapelyPolyList)#Shapely polygons
        masterList[0].append(poly4DrawList)#Polygons 4 drawing
        masterList[0].append(onOffList)#Detector status

        return masterList

    def initRing(self,ringNum=0):
        self.canvasD.delete("all")

        self.myVList=self.masterList[ringNum][0]
        self.shapelyPolyList=self.masterList[ringNum][1]

        self.poly4DrawList=self.masterList[ringNum][2]

        self.onOffList=self.masterList[ringNum][3]
        # if ringNum == 0:
            # print("firstVal", self.onOffList[0][0])

        # print("initRing, self.onOffList = ",self.onOffList)

        self.polyDrawnL=self.drawPolygons(self.poly4DrawList)

        self.writeRegionInfo(ringNum)
        if self.boolEnum:
            self.writeEnum(self.shapelyPolyList)


    def redrawRing(self, indexList):
        self.canvasD.delete("all")
        self.polyDrawnL=self.drawPolygons(self.poly4DrawList, indexList)
        if self.boolEnum:
            self.writeEnum(self.shapelyPolyList)

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
        if rN > 5:
            dR=-35
        # N=random.randint(3,48)
        N=self.sideList[self.listIndex]
        if self.listIndex == 10:
            rN-=2

        for i in range(rN):
            multiRingList[i]=self.createVertex4Poly(R,dR,N)
            R+=dR

        if self.listIndex == 10:
            N=16
            multiRingList[rN]=self.createVertex4Poly(R,dR,N)
            R+=dR
            N=8
            multiRingList[rN+1]=self.createVertex4Poly(R,dR,N)

        return multiRingList

    def getBoxList(self,coboIdx):
        shiftX,shiftY=self.shift
        coboW = self.coboW
        coboH = self.coboH

        shiftX=self.getRightShiftX(coboIdx)
        boxList=[[] for i in range(4)]

        boxList[0]=[shiftX,shiftY]
        boxList[1]=[shiftX,shiftY+coboH]
        boxList[2]=[shiftX+coboW,shiftY+coboH]
        boxList[3]=[shiftX+coboW,shiftY]

        return boxList


    def getTestBoxList(self,shifts=[400,100]):
        shiftX,shiftY=shifts
        boxW = 100
        boxH = 100

        # shiftX+=coboIdx*boxW
        boxList=[[] for i in range(4)]

        boxList[0]=[shiftX,shiftY]
        boxList[1]=[shiftX,shiftY+boxH]
        boxList[2]=[shiftX+boxW,shiftY+boxH]
        boxList[3]=[shiftX+boxW,shiftY]

        return boxList

    # def color_config(self, widget, color, event):
    #     widget.configure(foreground=color)

    def detect2Num(self,detectSet):
        dNumber=0
        dIntList=[[[0 for d in ring] for ring in section[1]]\
                  for section in detectSet]
        for sIndex in range(len(detectSet)):
            section=detectSet[sIndex][1]#Using the polyList
            for rIndex in range(len(section)):
                ring=section[rIndex]
                for dIndex in range(len(ring)):
                    dIntList[sIndex][rIndex][dIndex]=dNumber
                    dNumber+=1
        return dIntList

    def detect2Pid(self,detectSet):
        pidV=0
        pidList=[[[0 for d in ring] for ring in section[1]]\
                  for section in detectSet]
        for sIndex in range(len(detectSet)):
            section=detectSet[sIndex][1]#Using the polyList
            for rIndex in range(len(section)):
                ring=section[rIndex]
                for dIndex in range(len(ring)):
                    if self.checkFpn(pidV):
                        pidV+=1 #if fpn next val won't be
                    pidList[sIndex][rIndex][dIndex]=pidV
                    pidV+=1
        return pidList

    #Simple test print out
    def printRtest(self, dIntList,pidList):
        print("Inside print2Test")
        for sec in dIntList:
            sIndex=dIntList.index(sec)
            print("Section = ", sIndex)
            for ring in sec:
                rIndex=sec.index(ring)
                print("Ringnum = ", rIndex)
                print("listValue = ", dIntList[sIndex][rIndex])
                print("Using pidList = ", pidList[sIndex][rIndex])

    def getPidNumber(self,cobo, asad, aget, chan):
        #TODO: put this in a more global place
        chanInAGET=68
        agetInASAD=4
        asadInCOBO=4
        coboInCrate=10 #? Unsure of this

        agetCoef=chanInAGET
        asadCoef=agetInASAD*agetCoef
        coboCoef=asadInCOBO*asadCoef

        pid=coboCoef*cobo+asadCoef*asad+agetCoef*aget+chan
        return pid

    def getCrateRoute(self, pid):
        #TODO: put this in a more global place
        chanInAGET=68
        agetInASAD=4
        asadInCOBO=4
        coboInCrate=10 #? Unsure of this

        agetCoef=chanInAGET
        asadCoef=agetInASAD*agetCoef
        coboCoef=asadInCOBO*asadCoef

        # pid-=1

        cobo = int(pid/coboCoef)
        coboRes = pid%coboCoef

        asad = int(coboRes/asadCoef)
        asadRes = coboRes%asadCoef

        aget = int(asadRes/agetCoef)
        asadRes = asadRes % agetCoef

        chan = asadRes

        return [cobo,asad,aget,chan]

    def readXmlState(self):
        xmlDict=self.doc
        pidList=self.pidList
        for sec in pidList:
            sIndex=pidList.index(sec)
            localOnOffL=self.masterList[sIndex][3]
            for ring in sec:
                rIndex=sec.index(ring)
                for det in ring:
                    dIndex=ring.index(det)

                    pidV=pidList[sIndex][rIndex][dIndex]
                    cobo,asad,aget,ch=self.getCrateRoute(pidV)
                    readVal=getOptVal(xmlDict,cobo,asad,aget,ch,"isActive")
                    localOnOffL[rIndex][dIndex]=readVal

            self.masterList[sIndex][3]=localOnOffL

    def write2Dict(self):
        xmlDict=self.doc
        pidList=self.pidList #Enumerated detectors by pid
        for sec in pidList:
            sIndex=pidList.index(sec)
            localOnOffL=self.masterList[sIndex][3]
            for ring in sec:
                rIndex=sec.index(ring)
                for det in ring:
                    dIndex=ring.index(det)
                    onOffVal=localOnOffL[rIndex][dIndex]

                    pidV=pidList[sIndex][rIndex][dIndex]
                    cobo,asad,aget,ch=self.getCrateRoute(pidV)
                    xmlDict=self.getUp2ChXD(xmlDict,onOffVal,\
                                            cobo,asad,aget,ch)

        self.doc=xmlDict

    def getRightDict(self, chId, dVal=False, option="isActive"):
        chId=str(chId)
        if dVal == True:
            dVal = 'true'
        elif dVal == False:
            dVal = 'false'

        lVar=OrderedDict([('@id', chId), (option, dVal)])
        return lVar

    def getUp2ChXD(self,xmlDict,onOffVal,cobo,asad,aget,ch):
        rVar=getRoute(xmlDict,cobo,asad,aget,ch)
        cInsIdx=rVar[2]
        coboIdx=rVar[4]
        asadIdx=rVar[6]

        if rVar[-1]=='Aget':
            leaf=xmlDict["Setup"]["Node"][cInsIdx]\
                  ["Instance"][coboIdx]["AsAd"][asadIdx]\
                  ["Aget"]

            aget=str(aget)
            leaf.append(OrderedDict([("@id", aget),\
                                     ('channel', [])]))
            chanDict=self.getRightDict(ch,onOffVal)
            leaf[-1]['channel'].append(chanDict)

            xmlDict["Setup"]["Node"][cInsIdx]\
                  ["Instance"][coboIdx]["AsAd"][asadIdx]\
                  ["Aget"]=leaf

        elif rVar[-2]=='AsAd':
            leaf=xmlDict["Setup"]["Node"][cInsIdx]\
                  ["Instance"][coboIdx]["AsAd"][asadIdx]
            leaf['Aget']=[]
            newLeaf=leaf['Aget']

            aget=str(aget)
            newLeaf.append(OrderedDict([("@id", aget),\
                                     ('channel', [])]))
            chanDict=self.getRightDict(ch,onOffVal)
            newLeaf[-1]['channel'].append(chanDict)

            xmlDict["Setup"]["Node"][cInsIdx]\
                  ["Instance"][coboIdx]["AsAd"][asadIdx]\
                  ["Aget"]=newLeaf

        elif rVar[-1]=='channel':
            agetIdx=rVar[8]

            leaf=xmlDict["Setup"]["Node"][cInsIdx]\
                  ["Instance"][coboIdx]["AsAd"][asadIdx]\
                  ["Aget"][agetIdx]["channel"]

            lVar=self.getRightDict(ch, onOffVal)
            leaf.append(lVar)

            xmlDict["Setup"]["Node"][cInsIdx]\
                  ["Instance"][coboIdx]["AsAd"][asadIdx]\
                  ["Aget"][agetIdx]["channel"] = leaf
        else:
            agetIdx=rVar[8]
            chanIdx=rVar[10]
            lVar=self.getRightDict(ch, onOffVal)

            xmlDict["Setup"]["Node"][cInsIdx]\
                ["Instance"][coboIdx]["AsAd"]\
                [asadIdx]["Aget"][agetIdx]["channel"]\
                [chanIdx]['isActive']=lVar['isActive']

        return xmlDict

    def drawZone1(self):
        #Sending data [0,0] so it redraws the first zone
        self.listIndex=0
        #Twice so the 0,0 polygon stays the same, not very elegant but
        #it works ;-P
        self.redrawRing([0,0])
        self.redrawRing([0,0])
        self.writeRegionInfo(0)

    def writeRegionInfo(self, indexInfo):
        self.canvas_idD= self.canvasD.create_text(100,20)
        textVar="region "+str(indexInfo)
        self.canvasD.itemconfig(self.canvas_idD, text=textVar)

    def writeDetectInfo(self, indexInfo,indexList):
        pidList=self.pidList
        sIndex=indexInfo
        rIndex,dIndex=indexList
        pidV=pidList[sIndex][rIndex][dIndex]
        self.canvas_idD= self.canvasD.create_text(100,50)
        # textVar="GET route "+str(sIndex)+" "+str(rIndex)+" "+str(dIndex)
        cobo,asad,aget,chan=self.getCrateRoute(pidV)
        textVar="GET route "+str([cobo,asad,aget,chan])
        self.canvasD.itemconfig(self.canvas_idD, text=textVar)

    #Checks if a pid end up in an fixed pattern noise channel (fpn)
    def checkFpn(self, pid):
        fpnChan=[11,22,45,56]
        cobo,asad,aget,ch=self.getCrateRoute(pid)
        if ch in fpnChan:
            return True
        return False

    def writeEnum(self, shapelyPolyList):
        for ring in shapelyPolyList:
            numOfPoly=len(ring)
            for poly,i in zip(ring,range(numOfPoly)):
                pCent=list(poly.centroid.coords)[0]
                textObj=self.canvasD.create_text(pCent[0],pCent[1])
                self.canvasD.itemconfig(textObj, text=str(i))

    def createShapelyCoboPoly(self,coboIdx):
        coboPolVertex=self.getBoxList(coboIdx)
        convexPolyPoints=list(MultiPoint(coboPolVertex).convex_hull.exterior.coords)
        shapelyPolygon=Polygon(convexPolyPoints)
        return shapelyPolygon

    def createShapelyTestPoly(self,testBoxList):
        convexPolyPoints=list(MultiPoint(testBoxList).convex_hull.exterior.coords)
        shapelyPolygon=Polygon(convexPolyPoints)
        return shapelyPolygon

    def getShapelyCoboPolyD(self):
        idxList=self.cobosIDXs
        coboW=self.coboW
        shapelyCoboPolyD={}
        for idx in idxList:
            shapelyCoboPoly=self.createShapelyCoboPoly(idx)
            shapelyCoboPolyD[idx]=shapelyCoboPoly

        return shapelyCoboPolyD

    def getAsadCon(self,coboIdx,asadIdx):
        shiftX,shiftY=self.shift
        coboW = self.coboW
        coboH = self.coboH

        asadW = self.asadConW
        asadH = self.asadConH

        shiftX=self.getRightShiftX(coboIdx)

        if asadIdx in [0,1]:
            shiftY+=34
        else: #[2,3]
            shiftY+=107

        if asadIdx in [1,3]:
            shiftX+=15
        else: #[0,2]
            shiftX+=29

        asadCoords=[[] for i in range(4)]

        asadCoords[0]=[shiftX,shiftY]
        asadCoords[1]=[shiftX,shiftY+asadH]
        asadCoords[2]=[shiftX+asadW,shiftY+asadH]
        asadCoords[3]=[shiftX+asadW,shiftY]

        return asadCoords

    def getShapelyPolyFromList(self,coordsList):
        convexPolyPoints=list(MultiPoint(coordsList).convex_hull.exterior.coords)
        shapelyPolygon=Polygon(convexPolyPoints)
        return shapelyPolygon

    def getAsadsPolyListDForAllCobos(self,asadsConDCoords):
        asadsConDCoords=self.asadsConDCoords
        asadsPolyListDForAllCobos={}
        for coboKey in asadsConDCoords:
            asadsPolyListDForAllCobos[coboKey]=self.getAsadsPolyListForCobo(coboKey)

        return asadsPolyListDForAllCobos

    def getAsadsPolyListForCobo(self,coboKey):
        asadsConDCoords=self.asadsConDCoords
        localCoordL=asadsConDCoords[coboKey]
        asadsPolyListForCobo=[]
        for asadCoord in localCoordL:
            myAsadConShapelyPoly=self.getShapelyPolyFromList(asadCoord)
            asadsPolyListForCobo.append(myAsadConShapelyPoly)

        return asadsPolyListForCobo


    def getLocalAsadConL(self,coboIdx):
        localAsadConL=[]

        for asadIdx in range(4):
            newAsadCon=self.getAsadCon(coboIdx,asadIdx)
            localAsadConL.append(newAsadCon)

        return localAsadConL

    def getAsadsConDCoords(self):
        coboIdxL=self.cobosIDXs
        asadsConD={}
        for coboIdx in coboIdxL:
            asadsConD[coboIdx]=self.getLocalAsadConL(coboIdx)
        return asadsConD

    def getAsadsConDShapelyPoly(self):
        asadsConDPoly={}
        asadsConD=self.asadsConD
        for asadsConKey in asadsConD:
            coordsList=asadsConD[asadsConKey]
            asadsConDPoly[asadsConKey]=self.getShapelyPolyFromList(coordsList)
        return asadsConDPoly

    def getCoordsFromShapelyPoly(self,myShapelyPolygon):
        uglyBoxList=myShapelyPolygon.exterior.coords.xy

        myXList,myYList=uglyBoxList
        totLen=len(myXList)
        #Not sure if the int() is really needed
        prettyBoxList=[[int(myXList[i]),int(myYList[i])] for i in range(totLen)]
        return prettyBoxList

    def getRightShiftX(self,coboIdx):
        shiftX=self.shift[0]

        coboW=self.coboW

        shiftX+=coboW #excluding the first slot

        if coboIdx >=5:
            #jump the network and mutant slots
            shiftX+=2*coboW
        shiftX+=coboIdx*coboW

        return shiftX

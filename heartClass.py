from tkinter import *
from shapely.geometry import Polygon,MultiPoint,Point
import random
from math import pi,sin,cos

from xmlParser import *

class myAwesomeClass():
    def __init__(self, master):

        master.wm_title("Heartbit")
        self.debugVar=False
        self.sideList=[16,24,32,40,40,48,48,48,48,32,32]
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
        # self.shapelyPolyList=[] #Twice?!
        self.masterList=[]
        self.onOffList=[]

        self.dIntList=[]
        # master.iconbitmap(r"heart.png")

        # self.doc=getXmlDoc('configure-cobomutant.xcfg')
        self.doc=getXmlDoc('modifiedXml2.xml')

        self.var=self.doc['Setup']['@id'] # == u'Conditions'

        self.dummyVar=""

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

        self.canvasD = Canvas(rDownFrame, bg="white", width=self.W, height=self.H)

        self.canvasD.grid(row = 0, column = 0)

        self.masterList=self.fillAllRings()

        #The new functions
        self.initRing(0)

        self.dIntList=self.detect2Num(self.masterList)
        # self.printRtest(self.dIntList)

        self.readXmlState()

        # print("onOffList")
        # print(self.onOffList)

        getRoute(self.doc, 1,3,1,5)

        self.dummyVar=getOptVal(self.doc,1,3,1,5, "isActive")

        self.canvasD.bind("<Key>", self.key)
        self.canvasD.bind("<Button-1>", self.callbackD)
        self.canvasD.pack()

        # self.canvasD.delete(self.arc)

    def callbackD(self, event):
        # print("Lower canvas")
        # print("clicked at", e
              # vent.x, event.y)
        self.myPoint=Point(event.x, event.y)
        # if self.shapelyPoly.contains(self.myPoint):
        #     print("Point inside the polygon!!")
        indexList=self.checkEventInPolyList(event.x, event.y)
        # print("Index list is: ",indexList)
        # print("b4 if len(self.poly4DrawList)",len(self.poly4DrawList))
        if indexList != []:
            self.redrawRing(indexList)
        # self.genRandInt()
        # print("getPolySides(%d) = %d" % (self.myRandInt, self.getPolySides(self.myRandInt)))


    def callback(self, event):
        # print("Upper canvas")
        x=event.x
        y=event.y
        # print("clicked at", x, y)
        region=self.ringRegion(x,y)
        self.listIndex=region
        # print("region = ", region)

        # self.genRandInt()
        self.initRing(region)

        # print("getPolySides(%d) = %d" % (self.myRandInt, self.getPolySides(self.myRandInt)))

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
        outFileName="modifiedXml2.xml"
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
        # print("len(poly4DrawList) = ", len(poly4DrawList))

        for i in range(len(poly4DrawList)):
            for poly in poly4DrawList[i]:
                polyIndex=poly4DrawList[i].index(poly)
                color=getColor(i,polyIndex,indexStuff)

                polyDrawnL[i].append(self.canvasD.create_polygon(poly,fill=color,stipple="gray50", outline="#f12", width=2))

        # print("onOffList")
        # print(self.onOffList)

        return polyDrawnL

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

    def initRing(self,ringNum=0):
        self.canvasD.delete("all")

        self.myVList=self.masterList[ringNum][0]
        self.shapelyPolyList=self.masterList[ringNum][1]

        self.poly4DrawList=self.masterList[ringNum][2]

        self.onOffList=self.masterList[ringNum][3]
        # print("initRing, self.onOffList = ",self.onOffList)

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

    # def color_config(self, widget, color, event):
    #     widget.configure(foreground=color)

    def detect2Num(self,detectSet):
        # print("Inside detect2Num")
        dNumber=0
        # print("lenStuff = ",len(detectSet))
        dIntList=[[[0 for d in ring] for ring in section[1]]\
                  for section in detectSet]
        # print("After the dIntList generation")
        for sIndex in range(len(detectSet)):
            # sIndex=detectSet.index(section)
            # print("sIndex = ", sIndex)
            section=detectSet[sIndex][1]#Using the polyList
            # print("Section len = ", len(section))
            for rIndex in range(len(section)):
                # rIndex=section.index(ring)
                # print("rIndex = ", rIndex)
                ring=section[rIndex]
                # print("ring len", len(ring))
                for dIndex in range(len(ring)):
                    # dIndex=ring.index(detect)

                    # print("dIndex = ", dIndex)
                    dIntList[sIndex][rIndex][dIndex]=dNumber
                    dNumber+=1
                    # print("dNumber = ", dNumber)
        # print("dNumber = ", dNumber)
        return dIntList

    #Simple test print out
    def printRtest(self, dIntList):
        print("Inside print2Test")
        for sec in dIntList:
            sIndex=dIntList.index(sec)
            print("Section = ", sIndex)
            for ring in sec:
                rIndex=sec.index(ring)
                print("Ringnum = ", rIndex)
                print("listValue = ", dIntList[sIndex][rIndex])

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
        dIntList=self.dIntList #Enumerated detectors
        for sec in dIntList:
            sIndex=dIntList.index(sec)
            localOnOffL=self.masterList[sIndex][3]

            for ring in sec:
                rIndex=sec.index(ring)

                for det in ring:
                    dIndex=ring.index(det)

                    dNum=dIntList[sIndex][rIndex][dIndex]
                    cobo,asad,aget,ch=self.getCrateRoute(dNum)
                    pB=False
                    if dNum == 56:
                        print("dNum = %d"% dNum)
                        pB=True
                    readVal=getOptVal(xmlDict,cobo,asad,aget,ch,"isActive",pB)
                    localOnOffL[rIndex][dIndex]=readVal

            self.masterList[sIndex][3]=localOnOffL

    def write2Dict(self):
        xmlDict=self.doc
        dIntList=self.dIntList #Enumerated detectors
        for sec in dIntList:
            sIndex=dIntList.index(sec)
            localOnOffL=self.masterList[sIndex][3]

            for ring in sec:
                rIndex=sec.index(ring)

                for det in ring:
                    dIndex=ring.index(det)
                    onOffVal=localOnOffL[rIndex][dIndex]

                    dNum=dIntList[sIndex][rIndex][dIndex]
                    cobo,asad,aget,ch=self.getCrateRoute(dNum)
                    self.debugVar=False
                    if dNum == 56:
                        self.debugVar=True
                        print("Inside writting part of %d" % dNum)
                        print("cobo,asad,aget,ch = ", cobo,asad,aget,ch)
                        print("The onOffVal is ", onOffVal)
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
            if self.debugVar:
                print("getUp2ChXD first cond")
                print(leaf)

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

            if self.debugVar:
                print("getUp2ChXD second cond")
                print(newLeaf)

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
            if self.debugVar:
                print("getUp2ChXD third cond")
                print(leaf)
        else:
            agetIdx=rVar[8]
            chanIdx=rVar[10]
            lVar=self.getRightDict(ch, onOffVal)

            xmlDict["Setup"]["Node"][cInsIdx]\
                ["Instance"][coboIdx]["AsAd"]\
                [asadIdx]["Aget"][agetIdx]["channel"]\
                [chanIdx]['isActive']=lVar['isActive']
            if self.debugVar:
                print("getUp2ChXD else")
                print(lVar['isActive'])
                print("Getting the route")
                print(rVar)

        return xmlDict

import xmltodict
from collections import OrderedDict

def getXmlDoc(filename):
    with open(filename) as fd:
        doc = xmltodict.parse(fd.read())

    print("The var as soon as it is read")
    lRoute=getRoute(doc,0,0,0,56)
    print("Route is ", lRoute)
    leafVar=doc["Setup"]["Node"][1]\
                ["Instance"][1]["AsAd"]\
                [4]["Aget"][4]["channel"]\
                [1]
    print(leafVar)
    doc = getCheckedDict(doc) #Adapting the xmlvar to our standard
    return doc

def printDocProp(docVar):
    print(docVar["Setup"]["Node"][1]["@id"])
    print("len(node part) = ",len(docVar["Setup"]["Node"][1]["@id"]))
    print(docVar["Setup"]["Node"][1]["Instance"][1]["@id"]) #Crate00_Slot00
    print(docVar["Setup"]["Node"][1]["Instance"][1]["AsAd"][0]["Aget"][1]["channel"][0]["@id"])
    print("\n\nEntering the for\n")
    for e in docVar["Setup"]["Node"][1]["Instance"][1]["AsAd"][0]["Aget"][1]["channel"][0]:
        print(e)


def getRoute(docVar, cobo=0, asad=0, aget=0, ch=0):
    #Note this has to eventually handle the *'s
    #For cobo, asad, aget and chan
    coboStr=str(cobo)
    if len(coboStr)==1:
        coboStr='0'+coboStr
    slotName='Crate00_Slot'+coboStr

    routeVar=[]

    if asad not in range(4):
        print("Error, asad has to be in, ", range(4))
        return routeVar

    if "Setup" not in docVar:
        print("Error \"Setup\" is not present")
        return routeVar

    routeVar.append("Setup")

    setupDict=docVar["Setup"]

    if "Node" not in setupDict:
        print("Error \"Node\" info not present")
        return routeVar

    routeVar.append("Node")

    nodeList=setupDict["Node"]
    cNodeIdx=getIdxOfID(nodeList,'CoBo')

    if cNodeIdx == -1:
        print("Error, no name \"CoBo\" found")
        return routeVar

    routeVar.append(cNodeIdx)

    coboDict=nodeList[cNodeIdx]

    if "Instance" not in coboDict:
        print("Error, \"Instance\" not found")
        return routeVar

    routeVar.append("Instance")

    instanceList=coboDict["Instance"]

    #The specific list index of our CoBo (given by the cobo var)
    instanceIdx= getIdxOfID(instanceList, slotName)

    if instanceIdx == -1:
        print("Error, name '%s' not found the requested cobo"%slotName)
        return routeVar

    routeVar.append(instanceIdx)

    specificCOBO=instanceList[instanceIdx]

    if "AsAd" not in specificCOBO:
        print("Error, no 'AsAd' found in this CoBo")
        return routeVar

    routeVar.append("AsAd")

    asadList=specificCOBO["AsAd"]

    asadIdx= getIdxOfID(asadList, asad)

    asadDict=asadList[asadIdx]

    routeVar.append(asadIdx)

    if "Aget" not in asadDict:
        return routeVar

    routeVar.append("Aget")

    agetList=asadDict["Aget"]
    if type(agetList) is not list:
        # print("Entered the type condition, type is.", type(agetList))
        agetList=[agetList]

    agetIdx=getIdxOfID(agetList, aget)

    if agetIdx == -1:
        return routeVar

    routeVar.append(agetIdx)

    specificAget=agetList[agetIdx]

    if "channel" not in specificAget:
        print("Error, no 'channel' in specificAget")
        return routeVar

    routeVar.append("channel")
    chanList=specificAget["channel"]

    try:
        chanIdx=getIdxOfID(chanList, ch)
    except:
        print("Error found here")

    chanIdx=getIdxOfID(chanList, ch)

    if chanIdx == -1:
        return routeVar

    routeVar.append(chanIdx)

    specificChan=chanList[chanIdx]

    return routeVar

def getIdxOfID(listOfOrderedDicts, idVal):
    idVal=str(idVal)
    for e,i in zip(listOfOrderedDicts,range(len(listOfOrderedDicts))):
        newVar=e["@id"]
        if idVal == newVar:
            return i
    return -1

def getOptVal(xmlDict,cobo,asad,aget,ch,opt="isActive",pBool=False):
    if opt != "isActive":
        print("Option not implemented yet")
        return False

    if pBool:
        print("Got the signal")
    lRoute=getRoute(xmlDict,cobo,asad,aget,ch)
    # print("lRoute = ", lRoute)

    routeBool=routeTest(lRoute)

    if routeBool:
        # xmlDict=getUp2ChXD(self,xmlDict,onOffVal,cobo,asad,aget,ch):
        if pBool:
            print("In routeBool conditional")
        return True

    cInsIdx=lRoute[2] #The index in the Instance list for the CoBo
    coboIdx=lRoute[4] #The index in the CoBo list for cobo
    asadIdx=lRoute[6] #...
    agetIdx=lRoute[8]
    chanIdx=lRoute[10]

    leaf=xmlDict["Setup"]["Node"][cInsIdx]["Instance"][coboIdx]["AsAd"]\
          [asadIdx]["Aget"][agetIdx]["channel"][chanIdx]

    #Leaving the following in case getCheckedDict has to be debugged

    # try:
    #     leaf=leaf1[agetIdx]["channel"][chanIdx] #["channel"][chanIdx]
    # except:
    #     leaf=leaf1["channel"][chanIdx]
    #     print("Entered the except part")
    #     print("The agetIdx is, ", agetIdx)


    if opt not in leaf:
        #By default is true if it made it up to here
        if pBool:
            print("Not in leaf option")
        return True

    #If not, we read it, it could be either true or false
    optionVal=leaf[opt]

    if pBool:
        print("optionVal = %s" % optionVal)
        print("cobo, asad, aget, ch = ",cobo,asad,aget,ch)
        print("lRoute = ", lRoute)
        print("leaf = ", leaf)

    if optionVal == 'true':
        if pBool:
            print("Read optionVal as true")

        return True

    #For now hoping false is the other valid option (may not be in
    #other cases)
    # print("Found false case")
    if pBool:
        print("Returning False")
    return False

def getCheckedDict(xmlDict):
    #first check the indeces up to 'CoBo' then call the recursive
    #function
    if "Setup" not in xmlDict:
        print("Error, 'Setup' is not defined in xml file")
        return False

    if "Node" not in xmlDict["Setup"]:
        print("Error, 'Node' not found in xmlDict")
        return False

    if len(xmlDict["Setup"]["Node"]) == 0:
        print("Error, no indeces found in Node")
        return False

    if type(xmlDict["Setup"]["Node"]) is not list:
        #Make it a list so it respects our standard
        xmlDict["Setup"]["Node"]=[xmlDict["Setup"]["Node"]]

    coboIdx=getIdxOfID(xmlDict["Setup"]["Node"],'CoBo')
    subXmlDict=xmlDict["Setup"]["Node"][coboIdx]
    print("Stuff into xmlRecursive...", type(subXmlDict))
    subXmlDict=xmlRecursiveListChecked(subXmlDict)

    xmlDict["Setup"]["Node"][coboIdx]=subXmlDict

    return xmlDict

def xmlRecursiveListChecked(xmlDict):
    #Iterative recursive function for the rest of the dictionary
    #structure
    if type(xmlDict) is not OrderedDict:
        print("Found weird part")
        print(xmlDict)

        return xmlDict

    for e in xmlDict:
        myType=type(xmlDict[e])
        if myType is OrderedDict:
            xmlDict[e] = [xmlDict[e]]
        elif myType is str:
            continue

        dictList=xmlDict[e]
        for subDict,i in zip(dictList, range(len(dictList))):
            # print("Recursive part", i)
            xmlDict[e][i]=xmlRecursiveListChecked(subDict)

    return xmlDict

def routeTest(lRoute):
    if "Aget" not in lRoute or "Aget" == lRoute[-1]:
        #It is "on" if there is no index to get to it (blue)
        return True

    #channel was the last appended but no indeces then it's in blue
    if "channel" == lRoute[-1]:
        return True

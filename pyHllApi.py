from hllApi import HllApi
from time import sleep
from TestingException import *



class PyHllApi(HllApi):

    pSpace = bytes()

    def psConnect(self, psid):
        self.pSpace = bytes(psid)
        self.connectPresentationSpace(psid)
        self.setSessionParameters("IPAUSE")
        self.setSessionParameters("NWAIT")

    def notifyHost(self, timeOut=300):
        beforeScreen = str()
        beforeScreen = self.copyPresentationSpaceToString(
            beforeScreen)['screen']
        self.startHostNotification(self.pSpace + "   B")
        self.sendKey("@E")
        while(self.wait() > 0 and timeOut > 0):
            sleep(0.01)
        while(self.queryHostUpdate(self.pSpace) != 0 and timeOut > 0):
            self.pause(1)
            sleep(0.01)
            timeOut -= 1
        self.stopHostNotification(self.pSpace)
        afterScreen = str()
        afterScreen = self.copyPresentationSpaceToString(
            afterScreen)['screen']
        while(beforeScreen == afterScreen and timeOut > 0):
            afterScreen = self.copyPresentationSpaceToString(
                afterScreen)['screen']
            sleep(0.01)
            timeOut -= 1
        if(timeOut == 0):
            raise(TestingException("Timeout: Host timed out. Please Try Again"))
            
    def notifySearch(self, searchString, timeOut=300):
        self.notifyHost(timeOut)
        while(timeOut > 0 and self.
              searchPresentationSpace(searchString)['returnCode'] != 0):
            sleep(0.01)
            timeOut -= 1
        if(timeOut == 0):
            raise(TestingException("Timeout looking for: " + fieldName))
        
            

    def findEntryField(self, fieldName):
        location = self.searchPresentationSpace(fieldName)['position']
        if( location > 0 ):
            return self.findFieldPosition("NU", location)['length']
        else:
            return -1

    def fillEntryField(self, fieldName, fieldValue):
        location = self.findEntryField(fieldName)
        if( location > 0 ):
            return self.copyStringToField(fieldValue, location)
        else:
            raise(TestingException("Field: " + fieldName + " is not found"))
            return -1

    def clearScreen(self, timeOut=300):
        self.sendKey("@C")
        while(self.wait() > 0 and timeOut > 0):
            sleep(0.01)
            
    def processScreen(self, screen):
        count = 0
        buildString = ""
        while count < 8000:
            buildString = buildString + screen[count]
            if count % 80 == 0:
                buildString = buildString + "\n"
            count = count + 1
        return buildString   
    
    def printScreen(self):
        i = 0
        fullScreenPrint = " "
        sepLine = "\n--------------------------------------------------------------------------------\n"
        while i < 8000:
            fullScreenPrint = fullScreenPrint + " "
            i = i + 1
            
        fullScreenPrint = self.copyPresentationSpace(fullScreenPrint)
        finalString = self.processScreen(fullScreenPrint)
        finalString = sepLine + finalString.strip() + sepLine
        print ("Screen Shot Taken")
        return finalString


if __name__ == "__main__":
    pyhllapi = PyHllApi("C:\\Program Files\\Ericom Software\\PowerTerm Enterprise\\hllapi32.dll")
    pyhllapi.psConnect("A")

    pyhllapi.notifySearch("Userid")
    pyhllapi.fillEntryField("Userid", "SOMEID")
    pyhllapi.notifyHost()
    pyhllapi.disconnectPresentationSpace()
    

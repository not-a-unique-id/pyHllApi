from ctypes import *
import sys

class HllApi(object): 
    """A class that implements various HLLAPI DLL functions"""

    def __init__(self, dllLoc):
        self.hllDll = WinDLL (dllLoc)
        self.hllapi = self.hllDll.WinHLLAPI

    def connectPresentationSpace(self, presentation_space):
        function_number = c_int(1)
        data_string = c_char_p(presentation_space)
        length = c_int(4)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def disconnectPresentationSpace(self):
        function_number = c_int(2)
        data_string = c_char_p()
        length = c_int(4)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def sendKey(self, key):
        function_number = c_int(3)
        data_string = c_char_p(key)
        length = c_int(len(key))
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def wait(self):
        function_number = c_int(4)
        data_string = c_char_p()
        length = c_int()
        ps_position = c_int()
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def copyPresentationSpace(self, screen):
        function_number = c_int(5)
        data_string = screen
        length = c_int(8000)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return data_string.decode('latin-1')

    def searchPresentationSpace(self, targetString):
        function_number = c_int(6)
        encString = targetString.encode('ascii', 'ignore')
        data_string = c_char_p(encString)
        length = c_int(len(encString))
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return {'returnCode':ps_position.value, 'position':length.value}

    def copyPresentationSpaceToString(self, targetString):
        function_number = c_int(8)
        targetString = " " * 1920
        data_string = c_char_p(targetString)
        length = c_int(1920)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string, byref(length),
                    byref(ps_position))
        return {'returnCode':ps_position.value, 'screen':data_string.value,}

    def setSessionParameters(self, dataString):
        function_number = c_int(9)
        data_string = dataString
        length = c_int(len(dataString))
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def copyStringToPresentationSpace(self, string, position):
        function_number = c_int(15)
        encString = string.encode('ascii', 'ignore')
        data_string = encString
        length = c_int(len(string))
        ps_position = c_int(position)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def pause(self, time):
        function_number = c_int(18)
        data_string = None
        length = c_int(time)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def querySessionStatus(self, presentation_space):
        function_number = c_int(22)
        data_string = c_char_p(presentation_space)
        length = c_int(20)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def startHostNotification(self, params):
        function_number = c_int(23)
        data_string = c_char_p(params)
        length = c_int(16)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def queryHostUpdate(self, presentation_space):
        function_number = c_int(24)
        data_string = c_char_p(presentation_space)
        length = c_int(4)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

    def stopHostNotification(self, presentation_space):
        function_number = c_int(121)
        data_string = c_char_p(presentation_space)
        length = c_int(4)
        ps_position = c_int(0)
        self.hllapi(byref(function_number),
                    data_string, byref(length),
                    byref(ps_position))
        return ps_position.value

    def findFieldPosition(self, string, position):
        function_number = c_int(31)
        data_string = c_char_p(string)
        length = c_int(len(string))
        ps_position = c_int(position)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return {'returnCode':ps_position.value, 'length':length.value,}

    def copyStringToField(self, string, position):
        function_number = c_int(33)
        encString = string.encode('ascii', 'ignore')
        data_string = encString
        length = c_int(len(string))
        ps_position = c_int(position)
        self.hllapi(byref(function_number),
                    data_string,
                    byref(length),
                    byref(ps_position))
        return ps_position.value

if __name__ == "__main__":
    print("test main")
    test = HllApi("C:\\Program Files\\Ericom Software\\PowerTerm Enterprise\\hllapi32.dll")
    print(test.connectPresentationSpace("A"))
    print(test.copyStringToField("TESTING123", 1889))
    print(test.disconnectPresentationSpace())

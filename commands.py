#!/usr/bin/env python

from communication import Communication
from enum import Enum

class GeneralCommand(Enum):
    GetDeviceInformation = 1
    SetVoltage = 2
    GetVoltage = 3
    SetCurrent = 4
    GetCurrent = 5
    SelectChannel = 6
    SetOutput = 7
    
class Command():
    def __init__(self, command, length):
        self.command = command
        self.length = length
        
    def __mod__(self, value):
        return self.command % value
    
    def __str__(self):
        return self.command

class Device:    
    def __init__(self, device):
        self._GeneralCommands = {
                                  GeneralCommand.GetDeviceInformation : None,
                                  GeneralCommand.SetVoltage : None,
                                  GeneralCommand.GetVoltage : None,
                                  GeneralCommand.SetCurrent : None,
                                  GeneralCommand.GetCurrent : None,
                                  GeneralCommand.SelectChannel : None,
                                  GeneralCommand.SetOutput : None,
                                }
        self.__device = Communication(device)
        
    def __SelectChannel(self,channel): 
        self.__device.Write(self._GeneralCommands[GeneralCommand.SelectChannel] % channel)   
    
    def SetVoltage(self, channel, voltage):
        self.__SelectChannel(channel)
        
        self.__device.Write(self._GeneralCommands[GeneralCommand.SetVoltage] % voltage)
        
    def GetVoltage(self, channel):
        self.__SelectChannel(channel)
        self.__device.Write(self._GeneralCommands[GeneralCommand.GetVoltage])
        val = self.__device.Read(self._GeneralCommands[GeneralCommand.GetVoltage].length)
        print "val=" + str(val)
        
    def SetCurrent(self, channel, current):
        pass
    
    def GetCurrent(self, channel):
        pass
    
    def SetOutput(self, channel, state):
        self.__SelectChannel(channel)
        self.__device.Write(self._GeneralCommands[GeneralCommand.SetOutput] % state)
        
class HMC804xDevice(Device):
    def __init__(self, device):
        Device.__init__(self,device)
        
        self.__linefeed = "\n"
        self._GeneralCommands[GeneralCommand.SelectChannel] = Command("INST:NSEL %i" + self.__linefeed, None)
        self._GeneralCommands[GeneralCommand.SetVoltage] = Command("VOLT %f" + self.__linefeed, None)
        self._GeneralCommands[GeneralCommand.GetVoltage] = Command("VOLT?" + self.__linefeed, 10)
        self._GeneralCommands[GeneralCommand.SetOutput] = Command("OUTP %f" + self.__linefeed, None)
        
    
class DummyCommands(Device):
    def __init__(self):
        Device.__init__(self)
        
        
if __name__ == "__main__":
#     mycommand = HMC804xDevice()
#     mycommand.GetVoltage()
    print dir(Device)
    
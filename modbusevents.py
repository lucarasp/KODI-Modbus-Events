# CONSTANTS
__author__ = 'lucarasp'
__version__ = '1.0.0'
__url__ = ''
__date__ = '1/2016'

# imports
import sys
import os
import subprocess
import xbmc
import xbmcgui
import xbmcaddon
import urllib
import urllib2
from pymodbus.client.sync import ModbusTcpClient

# fetch addon information
moodbus_events = xbmcaddon.Addon('service.script.modbusevents')

# add libraries to path
library_path = modbus_events.getAddonInfo('path') + '/resources/Lib/'
sys.path.append(library_path)
library_path = modbus_browse.getAddonInfo('path') + '/resources/lib/'
sys.path.append(library_path)

# custom imports

#import pyisy
#import xb_events
import log
#import event_actions

#Initialize ADDON
__addon__     = xbmcaddon.Addon()

#Initialize ADDON LOG Settings (for Debugging)
xbmc.log('Modbus Commander: ******************* Modbus Commander ******************')
if (str(__addon__.getSetting("DEBUGLOG")) == "true"):
    debuging = True
    xbmc.log('Modbus Commander: Debuging log files is on')
else:
    debuging = False
    xbmc.log('Modbus Commander: Debuging log files is off')
    xbmc.log('Modbus Commander: *************************************************')

#Initialize ADDON INFORMATION
__addonname__ = __addon__.getAddonInfo('name')
__cwd__       = __addon__.getAddonInfo('path')
__author__    = __addon__.getAddonInfo('author')
__version__   = __addon__.getAddonInfo('version')

if (debuging): 
    xbmc.log('Modbus Commander: *************** Addon information ***************')
    xbmc.log('Modbus Commander: Addon info name    : ' + __addonname__)
    xbmc.log('Modbus Commander: Addon info path    : ' + __cwd__)
    xbmc.log('Modbus Commander: Addon info author  : ' + __author__ )
    xbmc.log('Modbus Commander: Addon info version : ' + __version__)
    xbmc.log('Modbus Commander: *************************************************')

# FUNCTIONS - START

# Modbus TCP Functions
#This function Will execute the requested action via modbus connection
def ModbusTCP(URL, Reg, Value):
    #Modbus simple query
    #Example strings
    #client = ModbusTcpClient('127.0.0.1') 
	#client.write_coil(1, True)
	#print result.bits[0]
	#client.close()

    #these are with a plus, since the my_data needs to be concatenated with the url
    try:
    	client = ModbusTcpClient(URL)
    	client.write_register(Reg, Value)
    	client.close()
    	#ActionData = 'reg: ' + Reg + ' val: ' + Value    	
    	#if (debuging): xbmc.log('Modbus Commander: ModbusTCP: ' + URL + ActionData)
    	ReturnValue = "success"
    #except:
    	#ActionData = 'reg: ' + Reg + ' val: ' + Value
    	#if (debuging):	xbmc.log('Modbus Commander: ModbusTCP: ' + URL + ActionData + ' Event Failed')
    	ReturnValue = "fail"
    #	return ReturnValue

# MAINEVENTHANDLER FUNCTION
def MainEventHandler(Type):
    #This function is the MainEventHandler, 
    #It receive the type of event that needs to be executed
    #The type of event comes from XMBC or the XBMC Player
    #for every active Device, where the event is enabled it will execute the action (ExecuteAction)
    
    #INITIALIZE
    DeviceCount = 1
    Application =  "ModbusTCP" 
    DeviceURL = "'" + __addon__.getSetting("IP") + "\'," + __addon__.getSetting("PORT")
    URL = DeviceURL
    if (debuging): 
        xbmc.log('Modbus Commander: *************** Handeling an Event **************')
        xbmc.log('Modbus Commander: Event Type = ' + str(Type))
    
    #Handle all Device's
    while (DeviceCount <= 5):
        #INITIALIZE per device
        ActionReg = ""
        ActionValue = ""
        ActionCall = ""
        ExecuteEvent = False
        if (DeviceCount <= 9):
            strCheckDeviceEnabled = "DEVID0" + str(DeviceCount) + "ENABLE"
        else:
            strCheckDeviceEnabled = "DEVID" + str(DeviceCount) + "ENABLE"
        
        #Execute Event if Device is enabled
        if (str(__addon__.getSetting(strCheckDeviceEnabled)) == "true"):
            
            #Retrieve specific device settings for the Event
            if Type == "X_Start":
                if (DeviceCount <= 9):
                    strXevStartEnabled = "XEVSTARTENABLE0" + str(DeviceCount)
                    strXevStartReg = "XEVSTARTREG0" + str(DeviceCount)
                    strXevStartVal = "XEVSTARTVAL0" + str(DeviceCount)
                else:
                    strXevStartEnabled = "XEVSTARTENABLE" + str(DeviceCount)
                    strXevStartReg = "XEVSTARTREG" + str(DeviceCount)
                    strXevStartVal = "XEVSTARTVAL" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strXevStartEnabled)) == "true"):
                    ExecuteEvent = True
                    ActionReg = str(__addon__.getSetting(strXevStartReg))
                    ActionValue = str(__addon__.getSetting(strXevStartVal))
            elif Type == "X_Stop":
                if (DeviceCount <= 9):
                    strXevStopEnabled = "XEVSTOPENABLE0" + str(DeviceCount)
                    strXevStopReg = "XEVSTOPREG0" + str(DeviceCount)
                    strXevStopVal = "XEVSTOPVAL0" + str(DeviceCount)
                else:
                    strXevStopEnabled = "XEVSTOPENABLE" + str(DeviceCount)
                    strXevStopReg = "XEVSTOPREG" + str(DeviceCount)
                    strXevStopVal = "XEVSTOPVAL" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strXevStopEnabled)) == "true"):
                    ExecuteEvent = True
                    ActionReg = str(__addon__.getSetting(strXevStopReg))
                    ActionValue = str(__addon__.getSetting(strXevStopVal))
            elif Type == "P_Start":
                if (DeviceCount <= 9):
                    strPevStartEnabled = "PEVSTARTENABLE0" + str(DeviceCount)
                    strPevStartReg = "PEVSTARTREG0" + str(DeviceCount)
                    strPevStartVal = "PEVSTARTVAL0" + str(DeviceCount)
                else:
                    strPevStartEnabled = "PEVSTARTENABLE" + str(DeviceCount)
                    strPevStartReg = "PEVSTARTREG" + str(DeviceCount)
                    strPevStartVal = "PEVSTARTVAL" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevStartEnabled)) == "true"):
                    ExecuteEvent = True
                    ActionReg = str(__addon__.getSetting(strPevStartReg))
                    ActionValue = str(__addon__.getSetting(strPevStartVal))
            elif Type == "P_Stop":
                if (DeviceCount <= 9):
                    strPevStopEnabled = "PEVSTOPENABLE0" + str(DeviceCount)
                    strPevStopReg = "PEVSTOPREG0" + str(DeviceCount)
                    strPevStopVal = "PEVSTOPVAL0" + str(DeviceCount)
                else:
                    strPevStopEnabled = "PEVSTOPENABLE" + str(DeviceCount)
                    strPevStopReg = "PEVSTOPREG" + str(DeviceCount)
                    strPevStopVal = "PEVSTOPVAL" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevStopEnabled)) == "true"):
                    ExecuteEvent = True
                    ActionReg = str(__addon__.getSetting(strPevStopReg))
                    ActionValue = str(__addon__.getSetting(strPevStopVal))
            elif Type == "P_Pause":
                if (DeviceCount <= 9):
                    strPevPauseEnabled = "PEVPAUSEENABLE0" + str(DeviceCount)
                    strPevPauseReg = "PEVPAUSEREG0" + str(DeviceCount)
                    strPevPauseVal = "PEVPAUSEVAL0" + str(DeviceCount)
                else:
                    strPevPauseEnabled = "PEVPAUSEENABLE" + str(DeviceCount)
                    strPevPauseReg = "PEVPAUSEREG" + str(DeviceCount)
                    strPevPauseVal = "PEVPAUSEVAL" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevPauseEnabled)) == "true"):
                    ExecuteEvent = True
                    ActionReg = str(__addon__.getSetting(strPevPauseReg))
                    ActionValue = str(__addon__.getSetting(strPevPauseVal))
            elif Type == "P_End":
                if (DeviceCount <= 9):
                    strPevEndEnabled = "PEVENDENABLE0" + str(DeviceCount)
                    strPevEndReg = "PEVENDREG0" + str(DeviceCount)
                    strPevEndVal = "PEVENDVAL0" + str(DeviceCount)
                else:
                    strPevEndEnabled = "PEVENDENABLE" + str(DeviceCount)
                    strPevEndReg = "PEVENDREG" + str(DeviceCount)
                    strPevEndVal = "PEVENDVAL" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevEndEnabled)) == "true"):
                    ExecuteEvent = True
                    ActionReg = str(__addon__.getSetting(strPevEndReg))
                    ActionValue = str(__addon__.getSetting(strPevEndVal))
            elif Type == "P_Resume":
                if (DeviceCount <= 9):
                    strPevResumeEnabled = "PEVRESUMEENABLE0" + str(DeviceCount)
                    strPevResumeReg = "PEVRESUMEREG0" + str(DeviceCount)
                    strPevResumeVal = "PEVRESUMEVAL0" + str(DeviceCount)
                else:
                    strPevResumeEnabled = "PEVRESUMEENABLE" + str(DeviceCount)
                    strPevResumeReg = "PEVRESUMEREG" + str(DeviceCount)
                    strPevResumeVal = "PEVRESUMEVAL" + str(DeviceCount)
                #Execute Event if it is enabled for the Device
                if (str(__addon__.getSetting(strPevResumeEnabled)) == "true"):
                    ExecuteEvent = True
                    ActionReg = str(__addon__.getSetting(strPevResumeReg))
                    ActionValue = str(__addon__.getSetting(strPevResumeVal))
            #Call to Execute the action on the device
            if (ExecuteEvent):
                ActionCall = ModbusTCP(URL, ActionReg, ActionValue)
                if (debuging): 
                    xbmc.log('Modbus Commander: Event Register = ' + str(ActionReg))
                    xbmc.log('Modbus Commander: Event Value     = ' + str(ActionValue))
                    xbmc.log('Modbus Commander: *************************************************')
            else:
                ActionCall = "failed"
        
        DeviceCount = DeviceCount + 1
    return

# FUNCTIONS - LOGGING
if (debuging): 
    xbmc.log('Modbus Commander: ******************* Modbus Commander ******************')
    xbmc.log('Modbus Commander: Import of libraries is done')
    xbmc.log('Modbus Commander: functions are initialized')
    xbmc.log('Modbus Commander: *************************************************')

# FUNCTIONS - END

# ADDON DEVICE APPLICATION AND URL SETTING
# 'http://' + my_ip + ':' + my_port + '/tenHsServer/tenHsServer.aspx?t=xbmc&f=ExecX10&d=' + my_devid + '&a=ON'
# User:Pass@

# ADDON SHOW INFORMATION ABOUT ALL SETTINGS
if (debuging): 
    xbmc.log('Modbus Commander: *************** Addon Host settings *************')
    xbmc.log('Modbus Commander: IP number          : ' + str(__addon__.getSetting("IP")))
    xbmc.log('Modbus Commander: PORT number        : ' + str(__addon__.getSetting("PORT")))
    xbmc.log('Modbus Commander: *************************************************')
#    xbmc.log('Modbus Commander: Base URL: ' + DeviceURL)

# ADDON START
if (debuging): 
    xbmc.log('Modbus Commander: ******************** STARTUP ********************')
    xbmc.log('Modbus Commander: *************************************************')

#START XBMC START Event
if (debuging): xbmc.log('Modbus Commander: ****************** START EVENT ******************')

MainEventHandler("X_Start")

if (debuging): xbmc.log('Modbus Commander: *************************************************')
#END XBMC START Event

# ADDON PLAYER
if (debuging): xbmc.log('Modbus Commander: ****************** CLASS PLAYER *****************')
class MyPlayer(xbmc.Player) :
    if (debuging): xbmc.log('Modbus Commander: Class player is opened')
    
    def __init__ (self):
        xbmc.Player.__init__(self)
        if (debuging): xbmc.log('Modbus Commander: Class player is initialized')

    def onPlayBackStarted(self):
        if xbmc.Player().isPlayingVideo():
            MainEventHandler("P_Start")
            if (debuging): xbmc.log('Modbus Commander: PLAYBACK STARTED')

    def onPlayBackEnded(self):
        if (VIDEO == 1):
            MainEventHandler("P_End")
            if (debuging): xbmc.log('Modbus Commander: PLAYBACK ENDED')

    def onPlayBackStopped(self):
        if (VIDEO == 1):
            MainEventHandler("P_Stop")
            if (debuging): xbmc.log('Modbus Commander: PLAYBACK STOPPED')

    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            MainEventHandler("P_Pause")
            if (debuging): xbmc.log('Modbus Commander: PLAYBACK PAUSED')

    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            MainEventHandler("P_Resume")
            if (debuging): xbmc.log('Modbus Commander: PLAYBACK RESUMED')

player=MyPlayer()

while (not xbmc.abortRequested):
    if xbmc.Player().isPlayingVideo():
        VIDEO = 1
    else:
        VIDEO = 0

    xbmc.sleep(1000)

if (xbmc.abortRequested):
    #START XBMC STOP Event
    if (debuging): xbmc.log('Modbus Commander: ****************** STOP EVENT ******************')
    MainEventHandler("X_Stop")
    if (debuging): xbmc.log('Modbus Commander: *************************************************')
    #END XBMC STOP Event
    #Execute XBMC STOP Event settings on Device

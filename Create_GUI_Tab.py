'''
Project X

This file contains OOAD Project X GUI and its classes 

Instructor: Edwin Mach
Student: Andy Song
'''

#======================
# imports tkinter and other support packages
#======================
import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
from tkinter import ttk
from tkinter.messagebox import showinfo

import PIL.Image
import PIL.ImageTk
from win32com.client import Dispatch
from pprint import pprint 

from Utils import *
  
UVI_ENTRY_WIDTH = 12 
POLLUTION_ENTRY_WIDTH = 12
WEATHER_ENTRY_WIDTH = 25
TIME_ZONE_ADJUST = -28800
UNRECOGNIZED_CITY_USE_COORD_MSG = 'Unrecognized City, try again or use Coordinates below'
UNRECOGNIZED_CITY_MSG = 'Unrecognized City, try again'
UNRECOGNIZED_COORDINATES_MSG = 'Enter valid Coordinates'
NOT_SUPPORTED_MSG = 'Not supported by OWM(Beta) yet'
POLLURTION_BETA_MSG = 'Default Coord only'
POLLURTION_BETA_SPEAKER_MSG = 'Beta version supports Default Coordinates only'
INVALID_COORDINATES__MSG = 'Enter Valid Coordinates'


##########################
# TAB 1 OpenWeatherMap UVI
##########################

class ProjectXGui(tk.Tk):
    
    speaker = False
    windowsSpeak = Dispatch('SAPI.SpVoice')
    windowsSpeak.Rate = 1
    
    #======================
    # Instantiate a TK GUI instance
    #======================
    gui = tk.Tk()   
    
    #======================
    # callback function
    #======================
    def QuitGui(self):
        ''' This function is to exit GUI gracefully
        '''
        
        self.gui.quit()      
        self.gui.destroy()
        exit() 
    
    
    def ShowProject(self):
        ''' This function is to display Project X description 
        when 'about' button is clicked
        '''
        
        self.info = []
        with open('ProjectX.txt') as self.rfile:
            self.info = self.rfile.readlines()
        
        self.file = ' '.join(self.info)
            
        messagebox.showinfo('Project X - Open Weather Map', self.file) 
    
    
    def ShowHelp(self):
        ''' This function is to display Project X help text 
        when 'help' button is clicked
        '''
        self.info = []
        with open('Help.txt') as self.rfile:
            self.info = self.rfile.readlines()
            
        self.file = ' '.join(self.info)
            
        messagebox.showinfo('Help Menu', self.file) 
    
    
    def SpeakerOn(self):
        ''' This function is to turn on the speaker
        '''
        ProjectXGui.speaker = True
    
    
    def SpeakerOff(self):
        ''' This function is to turn off the speaker
        '''
        ProjectXGui.speaker = False

    
    def __init__(self):       
        
        # Add a title       
        self.gui.title("OOAD projectX")
        # ---------------------------------------------------------------
        # Creating a Menu Bar
        self.menuBar = Menu()
        self.gui.config(menu=self.menuBar)
        
        # Add menu items to exit GUI gracefully
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Speaker On", command=self.SpeakerOn)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Speaker Off", command=self.SpeakerOff)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.QuitGui)  
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        
        # Add help Menu to the Menu Bar 
        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="About", command=self.ShowProject)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="Help", command=self.ShowHelp)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        # ---------------------------------------------------------------
        
        # Tab Control - instantiate an object for each tab class
        self.tabControl = ttk.Notebook(self.gui)          # Create Tab Control
        
        self.tab1 = ttk.Frame(self.tabControl)            # Create a tab for UltraViolet Index
        self.tabControl.add(self.tab1, text='Ultraviolet Index')      
        
        self.tab2 = ttk.Frame(self.tabControl)            # Create a tab for Pollution
        self.tabControl.add(self.tab2, text='Pollution Data')       
        
        self.tab3 = ttk.Frame(self.tabControl)            # Create a tab for weather
        self.tabControl.add(self.tab3, text='Weather Report')       
        
        self.tab4 = ttk.Frame(self.tabControl)            # Create a tab for city coordinate
        self.tabControl.add(self.tab4, text='Get City Coordinate')       
        
        self.tab5 = ttk.Frame(self.tabControl)            # Create a tab for future use
        self.tabControl.add(self.tab5, text='Future Use')       
        self.tabControl.pack(expand=1, fill="both")  # Pack to make visible
        

##########################
# TAB 1 OpenWeatherMap UVI
##########################

class UviTab(ProjectXGui):
    def __init__(self, tab):
        ''' UviTab constructor
        '''
        
        # Creating a container frame to hold other widgets
        self.uviCityFrame = ttk.LabelFrame(tab, text=' Latest Ultraviolet Index for ')
        self.uviCityFrame.grid(column=0, row=0, padx=8, pady=4)
        
        self.uviCoordinatesFrame = ttk.LabelFrame(tab, text=' Coordinates and Ultraviolet Index at Noon ')
        self.uviCoordinatesFrame.grid(column=0, row=1, padx=8, pady=4)
        
        # ---------------------------------------------------------------
        # Adding a Label in uviCityFrame
        ttk.Label(self.uviCityFrame, text="City: ").grid(column=0, row=0)
         
        # ---------------------------------------------------------------
        self.uviCity = tk.StringVar()
        self.uviCityCombo = ttk.Combobox(self.uviCityFrame, width=16, textvariable=self.uviCity)       
        self.uviCityCombo['values'] = ('Saratoga, US', 'Los Angeles, US', 'London, UK', 'Paris, FR', 'Mumbai, IN', 'Beijing, CN')
        self.uviCityCombo.grid(column=1, row=0)
        self.uviCityCombo.current(0)                 # highlight first city
        
        # Creating a label for uviCityFrame to display message
        self.unknownCityMsg = tk.StringVar()
        ttk.Label(self.uviCityFrame, textvariable=self.unknownCityMsg, foreground='red').grid(column=0, row=1, columnspan=3)
        
        # Create a button to get city's UVI
        ttk.Button(self.uviCityFrame,text='Get UVI by City', command=self.GetCityUVI).grid(column=2, row=0)


        # uviCoordinatesFrame
        self.unknownCoordinatesMsg = tk.StringVar()
        ttk.Label(self.uviCoordinatesFrame, textvariable=self.unknownCoordinatesMsg, foreground='red').grid(column=0, row=0, sticky='W')
        
        # ---------------------------------------------------------------
        # Adding Labels in uviCoordinatesFrame
        ttk.Label(self.uviCoordinatesFrame, text="Latitude: ", foreground='blue').grid(column=0, row=1, sticky='E')
        self.latitude = tk.StringVar()
        self.latitudeEntry = ttk.Entry(self.uviCoordinatesFrame, width=UVI_ENTRY_WIDTH, textvariable=self.latitude, foreground='blue')
        self.latitudeEntry.grid(column=1, row=1, sticky='W')
        
        ttk.Label(self.uviCoordinatesFrame, text="Longitude: ", foreground='blue').grid(column=0, row=2, sticky='E') 
        self.longitude = tk.StringVar()
        self.longitudeEntry = ttk.Entry(self.uviCoordinatesFrame, width=UVI_ENTRY_WIDTH, textvariable=self.longitude, foreground='blue')
        self.longitudeEntry.grid(column=1, row=2, sticky='W')
        
        ttk.Label(self.uviCoordinatesFrame, text="Date: ").grid(column=0, row=4, sticky='E') 
        self.uviDate = tk.StringVar()
        self.uviDateEntry = ttk.Entry(self.uviCoordinatesFrame, width=UVI_ENTRY_WIDTH+8, textvariable=self.uviDate, state='readonly')
        self.uviDateEntry.grid(column=1, row=4, sticky='W')
        
        ttk.Label(self.uviCoordinatesFrame, text="Ultraviolet Index: ", foreground='green').grid(column=0, row=5, sticky='E') 
        self.uviValue = tk.StringVar()
        self.uviValueEntry = ttk.Entry(self.uviCoordinatesFrame, width=UVI_ENTRY_WIDTH-5, textvariable=self.uviValue, foreground='green', state='readonly')
        self.uviValueEntry.grid(column=1, row=5, sticky='W')
         
        # Add some space around each widget
        for self.child in self.uviCoordinatesFrame.winfo_children(): 
                self.child.grid_configure(padx=2, pady=4)    
        
        
        ttk.Button(self.uviCoordinatesFrame,text='Get UVI by Coordinates', command=self.GetCoordinatesUvi).grid(column=1, row=0)

    # ---------------------------------------------------------------
    # callback function
    def GetCityUVI(self):
        ''' Get city name from the frame combo box, gets the corresponding 
        Coordinates and send inquiry request to Open Weather Map web server
        to get Ultraviolet Index and then updates the relevant fields
        
        input: city name from the frame
        output: update Coordinates, Date and Ultraviolet index fields in Frame
        '''
        
        self.uviCity = self.uviCityCombo.get()
        
        try:
            self.coordinates = Coordinates()
            self.location = self.coordinates.GetCoordinatesOfCity(self.uviCity)
            self.unknownCityMsg.set('')
            self.unknownCoordinatesMsg.set('')
            
        except:
            self.unknownCoordinatesMsg.set('')
            self.unknownCityMsg.set(UNRECOGNIZED_CITY_USE_COORD_MSG)
            
            if ProjectXGui.speaker == True:
                ProjectXGui.windowsSpeak.Speak(UNRECOGNIZED_CITY_USE_COORD_MSG)
                
            self.latitude.set('')
            self.longitude.set('')
            self.uviDate.set('')
            self.uviValue.set('')
    
        else:
            self.owmUvi = OpenWeatherMapUVI()
            self.uviData = self.owmUvi.GetOpenWeatherMapUVI(self.location)
            
            if ProjectXGui.speaker == True:
                ProjectXGui.windowsSpeak.Speak(self.uviCity)
                
            self.uviCityCombo.set(self.uviCity)
            self.__DisplayUvi(self.uviData)
   
    
    # ---------------------------------------------------------------
    # callback function
    def GetCoordinatesUvi(self):
        ''' Get Coordinates from combo box, then send inquiry request to 
        Open Weather Map web server to get Ultraviolet Index and then 
        updates the relevant fields
        
        input: Coordinates from the frame
        output: updates Date and Ultraviolet index fields in Frame
        '''
        
        try:
            self.lat = float(self.latitudeEntry.get())
            self.lon = float(self.longitudeEntry.get())
            self.loc = {"latitude" : self.lat, "longitude" : self.lon}
            self.unknownCityMsg.set('')
            self.unknownCoordinatesMsg.set('')
            self.uviCityCombo.set('')
            self.owmUvi = OpenWeatherMapUVI()
            self.uviData = self.owmUvi.GetOpenWeatherMapUVI(self.loc)
    
        except:
            self.unknownCityMsg.set('')
            self.unknownCoordinatesMsg.set(UNRECOGNIZED_COORDINATES_MSG)
            
            if ProjectXGui.speaker == True:
                ProjectXGui.windowsSpeak.Speak(UNRECOGNIZED_COORDINATES_MSG)
    
        else:
            if ProjectXGui.speaker == True:
                ProjectXGui.windowsSpeak.Speak(self.loc)
                
            self.__DisplayUvi(self.uviData)
            
    
    # ---------------------------------------------------------------
    # Display UVI data on GUI
    def __DisplayUvi(self, uviData):
        ''' Fill Ultraviolet Index data in corresponding fields in thge frame
        and announce 
        '''
        
        self.latitude.set(uviData['lat'])
        self.longitude.set(uviData['lon'])
        self.uviDate.set(uviData['date_iso'])
        self.uviValue.set(uviData['value'])
        
        if ProjectXGui.speaker == True:
            ProjectXGui.windowsSpeak.Speak('Ultraviolet index is ' + str(uviData['value']))

        
################################
# TAB 2 OpenWeatherMap Pollution
################################
class PollutionTab(ProjectXGui):
    def __init__(self, tab):
        ''' PollutionTab constructor
        '''
        
        # Creating a container frame to hold other widgets
        self.pollutionCityFrame = ttk.LabelFrame(tab, text=' Latest Pollution Data for ')
        self.pollutionCityFrame.grid(column=0, row=0, padx=8, pady=4)
        
        self.pollutionCoordinatesFrame = ttk.LabelFrame(tab, text=' Coordinates and Pollution Data (OWM Beta Version) ')
        self.pollutionCoordinatesFrame.grid(column=0, row=1, padx=8, pady=4)
        
        # ---------------------------------------------------------------
        # Adding a Label in pollutionCityFrame
        ttk.Label(self.pollutionCityFrame, text="City: ").grid(column=0, row=0)
         
        # ---------------------------------------------------------------
        self.pollutionCity = tk.StringVar()
        self.pollutionCityCombo = ttk.Combobox(self.pollutionCityFrame, width=16, textvariable=self.pollutionCity)       
        self.pollutionCityCombo['values'] = ('Saratoga, US', 'Los Angeles, US', 'London, UK', 'Paris, FR', 'Mumbai, IN', 'Beijing, CN')
        self.pollutionCityCombo.grid(column=1, row=0)
        self.pollutionCityCombo.current(0)                 # highlight first city
        
        # Creating a label for pollutionCityFrame to display message
        self.unknownCityMsg = tk.StringVar()
        ttk.Label(self.pollutionCityFrame, textvariable=self.unknownCityMsg, foreground='red').grid(column=0, row=1, columnspan=3)
        
        # Create a button to get city's pollution
        ttk.Button(self.pollutionCityFrame,text='Get pollution by City', command=self.GetCityPollution).grid(column=2, row=0)


        # pollutionCoordinates frame
        self.unknownCoordinatesMsg = tk.StringVar()
        ttk.Label(self.pollutionCoordinatesFrame, textvariable=self.unknownCoordinatesMsg, foreground='red').grid(column=2, row=0, sticky='W')
        
        # ---------------------------------------------------------------
        # Adding Labels in pollutionCoordinatesFrame
        ttk.Label(self.pollutionCoordinatesFrame, text="Latitude, Longitude:", foreground='blue').grid(column=0, row=1, sticky='E')
        self.latitude = tk.StringVar()
        self.latitudeCombo = ttk.Combobox(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.latitude, foreground='blue')
        self.latitudeCombo['value'] = (0.0)
        self.latitudeCombo.grid(column=1, row=1, sticky='W')
        self.latitudeCombo.current(0)        # default for OWM Beta version                
        
        self.longitude = tk.StringVar()
        self.longitudeCombo = ttk.Combobox(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.longitude, foreground='blue')
        self.longitudeCombo['value'] = (10.0)
        self.longitudeCombo.grid(column=2, row=1, sticky='W')
        self.longitudeCombo.current(0)        # default for OWM Beta version                
        
        ttk.Label(self.pollutionCoordinatesFrame, text="Date:").grid(column=0, row=4, sticky='E') 
        self.pollutionDate = tk.StringVar()
        self.pollutionDateEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH+6, textvariable=self.pollutionDate, state='readonly')
        self.pollutionDateEntry.grid(column=1, row=4, sticky='W')
        
        ttk.Label(self.pollutionCoordinatesFrame, text="Ozone Thickness (DU):", foreground='green').grid(column=0, row=5, sticky='E') 
        self.pollutionOzone = tk.StringVar()
        self.pollutionOzoneEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH-5, textvariable=self.pollutionOzone, foreground='green', state='readonly')
        self.pollutionOzoneEntry.grid(column=1, row=5, sticky='W')

        ttk.Label(self.pollutionCoordinatesFrame, text="Precision", foreground='green').grid(column=1, row=6, sticky='W') 
        ttk.Label(self.pollutionCoordinatesFrame, text="Pressure", foreground='green').grid(column=2, row=6, sticky='W') 
        ttk.Label(self.pollutionCoordinatesFrame, text="Value", foreground='green').grid(column=3, row=6, sticky='W') 

        ttk.Label(self.pollutionCoordinatesFrame, text="Carbon Monoxide:", foreground='green').grid(column=0, row=7, sticky='E') 
        self.pollutionCoPrec = tk.StringVar()
        self.pollutionCoPrecEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionCoPrec, foreground='green', state='readonly')
        self.pollutionCoPrecEntry.grid(column=1, row=7, sticky='W')
        self.pollutionCoPres = tk.StringVar()
        self.pollutionCoPresEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionCoPres, foreground='green', state='readonly')
        self.pollutionCoPresEntry.grid(column=2, row=7, sticky='W')
        self.pollutionCoValue = tk.StringVar()
        self.pollutionCoValueEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionCoValue, foreground='green', state='readonly')
        self.pollutionCoValueEntry.grid(column=3, row=7, sticky='W')

        ttk.Label(self.pollutionCoordinatesFrame, text="Nitrogen Dioxide:", foreground='green').grid(column=0, row=8, sticky='E') 
        self.pollutionNo2Prec = tk.StringVar()
        self.pollutionNo2PrecEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionNo2Prec, foreground='green', state='readonly')
        self.pollutionNo2PrecEntry.grid(column=1, row=8, sticky='W')
        self.pollutionNo2Pres = tk.StringVar()
        self.pollutionNo2PresEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionNo2Pres, foreground='green', state='readonly')
        self.pollutionNo2PresEntry.grid(column=2, row=8, sticky='W')
        self.pollutionNo2Value = tk.StringVar()
        self.pollutionNo2ValueEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionNo2Value, foreground='green', state='readonly')
        self.pollutionNo2ValueEntry.grid(column=3, row=8, sticky='W')

        ttk.Label(self.pollutionCoordinatesFrame, text="Sulfur Dioxide:", foreground='green').grid(column=0, row=9, sticky='E') 
        self.pollutionSo2Prec = tk.StringVar()
        self.pollutionSo2PrecEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionSo2Prec, foreground='green', state='readonly')
        self.pollutionSo2PrecEntry.grid(column=1, row=9, sticky='W')
        self.pollutionSo2Pres = tk.StringVar()
        self.pollutionSo2PresEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionSo2Pres, foreground='green', state='readonly')
        self.pollutionSo2PresEntry.grid(column=2, row=9, sticky='W')
        self.pollutionSo2Value = tk.StringVar()
        self.pollutionSo2ValueEntry = ttk.Entry(self.pollutionCoordinatesFrame, width=POLLUTION_ENTRY_WIDTH, textvariable=self.pollutionSo2Value, foreground='green', state='readonly')
        self.pollutionSo2ValueEntry.grid(column=3, row=9, sticky='W')

        # Add some space around each widget
        for self.child in self.pollutionCoordinatesFrame.winfo_children(): 
                self.child.grid_configure(padx=1, pady=2)    
       
        ttk.Button(self.pollutionCoordinatesFrame,text='Get pollution by Coord', command=self.GetCoordinatesPollution).grid(column=0, row=0)
        self.pollutionBetaVersionMsg = tk.StringVar()
        ttk.Label(self.pollutionCoordinatesFrame, textvariable=self.pollutionBetaVersionMsg, foreground='red').grid(column=1, row=0, columnspan=1, sticky='W')
        self.pollutionBetaVersionMsg.set(POLLURTION_BETA_MSG)

    # ---------------------------------------------------------------
    # callback function
    def GetCityPollution(self):
        ''' Get pollution data for a city is not supported in Open Weather Map
        site's beta version.
        Output: Display not supported message in Frame
        '''
        
        self.pollutionCity = self.pollutionCityCombo.get()
        self.unknownCityMsg.set(NOT_SUPPORTED_MSG)
        
        if ProjectXGui.speaker == True:
            ProjectXGui.windowsSpeak.Speak(NOT_SUPPORTED_MSG)
        
    
    # ---------------------------------------------------------------
    # callback function
    def GetCoordinatesPollution(self):
        ''' Get pollution data of a Coordinate location from Open Weather Map
        site's beta version.
        Pollution data includes Ozon thickness, Carbon Monoxide, Nitrogen Dioxide,
        Sulfur Dioxide's precision and value at 1000 hpa
        
        Input: Coordinates from the Frame
        Output: Display pollution data of the Coordinates location in Frame
        '''
        
        try:
            self.lat = float(self.latitudeCombo.get())
            self.lon = float(self.longitudeCombo.get())
            self.loc = {"latitude" : self.lat, "longitude" : self.lon}
            self.unknownCityMsg.set('')
            self.unknownCoordinatesMsg.set('')
            self.pollutionCityCombo.set('')
            self.owmOzone = OpenWeatherMapPollution()
            self.ozoneData = self.owmOzone.GetOpenWeatherMapPollution(self.loc, TYPE_OZONE)
            self.coData = self.owmOzone.GetOpenWeatherMapPollution(self.loc, TYPE_CO)
            self.no2Data = self.owmOzone.GetOpenWeatherMapPollution(self.loc, TYPE_NO2)
            self.so2Data = self.owmOzone.GetOpenWeatherMapPollution(self.loc, TYPE_SO2)
            self.__DisplayPollution(self.ozoneData, self.coData, self.no2Data, self.so2Data)
    
        except:
            self.unknownCityMsg.set('')
            self.unknownCoordinatesMsg.set(INVALID_COORDINATES__MSG)
            
            self.latitude.set('')
            self.longitude.set('')
            self.pollutionDate.set('')
            self.pollutionOzone.set('')
            self.pollutionCoPrec.set('')
            self.pollutionCoPres.set('')
            self.pollutionCoValue.set('')
            self.pollutionSo2Prec.set('')
            self.pollutionSo2Pres.set('')
            self.pollutionSo2Value.set('')
            self.pollutionNo2Prec.set('')
            self.pollutionNo2Pres.set('')
            self.pollutionNo2Value.set('')

            if ProjectXGui.speaker == True:
                ProjectXGui.windowsSpeak.Speak(INVALID_COORDINATES__MSG)
                ProjectXGui.windowsSpeak.Speak(POLLURTION_BETA_SPEAKER_MSG)
    
            
    # ---------------------------------------------------------------
    # Display Pollution data on GUI
    #    NO2 is not working,, leave it empty
    def __DisplayPollution(self, ozoneData, coData, no2Data, so2Data):
        ''' Display Ozon thickness, Carbon Monoxide, Nitrogen Dioxide,
        Sulfur Dioxide's precision, value and pressure (1000 hpa) in 
        corresponding fields of the Frame.
        
        Input: ozoneData, coData, no2Data and so2Data
        Output: ozoneData, coData, no2Data and so2Data in the Frame
        '''
        
        self.latitude.set(ozoneData['location']['latitude'])
        self.longitude.set(ozoneData['location']['longitude'])
        self.pollutionDate.set(ozoneData['time'])
        self.pollutionOzone.set(ozoneData['data'])
        
        self.pollutionCoPrec.set(coData['data'][0]['precision'])
        self.pollutionCoPres.set(coData['data'][0]['pressure'])
        self.pollutionCoValue.set(coData['data'][0]['value'])

        self.pollutionSo2Prec.set(so2Data['data'][0]['precision'])
        self.pollutionSo2Pres.set(so2Data['data'][0]['pressure'])
        self.pollutionSo2Value.set(so2Data['data'][0]['value'])
        
        self.pollutionNo2Prec.set(no2Data['data'][0]['precision'])
        self.pollutionNo2Pres.set(no2Data['data'][0]['pressure'])
        self.pollutionNo2Value.set(no2Data['data'][0]['value'])

 #==============================================================================
 #        if ProjectXGui.speaker == True:
 #            ProjectXGui.windowsSpeak.Speak(ozoneData['location'])
 #            ProjectXGui.windowsSpeak.Speak('Ozone thickness' + str(ozoneData['data']) + 'DU')
 # 
 #            ProjectXGui.windowsSpeak.Speak('Carbon Monoxide precision' + str(self.pollutionCoPrec.get()))
 #            ProjectXGui.windowsSpeak.Speak('pressure ' + str(self.pollutionCoPres.get()))
 #            ProjectXGui.windowsSpeak.Speak('value' + str(self.pollutionCoValue.get()))
 # 
 #            ProjectXGui.windowsSpeak.Speak('Nitrogen Dioxide precision' + str(self.pollutionNo2Prec.get()))
 #            ProjectXGui.windowsSpeak.Speak('pressure ' + str(self.pollutionNo2Pres.get()))
 #            ProjectXGui.windowsSpeak.Speak('value' + str(self.pollutionNo2Value.get()))
 # 
 #            ProjectXGui.windowsSpeak.Speak('Sulfur Dioxide precision' + str(self.pollutionSo2Prec.get()))
 #            ProjectXGui.windowsSpeak.Speak('pressure ' + str(self.pollutionSo2Pres.get()))
 #            ProjectXGui.windowsSpeak.Speak('value' + str(self.pollutionSo2Value.get()))
 #==============================================================================


##########################
# TAB 3 Weather Report
##########################

class WeatherTab(ProjectXGui):
    def __init__(self, tab):
        ''' WeatherTab constructor
        '''
        
        # Creating a container frame to hold other widgets
        self.weatherCityFrame = ttk.LabelFrame(tab, text=' Weather For ')
        self.weatherCityFrame.grid(column=0, row=0, padx=8, pady=4)
        
        # ---------------------------------------------------------------
        # Adding a Label in weatherCityFrame
        ttk.Label(self.weatherCityFrame, text="City: ").grid(column=0, row=0, sticky='E')
         
        # ---------------------------------------------------------------
        self.weatherCity = tk.StringVar()
        self.weatherCityCombo = ttk.Combobox(self.weatherCityFrame, width=16, textvariable=self.weatherCity)       
        self.weatherCityCombo['values'] = ('Saratoga, US', 'Los Angeles, US', 'New York, US', 'London, UK', 'Munich, DE', 'Zermatt, CH',\
                                           'Lausanne, CH','Paris, FR', 'Mumbai, IN', 'Beijing, CN', 'Taipei, TW', 'Tokyo, JP', 'Seoul, KR')
        self.weatherCityCombo.grid(column=1, row=0, sticky='W')
        self.weatherCityCombo.current(0)                 # highlight first city
        
        # Creating a label for weatherCityFrame to display message
        self.unknownCityMsg = tk.StringVar()
        ttk.Label(self.weatherCityFrame, textvariable=self.unknownCityMsg, foreground='red').grid(column=0, row=1, columnspan=3)
        
        # Create a button to get city's weather
        ttk.Button(self.weatherCityFrame,text=' Get Weather ', command=self.GetCityWeather).grid(column=2, row=0)

        # Add some space around each widget
        for self.child in self.weatherCityFrame.winfo_children(): 
                self.child.grid_configure(padx=2, pady=4)    

        # ---------------------------------------------------------------
        # Creating a container frame to hold all other widgets
        self.weatherConditionsFrame = ttk.LabelFrame(tab, text=' Current Weather Conditions ')
        self.weatherConditionsFrame.grid(column=0, row=1, padx=8, pady=4)
        
        # Adding Label & Textbox Entry widgets
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Last Observed:").grid(column=0, row=1, sticky='E')         # <== right-align
        self.updated = tk.StringVar()
        self.updatedEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.updated, state='readonly')
        self.updatedEntry.grid(column=1, row=1, sticky='W')
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Weather:").grid(column=0, row=2, sticky='E')               # <== increment row for each
        self.weather = tk.StringVar()
        self.weatherEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.weather, state='readonly')
        self.weatherEntry.grid(column=1, row=2, sticky='W')                                  # <== increment row for each
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Temperature:").grid(column=0, row=3, sticky='E')
        self.temp = tk.StringVar()
        self.tempEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.temp, state='readonly')
        self.tempEntry.grid(column=1, row=3, sticky='W')
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Humidity:").grid(column=0, row=4, sticky='E')
        self.relHumi = tk.StringVar()
        self.relHumiEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.relHumi, state='readonly')
        self.relHumiEntry.grid(column=1, row=4, sticky='W')
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Wind:").grid(column=0, row=5, sticky='E')
        self.wind = tk.StringVar()
        self.windEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.wind, state='readonly')
        self.windEntry.grid(column=1, row=5, sticky='W')
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Visibility:").grid(column=0, row=6, sticky='E')
        self.visi = tk.StringVar()
        self.visiEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.visi, state='readonly')
        self.visiEntry.grid(column=1, row=6, sticky='W')
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Pressure:").grid(column=0, row=7, sticky='E')
        self.msl = tk.StringVar()
        self.mslEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.msl, state='readonly')
        self.mslEntry.grid(column=1, row=7, sticky='W')
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Sunrise:").grid(column=0, row=8, sticky='E')
        self.sunrise = tk.StringVar()
        self.sunriseEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.sunrise, state='readonly')
        self.sunriseEntry.grid(column=1, row=8, sticky='E')
        #---------------------------------------------
        ttk.Label(self.weatherConditionsFrame, text="Sunset:").grid(column=0, row=9, sticky='E')
        self.sunset = tk.StringVar()
        self.sunsetEntry = ttk.Entry(self.weatherConditionsFrame, width=WEATHER_ENTRY_WIDTH, textvariable=self.sunset, state='readonly')
        self.sunsetEntry.grid(column=1, row=9, sticky='E')
        #---------------------------------------------
        
        # Add some space around each widget
        for child in self.weatherConditionsFrame.winfo_children(): 
                child.grid_configure(padx=4, pady=2)    



    # ---------------------------------------------------------------
    # callback function
    def GetCityWeather(self):
        ''' Get city name from the frame combo box, then send inquiry request 
        to Open Weather Map web server to get weather data then updates the 
        relevant fields in the Frame.
        Weather data includes Last Observation date, weather, temperature, 
        humidity, wind, visibility, pressure, sunrise and sunset time
        
        input: city name from the frame
        output: update corresponding weather data fields in Frame
        '''
        
        self.weatherCity = self.weatherCityCombo.get()
        try:
            self.openWeatherMapWeather = OpenWeatherMapWeather()
            self.weatherData, self.ico = self.openWeatherMapWeather.GetOpenWeatherMapWeather(self.weatherCity)
            self.unknownCityMsg.set('')
            
        except:
            self.unknownCityMsg.set(UNRECOGNIZED_CITY_MSG)
            
            if ProjectXGui.speaker == True:
                ProjectXGui.windowsSpeak.Speak(UNRECOGNIZED_CITY_MSG)
    
        else:
            self.weatherCityCombo.set(self.weatherCity)
            self.__DisplayWeatherData(self.weatherData, self.ico)
        
    
    # ---------------------------------------------------------------
    # Display UVI data on GUI
    def __DisplayWeatherData(self, weatherData, ico):
        ''' Display Last Observation date, weather, temperature, humidity, 
        wind, visibility, pressure, sunrise, sunset time and weather icon
        
        Input: weather data, weather icon
        Output: update weather data fields in the Frame and show weather icon
        '''
  
        self.utils = Utils()
        
        self.latLong = weatherData['coord']
        self.cityId = weatherData['id']
        self.cityName = weatherData['name']
        self.cityCountry = weatherData['sys']['country']
        
        self.lastupdateUnix = weatherData['dt']
        self.humidity = weatherData['main']['humidity']
        self.pressure = weatherData['main']['pressure']
        self.tempKelvin = weatherData['main']['temp']
        self.sunriseUnix = weatherData['sys']['sunrise']
        self.sunsetUnix = weatherData['sys']['sunset']
        self.timezone = weatherData['timezone']
        
        try: self.visibilityMeter = weatherData['visibility']
        except: self.visibilityMeter = 'N/A'
        
        self.owmWeather = weatherData['weather'][0]['description']
        
        try: self.windDeg = weatherData['wind']['deg']
        except: self.windDeg = ' ? '
        
        self.windSpeedMeterSec = weatherData['wind']['speed']
            
        if self.visibilityMeter is 'N/A':
            self.visibilityMiles = 'N/A'
        else:
            self.visibilityMiles = self.utils.MeterToMiles(self.visibilityMeter)
    
        # -------------------------------------------------------
        # Update GUI entry widgets with live data
        #open_location.set('{}, {}'.format(city_name, city_country))

        # All the timestamps are unix epoch time and seems like it's the local time of
        # time zone of -28800 sec. therefore, adjust it to target city's local time
        self.lastupdate = self.utils.UnixToDatetime(self.lastupdateUnix - (TIME_ZONE_ADJUST - self.timezone))
        self.updated.set(self.lastupdate)
        self.weather.set(self.owmWeather)
        self.tempFahr = self.utils.KelvinToFahrenheit(self.tempKelvin)
        self.tempCels = self.utils.KelvinToCelsius(self.tempKelvin)
        self.temp.set('{} \xb0F  ({} \xb0C)'.format(self.tempFahr, self.tempCels))
        self.relHumi.set('{} %'.format(self.humidity))
        self.windSpeedMph = self.utils.MpsToMph(self.windSpeedMeterSec)
        self.wind.set('{} degrees at {} MPH'.format(self.windDeg, self.windSpeedMph))
        self.visi.set('{} miles'.format(self.visibilityMiles))
        self.msl.set('{} hPa'.format(self.pressure))
        
        self.sunriseDt = self.utils.UnixToDatetime(self.sunriseUnix - (TIME_ZONE_ADJUST - self.timezone))
        self.sunrise.set(self.sunriseDt)
        self.sunsetDt = self.utils.UnixToDatetime(self.sunsetUnix - (TIME_ZONE_ADJUST - self.timezone))
        self.sunset.set(self.sunsetDt)
        
        self.openIm = PIL.Image.open(ico)
        self.openPhoto = PIL.ImageTk.PhotoImage(self.openIm)
         
        ttk.Label(self.weatherCityFrame, image=self.openPhoto).grid(column=0, row=1) 
        ttk.Label.image=self.openPhoto
        
        if ProjectXGui.speaker == True:
            ProjectXGui.windowsSpeak.Speak(self.cityName)
            ProjectXGui.windowsSpeak.Speak(self.cityCountry)
            ProjectXGui.windowsSpeak.Speak('weather' + self.owmWeather)
            ProjectXGui.windowsSpeak.Speak('temperature' + self.tempFahr + 'Fahrenheit')
            ProjectXGui.windowsSpeak.Speak('humidity' + str(self.humidity) + '%')
            ProjectXGui.windowsSpeak.Speak('wind direction' + str(self.windDeg) + 'degree')
            ProjectXGui.windowsSpeak.Speak('at' + self.windSpeedMph + 'mile per hour')
            ProjectXGui.windowsSpeak.Speak('visibility' + self.visibilityMiles + 'miles')


##########################
# TAB 4 Coordinates
##########################

class CoordinatesTab(ProjectXGui):
    ''' CoordinatesTab constructor
    '''
    
    def __init__(self, tab):
        # Creating a container frame to hold other widgets
        self.coordinatesCityFrame = ttk.LabelFrame(tab, text=' Get Coordinates of City ', width=380, height=300)
        self.coordinatesCityFrame.grid(column=0, row=0, padx=8, pady=4)
        self.coordinatesCityFrame.grid_propagate(0)
        
        # ---------------------------------------------------------------
        # Adding a Label in coordinatesCityFrame
        ttk.Label(self.coordinatesCityFrame, text="City: ").grid(column=0, row=1, sticky='E')
         
        # ---------------------------------------------------------------
        self.coordinatesCity = tk.StringVar()
        self.coordinatesCityCombo = ttk.Combobox(self.coordinatesCityFrame, width=16, textvariable=self.coordinatesCity)       
        self.coordinatesCityCombo['values'] = ('Saratoga, US', 'Los Angeles, US', 'London, UK', 'Paris, FR', 'Mumbai, IN', 'Beijing, CN')
        self.coordinatesCityCombo.grid(column=1, row=1, sticky='W')
        self.coordinatesCityCombo.current(0)                 # highlight first city
        
        # Creating a label for coordinatesCityFrame to display message
        self.unknownCityMsg = tk.StringVar()
        ttk.Label(self.coordinatesCityFrame, textvariable=self.unknownCityMsg, foreground='red').grid(column=3, row=1, columnspan=3)
        
        # Create a button to get city's UVI
        ttk.Button(self.coordinatesCityFrame,text='Get Coordinates of City', command=self.GetCityCoordinates).grid(column=1, row=0)

        # Adding Labels in uviCoordinatesFrame
        ttk.Label(self.coordinatesCityFrame, text="Latitude: ", foreground='blue').grid(column=0, row=2, sticky='E')
        self.latitude = tk.StringVar()
        self.latitudeEntry = ttk.Entry(self.coordinatesCityFrame, width=UVI_ENTRY_WIDTH, textvariable=self.latitude, foreground='blue')
        self.latitudeEntry.grid(column=1, row=2, sticky='W')
        
        ttk.Label(self.coordinatesCityFrame, text="Longitude: ", foreground='blue').grid(column=0, row=3, sticky='E') 
        self.longitude = tk.StringVar()
        self.longitudeEntry = ttk.Entry(self.coordinatesCityFrame, width=UVI_ENTRY_WIDTH, textvariable=self.longitude, foreground='blue')
        self.longitudeEntry.grid(column=1, row=3, sticky='W')

        # Add some space around each widget
        for self.child in self.coordinatesCityFrame.winfo_children(): 
                self.child.grid_configure(padx=2, pady=4)    
        
    # ---------------------------------------------------------------
    # callback function
    def GetCityCoordinates(self):
        ''' Get city name from the frame combo box then gets the Coordinates 
        and updates Coordinates fields in the Frame
        
        input: city name from the frame
        output: update Coordinates fields in Frame
        '''
        
        self.coordinateCity = self.coordinatesCityCombo.get()
        try:
            self.coordinates = Coordinates()
            self.location = self.coordinates.GetCoordinatesOfCity(self.coordinateCity)
            self.unknownCityMsg.set('')
            
        except:
            self.unknownCityMsg.set('Unrecognized City, try again.')
            self.latitude.set('')
            self.longitude.set('')
    
        else:
            self.latitude.set(self.location['latitude'])
            self.longitude.set(self.location['longitude'])
            
            if ProjectXGui.speaker == True:
                ProjectXGui.windowsSpeak.Speak(self.coordinateCity)
                ProjectXGui.windowsSpeak.Speak(self.location)
        

##########################
# TAB 5 Coordinates
##########################

class FutureProposalTab(ProjectXGui):
    def __init__(self, tab):
        ''' FutureProposalTab constructor
        '''
        
        # Creating a container frame to hold other widgets
        self.futureProposalFrame = ttk.LabelFrame(tab, text=' For Future Proposal ', width=380, height=300)
        self.futureProposalFrame.grid(column=0, row=0, padx=8, pady=4)
        self.futureProposalFrame.grid_propagate(0)
        
        # ---------------------------------------------------------------
        # Adding a Label in futureProposalFrame
        ttk.Label(self.futureProposalFrame, text="Future Proposal: ").grid(column=0, row=1, sticky='E')
         

#======================
# Start GUI
#======================
def run():
    
    projectXGui = ProjectXGui()
    uviTab = UviTab(projectXGui.tab1)
    pollutionTab = PollutionTab(projectXGui.tab2)
    weatherTab = WeatherTab(projectXGui.tab3)
    coordinatesTab = CoordinatesTab(projectXGui.tab4)
    futureProposalTab = FutureProposalTab(projectXGui.tab5)
    projectXGui.gui.mainloop()


if __name__ == "__main__":
    run()



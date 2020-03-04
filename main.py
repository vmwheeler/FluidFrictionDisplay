import kivy

kivy.require('1.11.1')
#print(kivy.__version__)

from kivy.app import App
from kivy.core.window import Window
Window.fullscreen = 'auto'
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
)
import os
import numpy as np
from screeninfo import get_monitors
displayinfo = get_monitors()[0]
displaywh = (displayinfo.width,displayinfo.height)
from daqhats import hat_list, HatIDs, mcc118

print(os.path.dirname(kivy.__file__))
#moop

def MakeDataPresentable(numin,trim=True):
    if trim:
        return "{:.3f}".format(numin).rstrip('0')
    else:
        return "{:.3f}".format(numin)


def CheckDAQBoard():
    
    # get hat list of MCC daqhat boards
    board_list = hat_list(filter_by_id = HatIDs.ANY)
    if not board_list:
        print("No boards found")
        sys.exit()
    for entry in board_list: 
        if entry.id == HatIDs.MCC_118:
            print("Board {}: MCC 118".format(entry.address))
            board = mcc118(entry.address)
    return board

class PressureSensor(Widget):
    psi_per_kpa = 1./6.89476
    
    data = StringProperty(10)
    
    def __init__(self, **kwargs):
        self.channel = kwargs.pop('channel')
        self.board = kwargs.pop('board')
        print("\n***\ninitializing pressure sensor on channel " + str(self.channel) + "\n***\n")
        
        super(PressureSensor, self).__init__(**kwargs)
        self.numdat = 0
        
        #self.error = 1.20676 # kPa
        self.error = 1.2 # kPa
        #print(self.numdat*self.psi_per_kpa)
        

    def pull(self):
        
        #self.numdat = 10 + np.random.randn()
        rawv = self.board.a_in_read(self.channel)
        self.numdat = self.v_to_p(rawv)
        self.data = MakeDataPresentable(self.numdat,trim=False)
        #self.error = 1.20676 # kPa
        self.error = 1.2 # kPa
        # print(self.numdat*self.psi_per_kpa)
        
    def v_to_p(self,v):
        return 43.0985*(v-2.)


class FrictionDisplay(Widget):

    #thefig = ObjectProperty(None)
    ps1 = ObjectProperty(PressureSensor(channel='None',board='None'))
    ps2 = ObjectProperty(PressureSensor(channel='None',board='None'))

    bgcol = ListProperty((0.6,0,0,1))
    
    tcol = ListProperty((1,1,1,1))
    pcol = ListProperty((0.2,0.2,0.2,1))
    
    pdiff = StringProperty('0')
    errordiff = StringProperty(u'\u221E')
    font_size = NumericProperty(72)

    def __init__(self, **kwargs):
        self.channels = kwargs.pop('channel_nums')
        self.board = kwargs.pop('board')
        super(FrictionDisplay, self).__init__(**kwargs)
        #self.thefig = RealTimeFigure()
        self.bggo = (0,0.4,0,1)
        self.bgstop = (0.6,0,0,1)
        self.ps1.channel = self.channels[0]
        self.ps2.channel = self.channels[1]
        self.ps1.board = self.board
        self.ps2.board = self.board
        #print('\n\n\n\n******')
        #print(self.thefig)
        #print('******\n\n\n\n')


    def update(self,dt):
        
        self.ps1.pull()
        #print(self.ps1.channel)
        self.ps2.pull()
        #print(self.ps2.channel)
        numdiff = abs(self.ps1.numdat - self.ps2.numdat)
        self.pdiff = MakeDataPresentable(numdiff,trim=False)
        numerror = np.sqrt(self.ps1.error**2 + self.ps2.error**2)
        self.errordiff = MakeDataPresentable(round(numerror,2))
        
        #self.thefig.redraw()
        if numdiff>numerror:
            self.bgcol = self.bggo
        else:
            self.bgcol = self.bgstop

class FrictionTrainerApp(App):

    def build(self):

        #hack for my old macbook laptop
        #Window.size = displaywh
        board = CheckDAQBoard()
        
        channelnums = [0,3]
        display = FrictionDisplay(channel_nums=channelnums,board=board)
        Clock.schedule_interval(display.update, 20.0/60.0)
        return display


if __name__ == '__main__':
    
    FrictionTrainerApp().run()

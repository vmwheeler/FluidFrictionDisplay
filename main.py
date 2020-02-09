import kivy

kivy.require('1.11.1')
#print(kivy.__version__)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty, ListProperty
)
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
import matplotlib.pyplot as plt
import numpy as np
import os

#print(os.path.dirname(kivy.__file__))
#moop

def MakeDataPresentable(numin):
    return "{:.3f}".format(numin)


class PressureSensor(Widget):
    psi_per_kpa = 1./6.89476
    
    print("\n\n***\ninitializing pressure sensor\n***\n\n")
    
    data = StringProperty(10)
    
    def __init__(self, **kwargs):
        super(PressureSensor, self).__init__(**kwargs)
        self.numdat = 10 + np.random.randn()
        
        print(self.numdat*self.psi_per_kpa)
        

    def pull(self):
        self.numdat = 10 + np.random.randn()
        self.data = MakeDataPresentable(self.numdat)
        print(self.numdat*self.psi_per_kpa)


class FrictionDisplay(Widget):

    def __init__(self, **kwargs):
        super(FrictionDisplay, self).__init__(**kwargs)
        #self.thefig = RealTimeFigure()
        self.bggo = (0,0.4,0,1)
        self.bgstop = (0.6,0,0,1)
        #print('\n\n\n\n******')
        #print(self.thefig)
        #print('******\n\n\n\n')

    #thefig = ObjectProperty(None)
    ps1 = ObjectProperty(None)
    ps2 = ObjectProperty(None)
    
    
    bgcol = ListProperty((0.6,0,0,1))
    
    tcol = ListProperty((1,1,1,1))
    pcol = ListProperty((0.2,0.2,0.2,1))
    
    pdiff = StringProperty(None)
    font_size = NumericProperty(50)
    
    
    def update(self,dt):
        
        self.ps1.pull()
        self.ps2.pull()
        numdiff = abs(self.ps1.numdat - self.ps2.numdat)
        self.pdiff = MakeDataPresentable(numdiff)
        #self.thefig.redraw()
        if numdiff>1.:
            self.bgcol = self.bggo
        else:
            self.bgcol = self.bgstop

class FrictionTrainerApp(App):

    def build(self):
        #print('\n\n\n*********building**********\n\n\n')
        display = FrictionDisplay()
        Clock.schedule_interval(display.update, 60.0/60.0)
        return display


if __name__ == '__main__':
    FrictionTrainerApp().run()

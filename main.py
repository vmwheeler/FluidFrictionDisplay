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
    
    print("initializing pressure sensor")
    
    data = StringProperty(10)
    
    def __init__(self, **kwargs):
        super(PressureSensor, self).__init__(**kwargs)
        self.numdat = 10 + np.random.randn()

    def pull(self):
        self.numdat = 10 + np.random.randn()
        self.data = MakeDataPresentable(self.numdat)
        
        
class RealTimeFigure(BoxLayout):
    
    
    
    def __init__(self, **kwargs):
        super(RealTimeFigure, self).__init__(**kwargs)
        
        self.ts = np.linspace(0,5,num=50)        
        self.data = np.sin(self.ts)
        
        
        #self.add_widget(self.kvthingy)
        #self.add_widget(self.fig.canvas)
        
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.ts,self.data) 
        #data = ListProperty(None)
        self.kvthingy = self.fig.canvas
        self.add_widget(self.kvthingy)
        
        
        print('\n\n****')
        print('first draw')
        print(self.kvthingy)
        print('****\n\n')
        
    def redraw(self):
                
        self.data[0] = self.data[0]+0.1
            
        print('\n\n\n\n******')
        print('redrawing')
        print(self.data)
        print('******\n\n\n\n')
        
        #self.ax.plot(self.ts,self.data)
        #self.kvthingy.figure.axes[0].plot(self.ts,self.data)  
        self.ax.clear()
        self.ax.plot(self.ts,self.data, 'bo-', linewidth=5.0)
        
        self.kvthingy.draw()
        
    #fig = ObjectProperty()
    

class FrictionDisplay(Widget):

    def __init__(self, **kwargs):
        super(FrictionDisplay, self).__init__(**kwargs)
        self.thefig = RealTimeFigure()
        print('\n\n\n\n******')
        print(self.thefig)
        print('******\n\n\n\n')

    #thefig = ObjectProperty(None)
    ps1 = ObjectProperty(None)
    ps2 = ObjectProperty(None)
    
    pdiff = StringProperty(None)
    font_size = NumericProperty(50)
    
    
    def update(self,dt):
        
        self.ps1.pull()
        self.ps2.pull()
        self.pdiff = MakeDataPresentable(abs(self.ps1.numdat - self.ps2.numdat))
        self.thefig.redraw()



class FrictionTrainerApp(App):

    def build(self):
        #print('\n\n\n*********building**********\n\n\n')
        display = FrictionDisplay()
        Clock.schedule_interval(display.update, 60.0/60.0)
        return display


if __name__ == '__main__':
    FrictionTrainerApp().run()
